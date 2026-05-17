# %%
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from typing import List, Dict, Tuple
from tqdm import tqdm
from scipy import fft, signal
import pickle
from scipy.io.wavfile import read
from collections import defaultdict
# %%
from create_constellations import create_constellation
from create_hashes import create_hashes

# %%
songs = glob.glob('data/*.wav')

song_index = {}

database = defaultdict(list)
for index, filename in enumerate(tqdm(sorted(songs))):
    song_index[index] = filename

    Fs, audio_input = read(filename)

    if audio_input.ndim == 2:
        audio_input = audio_input.mean(axis=1)

    constellation = create_constellation(audio_input, Fs)

    for h, time_pair in create_hashes(constellation, index):
        database[h].append(time_pair)
# %%
with open("database.pickle", 'wb') as db:
    pickle.dump(database, db, pickle.HIGHEST_PROTOCOL)
with open("song_index.pickle", 'wb') as songs:
    pickle.dump(song_index, songs, pickle.HIGHEST_PROTOCOL)
