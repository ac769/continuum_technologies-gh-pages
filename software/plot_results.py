import matplotlib.pyplot as plt
import sys

with open('data.txt', 'r') as file:
    data = file.readlines()
data = [x.strip() for x in data]
data = [float(i) for i in data]

with open('time.txt', 'r') as file:
    time = file.readlines()
time = [x.strip() for x in time]
time = [float(i) for i in time]

plt.plot(time, data, label='Data vs Time')
plt.show()
