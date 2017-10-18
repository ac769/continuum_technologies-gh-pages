import serial
import time

start_time = time.time()

data = [0]
ser = serial.Serial("COM6", 9600, timeout=0.5)
t = [0]

while True:
    line = ser.readline()
    try:
        print(float(line))
        if ser.in_waiting > 100:
            print('queue buffer is increasing', ser.in_waiting)
    except ValueError:
        print('!!! VALUE ERROR', line)
