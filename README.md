



# RaspberryPi Motor Driver Board

[English](README.md) 中文版

RaspberryPi 多功能电机驱动扩展板由[深圳市易创空间科技有限公司](http://www.emakefun.com)出品的一款全功能的机器人电机驱动扩展版，适用于Raspberry Pi Zero/Zero W/Zero WH/A+/B+/2B/3B/3B+/4B。能够同时支持多路电机/步进电机/舵机/编码电机(Stepper/Motor/Servo/Encoder)，空出摄像头和DIP显示屏排线接口，并且可以多板层叠使用扩展出更多的控制接口，特别适合玩家DIY机器人,智能小车,机械手臂,智能云台等各种应用。控制接口简单采用I2C接口，兼容3.3V/5V电平。



[RaspberryPi-MotorDriveBoard](https://github.com/emakefun/RaspberryPi-MotorDriveBoard/blob/master/RaspberryPi-MotorDriveBoard.jpg)


## 特点

- 双电源供电，5.5 ~ 2.1mmDC头或者3.5mm接线柱，供电电压6 ~ 25V，内置DC-DC稳压电路，为Raspberry Pi供电电流可达3A
- 驱动板IIC地址为0x60，地址可以由背面三个电阻决定
- 12位分辨率，可调PWM频率高达1.6KHz，可配置的推挽或开漏输出
- 支持同时驱动8路舵，3Pin(黑红蓝GVS)标准接口接线，方便连接舵机，舵机电源可切换到外部独立供电
- 支持4路6~24V直流电机，PH2.0接口或者3.5mm接线柱，电机单路输出高达电流3A 
- 支持同时驱动2路4线步进电机
- 板载无源蜂鸣器，板载红外接收头
- 主板预留2个IIC扩展接口，1个串口接口

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









