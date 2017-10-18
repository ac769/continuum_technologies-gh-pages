# Requires install from: https://github.com/IanHarvey/bluepy
# Runs on python 3.5
from bluepy.btle import *
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
knee_mac = config['MAC']['knee']
ankle_mac = config['MAC']['ankle']

start_time = time.time()

data = []
data2 = []
data3 = []
data4 = []
angles = []

data = [0]
t = [0]

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        global data2, data3, data4, angle
        if cHandle == 37:
            print(data.decode("utf-8"))
        else:
            print('received an unexpected handle')

print('Attempting to connect...')
per = Peripheral(knee_mac, "public")
per.setDelegate(MyDelegate())

print("Connected")


while True:
    if per.waitForNotifications(5):
        continue
