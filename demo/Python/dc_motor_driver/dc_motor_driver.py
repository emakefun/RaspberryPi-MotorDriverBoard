#!/usr/bin/python
from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_Servo

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Emakefun_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
M4 = mh.getMotor(4)

# set the speed to start, from 0 (off) to 255 (max speed)
M4.setSpeed(150)
M4.run(Emakefun_MotorHAT.FORWARD);
# turn on motor
M4.run(Emakefun_MotorHAT.RELEASE);


while (True):
    print ("Forward! ")

    print ("\tSpeed up...")
    for i in range(255):
        M4.setSpeed(i)
        M4.run(Emakefun_MotorHAT.FORWARD)
        time.sleep(0.01)

    print ("\tSlow down...")
    for i in reversed(range(255)):
        M4.setSpeed(i)
        M4.run(Emakefun_MotorHAT.FORWARD)
        time.sleep(0.01)

    print ("Backward! ")
    
    print ("\tSpeed up...")
    for i in range(255):
        M4.setSpeed(i)
        M4.run(Emakefun_MotorHAT.BACKWARD)
        time.sleep(0.01)

    print ("\tSlow down...")
    for i in reversed(range(255)):
        M4.setSpeed(i)
        M4.run(Emakefun_MotorHAT.BACKWARD)
        time.sleep(0.01)

    print ("Release")
    M4.run(Emakefun_MotorHAT.RELEASE)
    time.sleep(1.0)