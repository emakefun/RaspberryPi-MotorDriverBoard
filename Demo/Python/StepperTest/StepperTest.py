#!/usr/bin/python
#import Emakefun_MotorHAT, Emakefun_DCMotor, Raspi_Stepper 
from Emakefun_MotorHAT import Emakefun_MotorHAT, Emakefun_DCMotor, Emakefun_StepperMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Emakefun_MotorHAT(0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE)
	mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)  	# 200 steps/rev, motor port #1
myStepper.setSpeed(30)  		# 30 RPM

while (True):
	print("Single coil steps")
	myStepper.step(100, Emakefun_MotorHAT.FORWARD,  Emakefun_MotorHAT.SINGLE)
	myStepper.step(100, Emakefun_MotorHAT.BACKWARD, Emakefun_MotorHAT.SINGLE)

	print("Double coil steps")
	myStepper.step(100, Emakefun_MotorHAT.FORWARD,  Emakefun_MotorHAT.DOUBLE)
	myStepper.step(100, Emakefun_MotorHAT.BACKWARD, Emakefun_MotorHAT.DOUBLE)

	print("Interleaved coil steps")
	myStepper.step(100, Emakefun_MotorHAT.FORWARD,  Emakefun_MotorHAT.INTERLEAVE)
	myStepper.step(100, Emakefun_MotorHAT.BACKWARD, Emakefun_MotorHAT.INTERLEAVE)

	print("Microsteps")
	myStepper.step(100, Emakefun_MotorHAT.FORWARD,  Emakefun_MotorHAT.MICROSTEP)
	myStepper.step(100, Emakefun_MotorHAT.BACKWARD, Emakefun_MotorHAT.MICROSTEP)
