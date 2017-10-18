from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import time
import software.signal_filters as f
import sys

data = [0]
ser = serial.Serial("COM4", 9600, timeout=0.5)
t = [0]

start_time = time.time()
time2 = []
while time.time() - start_time < 3:
    line = ser.readline()
    print('data: ', float(line))

# Calibration
print('Beginning calibration')
print('Please make your arm straight for 3 seconds...')
time.sleep(3)
ser.reset_input_buffer()
ser.reset_output_buffer()
arm_straight = float(ser.readline())  # Voltage for ~180 degrees
print('Done')

print('Please bend your arm for 3 seconds...')
time.sleep(3)
ser.reset_input_buffer()
ser.reset_output_buffer()
arm_bent = float(ser.readline())  # Voltage for 45 degrees
print('Done')

print(arm_straight, arm_bent)

ser.reset_input_buffer()
ser.reset_output_buffer()

# while True:
#     line = float(ser.readline())
#     angle = 180 - (line - arm_straight) / (arm_bent - arm_straight) * 135
#     print(angle)

app = QtGui.QApplication([])

start_time = time.time()

p = pg.plot()
p.setWindowTitle('live plot from serial')
p.setLabels(left=('millivolts', 'mV'))
curve = p.plot()

angle = [0]

def update():
    global curve, data
    line = ser.readline()

    try:
        data = float(line)
        angle.append(180 - (data - arm_straight) / (arm_bent - arm_straight) * 135)
        t.append(time.time() - start_time)
        # curve.setData(t, angle)
        angle_filtered = f.butter_lowpass_filter(rate=100, data=angle, freqHighCutoff=45, order=5)
        curve.setData(t, angle_filtered)
        p.setXRange(t[-1] - 5, t[-1] + 1)
        app.processEvents()
        # print('time taken = ' + str((t[-1]-t[-2])*1000) + 'ms')
        # print('bits waiting=' + str(ser.in_waiting), 'mseconds=' + str((t[-1] - t[-2])*1000), 'data=' + str(data[-1]))
        if ser.in_waiting > 100:
            print('queue buffer is incresing', ser.in_waiting)
    except ValueError:
        print('!!! VALUE ERROR', line)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
