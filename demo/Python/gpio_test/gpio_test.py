#!/usr/bin/python
from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_Servo

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Emakefun_MotorHAT(addr=0x60, freq=1000)


while (True):
    print ("S1 HIGH! ")
    mh.setPin(Emakefun_MotorHAT.S1, 1)
    time.sleep(1)
    print ("S1 LOW! ")
    mh.setPin(Emakefun_MotorHAT.S1, 0)
    time.sleep(1)