import serial
import time
import matplotlib.pyplot as plt
import csv

start_time = time.time()
ser = serial.Serial('COM4', timeout=0.1)
t = []
V_byte = []

# Read the serial port
while time.time() - start_time < 10:
    t.append(time.time() - start_time)
    V_byte.append(ser.readline())
    time.sleep(0.01)

# Convert the serial port data to floating point number
V_float = []
for i in V_byte:
    dummy = i.decode("utf-8")
    if dummy.rstrip():
        #V_float.append(float(dummy.rstrip()))
        V_float.append(dummy.rstrip())
    else:
        V_float.append(float(0))

#print(t, V_float)

plt.plot(t, V_float, label='Noisy signal')
plt.show()

with open('data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows([t, V_float])
