# %%
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy import fft, signal
import sys
from scipy.io.wavfile import read
from create_constellations import create_constellation
from create_hashes import create_hashes


if len(sys.argv) < 2:
    print("no audio recording file given, try again :(")
    exit(1)

file_path = sys.argv[1]
Fs, audio_input = read(file_path)


constellation = create_constellation(audio_input, Fs)
hashes = create_hashes(constellation, None)

# %%
database = pickle.load(open('database.pickle', 'rb'))
song_index_lookup = pickle.load(open("song_index.pickle", "rb"))


def score_songs(hashes):
    matches_per_song = {}

    for hash_value, (sample_time, _) in hashes:

        if hash_value in database:
            matching_occurences = database[hash_value]
            for source_time, song_index in matching_occurences:
                if song_index not in matches_per_song:
                    matches_per_song[song_index] = []
                matches_per_song[song_index].append((hash_value, sample_time, source_time))
            

    # %%
    scores = {}
    for song_index, matches in matches_per_song.items():
        song_scores_by_offset = {}
        for hash, sample_time, source_time in matches:
            delta = source_time - sample_time
            if delta not in song_scores_by_offset:
                song_scores_by_offset[delta] = 0
            song_scores_by_offset[delta] += 1

        max = (0, 0)
        for offset, score in song_scores_by_offset.items():
            if score > max[1]:
                max = (offset, score)
        
        scores[song_index] = max

    # Sort the scores for the user
    scores = list(sorted(scores.items(), key=lambda x: x[1][1], reverse=True)) 
    
    return scores

scores = score_songs(hashes)

print("\n" + "=" * 60)
print("AUDIO MATCH RESULTS")
print("=" * 60)

for i, (song_index, (offset, score)) in enumerate(scores):
    song_name = song_index_lookup[song_index]

    print(f"\nMatch #{i + 1}")
    print(f"Song       : {song_name}")
    print(f"Score      : {score}")
    print(f"Offset     : {offset}")

print("\n" + "=" * 60)

# %%