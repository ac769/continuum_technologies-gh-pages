"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 0.1
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

devices = p.get_device_count()

def valid_test(device):
    """given a device ID and a rate, return TRUE/False if it's valid."""
    try:
        info = p.get_device_info_by_index(device)
        if not info["maxInputChannels"] > 0:
            return False
        return True
    except:
        return False

mics = {}
mic_count = 0
for device in range(0, devices):
    if valid_test(device):
        mics[str(mic_count)] = device
        mic_count += 1

print(f'Number of devices: {devices}')
print(f'Number of mics: {len(mics)}')
mic = 1

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=mic)

print(f"*** recording from mic index: {mic}")
device_info = p.get_device_info_by_index(mics[str(mic)])
print('name: ' + device_info['name'])

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    print(data)

print("*** done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
