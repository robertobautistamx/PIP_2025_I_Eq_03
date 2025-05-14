from asyncio import timeout

import serial as control

arduino = (control.Serial("COM3", baudrate=9600, timeout=1))


while True:
    v=input("Valor de control para el led:")
    arduino.write(v.encode())

#21 - 35, renombrar caerpetas , joystick 36