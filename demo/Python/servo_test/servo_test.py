#!/usr/bin/python

from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_Servo
import time
mh = Emakefun_MotorHAT(addr=0x60, freq=50)   # servo driver must 50HZ pwm)

S1 = mh.getServo(1)
S2 = mh.getServo(2)
S3 = mh.getServo(3)
S4 = mh.getServo(4)
S5 = mh.getServo(5)
S6 = mh.getServo(6)
S7 = mh.getServo(7)
S8 = mh.getServo(8)

speed = 5    #  min: 1 - max: 10

while (True):
    speed = 5 
    S1.writeServoWithSpeed(0, speed)
    time.sleep(1)

    speed = 10
    S1.writeServoWithSpeed(90, speed)
    time.sleep(1)

    S1.writeServoWithSpeed(180, speed)
    time.sleep(1)

