from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time
import serial
import time
import software.signal_filters as f

app = QtGui.QApplication([])

start_time = time.time()

p = pg.plot()
p.setWindowTitle('live plot from serial')
p.setLabels(left=('millivolts', 'mV'))
curve = p.plot()

data = [0]
ser = serial.Serial("COM6", 9600, timeout=0.5)
t = [0]

def update():
    global curve, data
    line = ser.readline()
    try:
        # 188uV per bit is ADS1115 16-bit ADC scaling (5V)
        # 3.223mV per bit is Arduino Yun Mini 10-bit ADS scaling (3.3V)
        data.append(float(line) * 3.223)  # Scaling factor
        t.append(time.time() - start_time)
        curve.setData(t, data)
        # data_filtered = f.butter_lowpass_filter(rate=100, data=data, freqHighCutoff=45, order=5)
        # curve.setData(t, data_filtered)
        p.setXRange(t[-1] - 5, t[-1] + 1)
        app.processEvents()
        # print('time taken = ' + str((t[-1]-t[-2])*1000) + 'ms')
        # print('bits waiting=' + str(ser.in_waiting), 'mseconds=' + str((t[-1] - t[-2])*1000), 'data=' + str(data[-1]))
        if len(data) > 5000:
            del data[0:-2]
            del t[0:-2]
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
