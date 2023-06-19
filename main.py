from microbit import *
import radio


identity = 'transmitter'

radio.on()

if identity == 'transmitter':
    while True:
        pressed = False
        if button_b.is_pressed():
            pressed = True
        gesture = accelerometer.current_gesture()
        x = str(accelerometer.get_x())
        y = str(accelerometer.get_y())
        z = str(accelerometer.get_z())
        message = str(pressed) + "|" + x + " " + y + " " + z + "|" + gesture
        radio.send(message)
        sleep(10)
        
if identity == 'receiver':
    while True:
        transmission = radio.receive()
        if transmission:
            print(transmission)