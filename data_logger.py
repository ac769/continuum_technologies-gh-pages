import serial
import time
import csv

start_time = time.time()
ser = serial.Serial('COM19', timeout=5, baudrate=9600)
t = []
V_byte = []
data = []

while time.time() - start_time < 10:
    input = int(ser.readline().rstrip())
    try:
        data.append(input)
        t_read = time.time()
        # print(ser.in_waiting)
        # print(ser.out_waiting)
    except Exception as e:
        print(e)

    t.append(t_read - start_time)
    print(input, t_read - start_time)


with open('data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows([t, data])

print("Wrote %d samples to data.csv" % (len(data),))
