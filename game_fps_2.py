import sys
import glob
import serial
from time import sleep
import re
import pyautogui
import numpy as np
projects = ["Dino", "FPS"]

from pynput.mouse import Button, Controller
def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
print(serial_ports())

def outliers_modified_z_score(ys, threshold=3.5):
    ys_arr = np.array(ys)
    median_y = np.median(ys_arr)
    median_absolute_deviation_y = np.median(np.abs(ys_arr - median_y))
    modified_z_scores = 0.6745 * (ys_arr - median_y) / median_absolute_deviation_y
    return (ys_arr[np.abs(modified_z_scores) > threshold]).tolist()

ser = serial.Serial(port='/dev/tty.usbmodem14101', baudrate=9600)
import time

data=[]
count=0
mouse = Controller()
while True:
    getVal = ser.readline()
    non_decimal = re.compile(r'[^\d.]+')
    data.append(int(float(non_decimal.sub('', getVal.decode("utf-8")))))
    data = data[-60:]
    count+=1
    if sum(data)/60 > 300 and count==40:
        pyautogui.scroll(1)
        time.sleep(0.25)
        print("Scroll " + str((sum(data) / len(data))))
        data = [0 for i in range(60)]
        count=0
    elif sum(data) / len(data) > 125 and sum(data) / 60 < 250 and count==40:
        pyautogui.dragTo(button='left')
        pyautogui.click(clicks=2)
        time.sleep(0.25)
        print("Click "+ str((sum(data) / len(data))))
        data = [0 for i in range(60)]
        count = 0
    if count%40==0:
        count=0



