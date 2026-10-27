import glob
import pickle
from collections import defaultdict

from scipy.io.wavfile import read
from tqdm import tqdm

from constellation import create_constellation
from hashing import create_hashes


def main():
    song_paths = {}
    database = defaultdict(list)

    for song_id, path in enumerate(tqdm(sorted(glob.glob("data/*.wav")))):
        song_paths[song_id] = path

        sample_rate, audio = read(path)
        constellation = create_constellation(audio, sample_rate)

        for hash_value, occurrence in create_hashes(constellation, song_id):
            database[hash_value].append(occurrence)

    with open("database.pickle", "wb") as f:
        pickle.dump(database, f, pickle.HIGHEST_PROTOCOL)
    with open("song_index.pickle", "wb") as f:
        pickle.dump(song_paths, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
