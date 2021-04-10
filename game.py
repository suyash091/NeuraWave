import sys
import glob
import serial
from time import sleep
import re
import pyautogui

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


ser = serial.Serial(port='/dev/tty.usbmodem14101', baudrate=9600)

while True:
    getVal = ser.readline()
    non_decimal = re.compile(r'[^\d.]+')
    if int(float(non_decimal.sub('', getVal.decode("utf-8")))) > 700 :
        pyautogui.press("space")
        #pyautogui.press("up")
        pyautogui.scroll(1)
