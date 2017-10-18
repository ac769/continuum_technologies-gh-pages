import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

start_time = time.time()
ser = serial.Serial('COM4', timeout=5)
t = []
V_byte = []
time = float(0)

while len(V_byte) < 30 * 100 * 0.1:
    input = ser.readline().strip()
    try:
        input = int(input)
        V_byte += [input]

    except Exception as e:
        #print(e)
        #V_byte += [0, 0]
        V_byte += [0]

    time += 0.001
    t.append(time)

with open('pulsies.txt', 'w') as f:
   np.array(V_byte, dtype='float').tofile(f, sep='\n')

print("Wrote %d samples to pulsies.txt" % (len(V_byte),))

original_signal = np.array(V_byte)
t = np.array(t)

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

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

# Filter requirements.
order = 5
fs = 1000.0  # sample rate, Hz
cutoff = 45  # desired cutoff frequency of the filter, Hz
lowcut = 0.5
highcut = 45

# Get the filter coefficients so we can check its frequency response.
b, a = butter_lowpass(cutoff, fs, order)

# Plot the frequency response.
w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5 * fs)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()

# Filter the data, and plot both the original and filtered signals.
y = butter_lowpass_filter(original_signal, cutoff, fs, order)
#y = butter_bandpass_filter(original_signal, lowcut, highcut, fs, order)

plt.subplot(2, 1, 2)
plt.plot(t, original_signal, 'b-', label='orig signal')
plt.plot(t, y, 'g-', linewidth=2, label='filtered signal')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend()

plt.subplots_adjust(hspace=0.35)
plt.show()

import sys
sys.exit(0)

raise Exception("Major Fail!")
# Read the serial port
while time.time() - start_time < 2:
    t.append(time.time() - start_time)
    V_byte.append(ser.readline())
    time.sleep(0.01)

# Convert the serial port data to floating point number
V_float = []
for i in V_byte:
    dummy = i.decode("latin1")
    print("XXX", repr(dummy))
    continue
    if dummy.rstrip():
        # V_float.append(float(dummy.rstrip()))
        V_float.append(dummy.rstrip())
    else:
        V_float.append(float(0))

# print(t, V_float)

plt.plot(t, V_float, label='Noisy signal')
plt.show()

with open('data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows([t, V_float])
