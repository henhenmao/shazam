# pip install matplotlib to examine windows

# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io.wavfile import read

# Read the input WAV files
sample_rate, audio = read("data/001. 24kgoldn - Mood (feat. iann dior).wav")

time_to_plot = np.arange(sample_rate * 1, sample_rate * 1.5, dtype=int)
plt.plot(time_to_plot, audio[time_to_plot])
plt.title("Sound Signal")
plt.xlabel("Time Index")
plt.ylabel("Magnitude")

# %%
window_length_seconds = 2
window_length_samples = int(window_length_seconds * sample_rate)
window_length_samples += window_length_samples % 2
peaks_per_window = 7

amount_to_pad = window_length_samples - audio.size % window_length_samples

padded_audio = np.pad(audio, (0, amount_to_pad))

frequencies, _, stft = signal.stft(
    padded_audio, sample_rate, nperseg=window_length_samples, nfft=window_length_samples
)

windows = stft.T
num_windows = windows.shape[0]
window = windows[num_windows // 2 + 5, :]
plt.plot(frequencies, abs(window) ** 2)
plt.title("Power Spectrum of Window")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")

# %%
spectrum = np.log(abs(window) ** 2)
plt.figure()
plt.plot(frequencies, spectrum)
plt.title("Log Power Spectrum of Window")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Log Power")

# %%
peaks, props = signal.find_peaks(abs(window), prominence=0, distance=500)
num_peaks = min(peaks_per_window, len(peaks))
# Get the num_peaks largest peaks from the prominences
largest_peaks = np.argpartition(props["prominences"], -num_peaks)[-num_peaks:]
constellation_map = []
for peak in peaks[largest_peaks]:
    constellation_map.append([frequencies[peak], abs(window)[peak]])

plt.figure()
plt.plot(frequencies, abs(window), label="Spectrum")
plt.scatter(*zip(*constellation_map), color="r", zorder=10, label="Peaks")
plt.legend()
plt.title("Spectrum Peaks of Window")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.show()
