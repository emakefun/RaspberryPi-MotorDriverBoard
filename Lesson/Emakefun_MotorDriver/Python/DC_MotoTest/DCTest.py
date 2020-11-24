#!/usr/bin/python
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor, Raspi_Servo

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
myMotor = mh.getMotor(4)

# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(150)
myMotor.run(Raspi_MotorHAT.FORWARD);
# turn on motor
myMotor.run(Raspi_MotorHAT.RELEASE);


while (True):
	print ("Forward! ")

	print ("\tSpeed up...")
	for i in range(255):
		myMotor.setSpeed(i)
		myMotor.run(Raspi_MotorHAT.FORWARD)
		time.sleep(0.01)

	print ("\tSlow down...")
	for i in reversed(range(255)):
		myMotor.setSpeed(i)
		myMotor.run(Raspi_MotorHAT.FORWARD)
		time.sleep(0.01)

	print ("Backward! ")
    
	print ("\tSpeed up...")
	for i in range(255):
		myMotor.setSpeed(i)
		myMotor.run(Raspi_MotorHAT.BACKWARD)
		time.sleep(0.01)

	print ("\tSlow down...")
	for i in reversed(range(255)):
		myMotor.setSpeed(i)
		myMotor.run(Raspi_MotorHAT.BACKWARD)
		time.sleep(0.01)

	print ("Release")
	myMotor.run(Raspi_MotorHAT.RELEASE)
	time.sleep(1.0)
