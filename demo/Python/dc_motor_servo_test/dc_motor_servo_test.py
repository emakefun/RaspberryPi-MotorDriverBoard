#!/usr/bin/python
from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_Servo

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Emakefun_MotorHAT(addr=0x60, freq=50)   # servo driver must 50HZ pwm

M1 = mh.getMotor(1)
M2 = mh.getMotor(2)
M3 = mh.getMotor(3)
M4 = mh.getMotor(4)

M1.setSpeed(255)
M2.setSpeed(255)
M3.setSpeed(255)
M4.setSpeed(255)

S1 = mh.getServo(1)
S2 = mh.getServo(2)
S3 = mh.getServo(3)
S4 = mh.getServo(4)
S5 = mh.getServo(5)
S6 = mh.getServo(6)
S7 = mh.getServo(7)
S8 = mh.getServo(8)

seveo_speed = 10    #  min: 1 - max: 10
# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE)
    mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

while (True):
    print ("Servo degree = 0")
    S1.writeServoWithSpeed(0, seveo_speed)
    S2.writeServoWithSpeed(0, seveo_speed)
    S3.writeServoWithSpeed(0, seveo_speed)
    S4.writeServoWithSpeed(0, seveo_speed)
    S5.writeServoWithSpeed(0, seveo_speed)
    S6.writeServoWithSpeed(0, seveo_speed)
    S7.writeServoWithSpeed(0, seveo_speed)
    S8.writeServoWithSpeed(0, seveo_speed)
    print ("Forward! ")
    M1.run(Emakefun_MotorHAT.FORWARD)
    M2.run(Emakefun_MotorHAT.FORWARD)
    M3.run(Emakefun_MotorHAT.FORWARD)
    M4.run(Emakefun_MotorHAT.FORWARD)
    time.sleep(1.0)
    
    print ("Servo degree = 180")
    S1.writeServoWithSpeed(180, seveo_speed)
    S2.writeServoWithSpeed(180, seveo_speed)
    S3.writeServoWithSpeed(180, seveo_speed)
    S4.writeServoWithSpeed(180, seveo_speed)
    S5.writeServoWithSpeed(180, seveo_speed)
    S6.writeServoWithSpeed(180, seveo_speed)
    S7.writeServoWithSpeed(180, seveo_speed)
    S8.writeServoWithSpeed(180, seveo_speed)
    print ("Backward! ")
    M1.run(Emakefun_MotorHAT.BACKWARD)
    M2.run(Emakefun_MotorHAT.BACKWARD)
    M3.run(Emakefun_MotorHAT.BACKWARD)
    M4.run(Emakefun_MotorHAT.BACKWARD)
    time.sleep(1.0)
