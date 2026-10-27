import pickle
import sys
from collections import defaultdict

from scipy.io.wavfile import read

from constellation import create_constellation
from hashing import create_hashes

# unrelated songs typically line up only a handful of hashes by chance,
# so anything below this is reported as no match
MIN_MATCH_SCORE = 10


def score_songs(clip_hashes, database):
    matches_per_song = defaultdict(list)

    for hash_value, (clip_time, _) in clip_hashes:
        for song_time, song_id in database.get(hash_value, []):
            matches_per_song[song_id].append((clip_time, song_time))

    scores = {}
    for song_id, matches in matches_per_song.items():
        offset_counts = defaultdict(int)
        for clip_time, song_time in matches:
            offset_counts[song_time - clip_time] += 1

        scores[song_id] = max(offset_counts.items(), key=lambda x: x[1])

    # Sort the scores for the user
    return sorted(scores.items(), key=lambda x: x[1][1], reverse=True)


def identify(audio, sample_rate, database):
    return score_songs(create_hashes(create_constellation(audio, sample_rate)), database)


def main():
    if len(sys.argv) < 2:
        print("no audio recording file given, try again :(")
        sys.exit(1)

    sample_rate, audio = read(sys.argv[1])

    with open("database.pickle", "rb") as f:
        database = pickle.load(f)
    with open("song_index.pickle", "rb") as f:
        song_paths = pickle.load(f)

    scores = identify(audio, sample_rate, database)

    print("\n" + "=" * 60)
    print("AUDIO MATCH RESULTS")
    print("=" * 60)

    if not scores or scores[0][1][1] < MIN_MATCH_SCORE:
        print("\nNo confident match found")

    for rank, (song_id, (_, score)) in enumerate(scores, start=1):
        print(f"\nMatch #{rank}")
        print(f"Song       : {song_paths[song_id]}")
        print(f"Score      : {score}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
