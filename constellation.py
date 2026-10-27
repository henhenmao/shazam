from math import gcd

import numpy as np
from scipy import signal
from scipy.ndimage import maximum_filter

# everything is resampled to this rate so songs and recordings made at
# different rates (44.1 kHz vs 48 kHz) produce comparable spectrograms
SAMPLE_RATE = 11025
WINDOW_SIZE = 1024
HOP_SIZE = 256
MAX_FREQUENCY = 4000

# A peak must be the loudest point within this many frequency bins / frames
NEIGHBORHOOD_FREQUENCY_BINS = 10
NEIGHBORHOOD_FRAMES = 10
# Ignore peaks this many dB below the loudest point of the clip
PEAK_THRESHOLD_DB = -40
PEAKS_PER_SECOND = 30

FRAMES_PER_SECOND = SAMPLE_RATE / HOP_SIZE


def prepare_audio(audio, sample_rate):
    audio = audio.astype(np.float32)
    if audio.ndim == 2:
        audio = audio.mean(axis=1)

    divisor = gcd(sample_rate, SAMPLE_RATE)
    audio = signal.resample_poly(audio, SAMPLE_RATE // divisor, sample_rate // divisor)

    return audio / (np.max(np.abs(audio)) + 1e-9)


def create_constellation(audio, sample_rate):
    audio = prepare_audio(audio, sample_rate)

    frequencies, _, stft = signal.stft(
        audio,
        SAMPLE_RATE,
        nperseg=WINDOW_SIZE,
        noverlap=WINDOW_SIZE - HOP_SIZE
    )

    spectrogram = 20 * np.log10(np.abs(stft[frequencies <= MAX_FREQUENCY]) + 1e-10)

    neighborhood_max = maximum_filter(
        spectrogram,
        size=(2 * NEIGHBORHOOD_FREQUENCY_BINS + 1, 2 * NEIGHBORHOOD_FRAMES + 1)
    )
    is_peak = (spectrogram == neighborhood_max) & (spectrogram > spectrogram.max() + PEAK_THRESHOLD_DB)
    frequency_bins, time_indices = np.nonzero(is_peak)
    loudness = spectrogram[frequency_bins, time_indices]

    # keep only the loudest peaks in each second so quiet passages and
    # dense passages contribute a similar number of hashes
    seconds = (time_indices / FRAMES_PER_SECOND).astype(int)
    constellation_map = []
    for second in np.unique(seconds):
        in_second = np.nonzero(seconds == second)[0]
        loudest = in_second[np.argsort(loudness[in_second])[::-1][:PEAKS_PER_SECOND]]
        constellation_map.extend(zip(time_indices[loudest].tolist(), frequency_bins[loudest].tolist()))

    return sorted(constellation_map)
