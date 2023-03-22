#!/usr/bin/python

from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_Servo
import time
mh = Emakefun_MotorHAT(addr=0x60)

myServo = mh.getServo(1)
speed = 9
while (True):
    myServo.writeServoWithSpeed(0, speed)
    time.sleep(1)

    myServo.writeServoWithSpeed(90, speed)
    time.sleep(1)

    myServo.writeServoWithSpeed(180, speed)
    time.sleep(1)

    # for i in range (0, 181, 10):
    #     myServo.writeServo(i, 9)
    #     time.sleep(0.02)
    # time.sleep(1)
    # for i in range (180, -1, -10):
    #     myServo.writeServo(i, 9)
    #     time.sleep(0.02)
    # time.sleep(1)

