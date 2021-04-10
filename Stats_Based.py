import sys
import glob
import serial
from time import sleep
import re
import pyautogui
import numpy as np
projects = ["Dino", "FPS"]

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
avglist=[]
flag=False
count=0
non_decimal = re.compile(r'[^\d.]+')


print("Loose Your hand")
time.sleep(5)
normal=0
for i in range(200):
    getVal = ser.readline()
    normal+=int(float(non_decimal.sub('', getVal.decode("utf-8"))))

normal=normal/200
print(normal)
time.sleep(3)


start_time = time.time()
while True:
    getVal = ser.readline()

    data.append(int(float(non_decimal.sub('', getVal.decode("utf-8")))))
    data=data[-40:]
    if int(time.time() - start_time) == 5:
        print("Perform the gesture")
        start_time = time.time()
        count=0
        flag=True
    if flag and count==30:
        flag=False
        print(sum(data)/len(data))
        avglist.append(sum(data)/len(data))
        if len(avglist)>10:
            break
    count+=1

correct=[]
outliers=outliers_modified_z_score(avglist, threshold=1.5)
for i in avglist:
    if i not in outliers:
        correct.append(i)

print(correct)
thres1 = sum(correct[:int(len(correct)/2)])/int(len(correct)/2) - normal
print(thres1)


data=[]
avglist=[]
flag=False
count=0

start_time = time.time()
while True:
    getVal = ser.readline()

    data.append(int(float(non_decimal.sub('', getVal.decode("utf-8")))))
    data=data[-40:]
    if int(time.time() - start_time) == 5:
        print("Perform the gesture")
        start_time = time.time()
        count=0
        flag=True
    if flag and count==30:
        flag=False
        print(sum(data)/len(data))
        avglist.append(sum(data)/len(data))
        if len(avglist)>10:
            break
    count+=1

correct=[]
outliers=outliers_modified_z_score(avglist, threshold=1.5)
for i in avglist:
    if i not in outliers:
        correct.append(i)

print(correct)
thres2 = sum(correct[:int(len(correct)/2)])/int(len(correct)/2) - normal - normal - normal
print(thres2)







data=[]
while True:
    getVal = ser.readline()
    non_decimal = re.compile(r'[^\d.]+')
    data.append(int(float(non_decimal.sub('', getVal.decode("utf-8")))))
    data = data[-40:]
    if sum(data)/len(data) > thres2:
        pyautogui.scroll(1)
        time.sleep(0.15)
        #print(sum(data)/len(data))
        data = [0 for i in range(40)]
    elif sum(data) / len(data) > thres1:
        pyautogui.click()
        time.sleep(0.25)
        #print(sum(data) / len(data))
        data = [0 for i in range(40)]
        #pyautogui.press("up")
        #pyautogui.scroll(1)


