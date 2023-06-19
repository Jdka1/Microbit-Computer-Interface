import math
import pygame
import numpy as np
import serial
import serial.tools.list_ports as list_ports
from math import sin, cos

PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1

WINDOW_SIZE = (800, 800)

window = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))
clock = pygame.time.Clock()

cube_points = np.array([[-1, -1, 1],
                        [1,-1,1],
                        [1,1,1],
                        [-1,1,1],
                        [-1,-1,-1],
                        [1,-1,-1],
                        [1,1,-1],
                        [-1,1,-1]])

projection_matrix = np.array([[1,0,0],
                              [0,1,0],
                              [0,0,0]])


scale = 100
offset = (WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2)

angle_x = angle_y = angle_z = 0

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


def pygame_loop(angle_x, angle_y, angle_z, fps):
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    window.fill((0,0,0))
            
    rotation_x = np.array([[1, 0, 0],
                    [0, cos(angle_x), -sin(angle_x)],
                    [0, sin(angle_x), cos(angle_x)]])

    rotation_y = np.array([[cos(angle_y), 0, sin(angle_y)],
                    [0, 1, 0],
                    [-sin(angle_y), 0, cos(angle_y)]])

    rotation_z = np.array([[cos(angle_z), -sin(angle_z), 0],
                    [sin(angle_z), cos(angle_z), 0],
                    [0, 0, 1]])   
    
    points = []
    for point in cube_points:
        rotate_x = np.matmul(rotation_x, point)
        rotate_y = np.matmul(rotation_y, rotate_x)
        rotate_z = np.matmul(rotation_z, rotate_y)
        point_2d = np.matmul(projection_matrix, rotate_z)
        x = point_2d[0] * scale + offset[0]
        y = point_2d[1] * scale + offset[1]
        pygame.draw.circle(window, (255, 0, 0), (x, y), 5)
        points.append((x, y))
    for i in [[0,1],[0,3],[0,4],[1,2],[1,5],[2,6],[2,3],[3,7],[4,5],[4,7],[5,6],[6,7]]:
        pygame.draw.line(window, (255,255,255), points[i[0]], points[i[1]])
    pygame.display.update()
    
    

def main():
    lines = []
    
    while True:
        line = ser_micro.readline().decode('utf-8')
        if line:
            lines.append(list(map(lambda x: int(x), line.strip('\n').split())))
            if len(lines) > 500:
                lines.pop(0)
            print(lines[-1])
            k = 0.001
            pygame_loop(lines[-1][0]*k,lines[-1][1]*k,lines[-1][2]*k,120)
        
    
    

print('looking for microbit')
ser_micro = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
if not ser_micro:
    print('microbit not found')
    exit()
print('opening and monitoring microbit port')
ser_micro.open()
main()
ser_micro.close()
    