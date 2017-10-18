import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt
from clean_bad_trace import clean_bad_trace


file = open("processing/save_to_file/data.txt")
trace = file.readlines()

trace_clean = clean_bad_trace(trace)

print(trace_clean)
plt.plot(trace_clean, label='Noisy signal')
plt.show()

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


if __name__ == "__main__":
    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 5000.0
    lowcut = 500.0
    highcut = 1250.0

    # Filter our noisy signal.
    y = butter_bandpass_filter(trace_clean, lowcut, highcut, fs, order=6)
    plt.plot(y, label='Filtered signal (Hz)')
    plt.xlabel('time (seconds)')
    plt.hlines([-a, a], 0, T, linestyles='--')
    plt.grid(True)
    plt.axis('tight')
    plt.legend(loc='upper left')

    plt.show()