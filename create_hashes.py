# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, signal
from scipy.io.wavfile import read

from create_constellations import create_constellation
# %%
# Fs, audio_input = read("data/001. 24kgoldn - Mood (feat. iann dior).wav")

# constellation_map = create_constellation(audio_input, Fs)
upper_frequency = 23000
frequency_bits = 10
FAN_OUT = 10

def create_hashes(constellation_map, song_id=None):
    for i, (t1, f1) in enumerate(constellation_map):

        for (t2, f2) in constellation_map[i+1:i+1+FAN_OUT]:

            diff = t2 - t1
            if diff <= 1 or diff > 10:
                continue

            f1b = int(f1 / upper_frequency * (2 ** frequency_bits))
            f2b = int(f2 / upper_frequency * (2 ** frequency_bits))

            h = f1b | (f2b << 10) | (diff << 20)

            yield h, (t1, song_id)

# hashes = create_hashes(constellation_map)
# hashes
# %%
