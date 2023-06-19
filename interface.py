import math
import pygame
import numpy as np
import serial
import serial.tools.list_ports as list_ports
from math import sin, cos
import pyautogui

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1

def find_comport(pid, vid, baud):
    ''' return a serial port '''
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print('port: {}'.format(p))
        try:
            print('pid: {} vid: {}'.format(p.pid, p.vid))
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print('found target device pid: {} vid: {} port: {}'.format(
                p.pid, p.vid, p.device))
            ser_port.port = str(p.device)
            return ser_port
    return None

    
def main():
    lines = []
    pyautogui.PAUSE = 0.0001
    mousedown = False
    
    while True:
        line = ser_micro.readline().decode('utf-8')
        if line:
            lines.append(line.strip('\n'))
            if len(lines) > 100:
                lines.pop(0)

            parsed = list(map(lambda x: int(x), lines[-1].split('|')[1].split()))
            pressed = lines[-1].split('|')[0]
            x, y, z = parsed
            k = 0.01
            pyautogui.move(-x*k, -y*k)
            print(pressed)
            if pressed == "True":
                if mousedown == False:
                    pyautogui.mouseDown()
                    mousedown = True
            else:
                if mousedown == True:
                    pyautogui.mouseUp()
                    mousedown = False
            
        
    
    

print('looking for microbit')
ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
if not ser_micro:
    print('microbit not found')
    exit()
print('opening and monitoring microbit port')
ser_micro.open()
main()
ser_micro.close()
