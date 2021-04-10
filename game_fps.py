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
data0=[]
mouse = Controller()
while True:
    getVal = ser.readline()
    non_decimal = re.compile(r'[^\d.]+')
    data.append(int(float(non_decimal.sub('', getVal.decode("utf-8")))))
    data0.append(int(float(non_decimal.sub('', getVal.decode("utf-8")))))
    data = data[-40:]
    data0 = data0[-40:]
    if sum(data0)/len(data0) > 300:
        pyautogui.scroll(1)
        time.sleep(0.2)
        print("Scroll " + str((sum(data0) / len(data0))))
        data0 = [0 for i in range(40)]
        data = [0 for i in range(40)]
    elif sum(data) / len(data) > 105 and sum(data) / len(data) < 200:
        pyautogui.dragTo(button='left')
        pyautogui.click(clicks=2)
        time.sleep(0.25)
        print("Click "+ str((sum(data) / len(data))))
        data = [0 for i in range(40)]
        #pyautogui.press("up")
        #pyautogui.scroll(1)


