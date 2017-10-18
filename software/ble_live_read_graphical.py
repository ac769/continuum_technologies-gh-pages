from bluepy.btle import *
import time
import serial
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

start_time = time.time()

data = []
data2 = []
data3 = []
data4 = []
angles = []

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pen = pg.mkPen('k', width=8)

app = QtGui.QApplication([])
plotWidget = pg.plot(title='biomechanics')
plotWidget.setWindowTitle('elbow angle')
plotWidget.setLabels(left=('angle', 'degrees'))
plotWidget.plotItem.getAxis('left').setPen(pen)
plotWidget.plotItem.getAxis('bottom').setPen(pen)
curve = plotWidget.plot(pen=pen)
plotWidget.setYRange(20, 210)

data = [0]
ser = serial.Serial("/dev/rfcomm0", 9600, timeout=0.5)
t = [0]

# from calibration
arm_straight = 957
arm_bent = 987

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global data2, data3, data4, angle
        if cHandle == 37:
            data = data.decode("utf-8")
            data2.append(data)
            data3 = ''.join(data2)
            data4 = data3.splitlines()
            angle = 180 - (float(data4[-1]) - arm_straight) / (arm_bent - arm_straight) * 135
            print(data4[-1])
            angles.append(angle)
            # print(data4[-1], angle)
        else:
            print('received an unexpected handle')

print('Attempting to connect...')
mac1 = 'a4:d5:78:0d:1c:53'
mac2 = 'a4:d5:78:0d:2e:fc'
per = Peripheral(mac1, "public")
per.setDelegate(MyDelegate())

print("Connected")

def update():
    global curve, data, angles2
    if per.waitForNotifications(1):
        t.append(time.time() - start_time)
        x = list(range(0, len(angles), 1))
        angles2 = [float(i) for i in angles]
        curve.setData(x[-50:-1], angles2[-50:-1])
        app.processEvents()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()