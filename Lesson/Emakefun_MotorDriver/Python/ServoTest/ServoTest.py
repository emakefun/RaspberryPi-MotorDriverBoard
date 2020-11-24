#!/usr/bin/python

from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_Servo
import time
mh = Raspi_MotorHAT(addr=0x60)

myServo = mh.getServo(1)
while (True):

    for i in range (0, 181, 10):
        myServo.writeServo(i)
        time.sleep(0.02)
    time.sleep(2)
    for i in range (180, -1, -10):
        myServo.writeServo(i)
        time.sleep(0.02)

