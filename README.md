



# Emakefun_MotorDriverBoard

[English](README.md) 中文版

RaspberryPi 多功能电机驱动扩展板   [深圳市易创空间科技有限公司](www.emakefun.com)出品
![image](https://github.com/emakefun/emakefun-docs/raw/master/docs/open_source_hardware/UNO_mega2560_pic/icon.png)

## 特点

- 支持驱动8路舵机
- 支持4路直流电机
- 支持驱动2路4线步进电机
- 板载无源蜂鸣器
- 板载红外接收头
- 舵机电源可切换到外部供电

## 功能介绍

### 驱动舵机

#### C++代码

``` C++
#include "Emakefun_MotorShield.h"

int main () {
	Emakefun_MotorShield Pwm = Emakefun_MotorShield();
	Pwm.begin(50);
	Emakefun_Servo *myServo1 = Pwm.getServo(1);
	Emakefun_Servo *myServo2 = Pwm.getServo(2);
	Emakefun_Servo *myServo3 = Pwm.getServo(3);
	Emakefun_Servo *myServo4 = Pwm.getServo(4);
	Emakefun_Servo *myServo5 = Pwm.getServo(5);
	Emakefun_Servo *myServo6 = Pwm.getServo(6);
	Emakefun_Servo *myServo7 = Pwm.getServo(7);
	Emakefun_Servo *myServo8 = Pwm.getServo(8);

	while(1) {
		for (int i = 0; i <= 180; i+=10)
		{
			myServo1->writeServo(i);
			myServo2->writeServo(i);
			myServo3->writeServo(i);
			myServo4->writeServo(i);
			myServo5->writeServo(i);
			myServo6->writeServo(i);
			myServo7->writeServo(i);
			myServo8->writeServo(i);
			delay(20);
		}

		for (int i = 180; i >= 0; i-=10)
		{
			myServo1->writeServo(i);
			myServo2->writeServo(i);
			myServo3->writeServo(i);
			myServo4->writeServo(i);
			myServo5->writeServo(i);
			myServo6->writeServo(i);
			myServo7->writeServo(i);
			myServo8->writeServo(i);
			delay(20);
		}
	}
}
```

#### Python代码

``` Python
#!/usr/bin/python

from Raspi_PWM_Servo_Driver import PWM
import time
pwm = PWM(0x60)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

pwm.setPWMFreq(50)                        # Set frequency to 60 Hz
while (True):
  # Change speed of continuous servo on channel O
  pwm.setAllPWM(0,servoMin)
  time.sleep(1)
  pwm.setAllPWM(0,servoMax)
  time.sleep(1)
```

### 驱动直流电机

#### C++代码

```C++
#include "Emakefun_MotorShield.h"

int main () {
	Emakefun_MotorShield Pwm = Emakefun_MotorShield();
	Pwm.begin(50);
	Emakefun_DCMotor *DCmotor1 = Pwm.getMotor(1);
	Emakefun_DCMotor *DCmotor2 = Pwm.getMotor(2);

	DCmotor1->setSpeed(255);
	DCmotor2->setSpeed(255);

	while(1) {
		DCmotor1->run(FORWARD);
		DCmotor2->run(FORWARD);
		delay(5000);
		DCmotor1->run(BACKWARD);
		DCmotor2->run(BACKWARD);
		delay(5000);
	}
}
```
#### Python代码

``` Python
#!/usr/bin/python
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

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
myMotor = mh.getMotor(3)

# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.setSpeed(150)
myMotor.run(Raspi_MotorHAT.FORWARD);
# turn on motor
myMotor.run(Raspi_MotorHAT.RELEASE);


while (True):
	print ("Forward! ")
	myMotor.run(Raspi_MotorHAT.FORWARD)

	print ("\tSpeed up...")
	for i in range(255):
		myMotor.setSpeed(i)
		time.sleep(0.01)

	print ("\tSlow down...")
	for i in reversed(range(255)):
		myMotor.setSpeed(i)
		time.sleep(0.01)

	print ("Backward! ")
	myMotor.run(Raspi_MotorHAT.BACKWARD)

	print ("\tSpeed up...")
	for i in range(255):
		myMotor.setSpeed(i)
		time.sleep(0.01)

	print ("\tSlow down...")
	for i in reversed(range(255)):
		myMotor.setSpeed(i)
		time.sleep(0.01)

	print ("Release")
	myMotor.run(Raspi_MotorHAT.RELEASE)
	time.sleep(1.0)

```



### 驱动步进电机

#### C++代码

``` c++
#include "Emakefun_MotorShield.h"

int main () {
	Emakefun_MotorShield Pwm = Emakefun_MotorShield();
	Pwm.begin(50);
	Emakefun_StepperMotor *StepperMotor1 = Pwm.getStepper(200, 1);

	while(1) {
		StepperMotor1->setSpeed(30);
		StepperMotor1->step(100, BACKWARD,SINGLE);
	}
}
```
#### Python代码

``` python
#!/usr/bin/python
#import Raspi_MotorHAT, Raspi_DCMotor, Raspi_Stepper 
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor, Raspi_StepperMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(0x6F)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

myStepper = mh.getStepper(200, 1)  	# 200 steps/rev, motor port #1
myStepper.setSpeed(30)  		# 30 RPM

while (True):
	print("Single coil steps")
	myStepper.step(100, Raspi_MotorHAT.FORWARD,  Raspi_MotorHAT.SINGLE)
	myStepper.step(100, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.SINGLE)

	print("Double coil steps")
	myStepper.step(100, Raspi_MotorHAT.FORWARD,  Raspi_MotorHAT.DOUBLE)
	myStepper.step(100, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.DOUBLE)

	print("Interleaved coil steps")
	myStepper.step(100, Raspi_MotorHAT.FORWARD,  Raspi_MotorHAT.INTERLEAVE)
	myStepper.step(100, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.INTERLEAVE)

	print("Microsteps")
	myStepper.step(100, Raspi_MotorHAT.FORWARD,  Raspi_MotorHAT.MICROSTEP)
	myStepper.step(100, Raspi_MotorHAT.BACKWARD, Raspi_MotorHAT.MICROSTEP)

```









