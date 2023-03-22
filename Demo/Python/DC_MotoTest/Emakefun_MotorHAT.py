#!/usr/bin/python

from Emakefun_MotorDriver import PWM
import time

class Emakefun_StepperMotor:
	MICROSTEPS = 8
	MICROSTEP_CURVE = [0, 50, 98, 142, 180, 212, 236, 250, 255]

	#MICROSTEPS = 16
	# a sinusoidal curve NOT LINEAR!
	#MICROSTEP_CURVE = [0, 25, 50, 74, 98, 120, 141, 162, 180, 197, 212, 225, 236, 244, 250, 253, 255]
	
	def __init__(self, controller, num, steps=200):
		self.MC = controller
		self.revsteps = steps
		self.motornum = num
		self.sec_per_step = 0.1
		self.steppingcounter = 0
		self.currentstep = 0

		num -= 1

		if (num == 0):
			#self.PWMA = 8
			self.AIN2 = 13
			self.AIN1 = 11
			#self.PWMB = 13
			self.BIN2 = 10
			self.BIN1 = 8
		elif (num == 1):
			#self.PWMA = 2
			self.AIN2 = 2
			self.AIN1 = 4
			#self.PWMB = 7
			self.BIN2 = 5
			self.BIN1 = 7
		else:
			raise NameError('MotorHAT Stepper must be between 1 and 2 inclusive')

	def setSpeed(self, rpm):
		self.sec_per_step = 60.0 / (self.revsteps * rpm)
		self.steppingcounter = 0

	def oneStep(self, dir, style):
		pwm_a = pwm_b = 255

		# first determine what sort of stepping procedure we're up to
		if (style == Emakefun_MotorHAT.SINGLE):
				if ((self.currentstep/(self.MICROSTEPS/2)) % 2):
				# we're at an odd step, weird
					if (dir == Emakefun_MotorHAT.FORWARD):
						self.currentstep += self.MICROSTEPS/2
					else:
						self.currentstep -= self.MICROSTEPS/2
		else:
				# go to next even step
				if (dir == Emakefun_MotorHAT.FORWARD):
					self.currentstep += self.MICROSTEPS
				else:
					self.currentstep -= self.MICROSTEPS
		if (style == Emakefun_MotorHAT.DOUBLE):
			if not (self.currentstep/(self.MICROSTEPS/2) % 2):
				# we're at an even step, weird
				if (dir == Emakefun_MotorHAT.FORWARD):
					self.currentstep += self.MICROSTEPS/2
				else:
					self.currentstep -= self.MICROSTEPS/2
			else:
				# go to next odd step
				if (dir == Emakefun_MotorHAT.FORWARD):
					self.currentstep += self.MICROSTEPS
				else:
					self.currentstep -= self.MICROSTEPS
		if (style == Emakefun_MotorHAT.INTERLEAVE):
			if (dir == Emakefun_MotorHAT.FORWARD):
				self.currentstep += self.MICROSTEPS/2
			else:
				self.currentstep -= self.MICROSTEPS/2

		if (style == Emakefun_MotorHAT.MICROSTEP):
			if (dir == Emakefun_MotorHAT.FORWARD):
				self.currentstep += 1
			else:
				self.currentstep -= 1

				# go to next 'step' and wrap around
				self.currentstep += self.MICROSTEPS * 4
				self.currentstep %= self.MICROSTEPS * 4

				pwm_a = pwm_b = 0
			if (self.currentstep >= 0) and (self.currentstep < self.MICROSTEPS):
				pwm_a = self.MICROSTEP_CURVE[self.MICROSTEPS - self.currentstep]
				pwm_b = self.MICROSTEP_CURVE[self.currentstep]
			elif (self.currentstep >= self.MICROSTEPS) and (self.currentstep < self.MICROSTEPS*2):
				pwm_a = self.MICROSTEP_CURVE[self.currentstep - self.MICROSTEPS]
				pwm_b = self.MICROSTEP_CURVE[self.MICROSTEPS*2 - self.currentstep]
			elif (self.currentstep >= self.MICROSTEPS*2) and (self.currentstep < self.MICROSTEPS*3):
				pwm_a = self.MICROSTEP_CURVE[self.MICROSTEPS*3 - self.currentstep]
				pwm_b = self.MICROSTEP_CURVE[self.currentstep - self.MICROSTEPS*2]
			elif (self.currentstep >= self.MICROSTEPS*3) and (self.currentstep < self.MICROSTEPS*4):
				pwm_a = self.MICROSTEP_CURVE[self.currentstep - self.MICROSTEPS*3]
				pwm_b = self.MICROSTEP_CURVE[self.MICROSTEPS*4 - self.currentstep]


		# go to next 'step' and wrap around
		self.currentstep += self.MICROSTEPS * 4
		self.currentstep %= self.MICROSTEPS * 4

		# only really used for microstepping, otherwise always on!
		#self.MC._pwm.setPWM(self.PWMA, 0, pwm_a*16)
		#self.MC._pwm.setPWM(self.PWMB, 0, pwm_b*16)

		# set up coil energizing!
		coils = [0, 0, 0, 0]

		if (style == Emakefun_MotorHAT.MICROSTEP):
			if (self.currentstep >= 0) and (self.currentstep < self.MICROSTEPS):
				coils = [1, 1, 0, 0]
			elif (self.currentstep >= self.MICROSTEPS) and (self.currentstep < self.MICROSTEPS*2):
				coils = [0, 1, 1, 0]
			elif (self.currentstep >= self.MICROSTEPS*2) and (self.currentstep < self.MICROSTEPS*3):
				coils = [0, 0, 1, 1]
			elif (self.currentstep >= self.MICROSTEPS*3) and (self.currentstep < self.MICROSTEPS*4):
				coils = [1, 0, 0, 1]
		else:
			step2coils = [ 	[1, 0, 0, 0], 
				[1, 1, 0, 0],
				[0, 1, 0, 0],
				[0, 1, 1, 0],
				[0, 0, 1, 0],
				[0, 0, 1, 1],
				[0, 0, 0, 1],
				[1, 0, 0, 1] ]
			coils = step2coils[int(self.currentstep/(self.MICROSTEPS/2))]

		#print "coils state = " + str(coils)
		self.MC.setPin(self.AIN2, coils[0])
		self.MC.setPin(self.BIN1, coils[1])
		self.MC.setPin(self.AIN1, coils[2])
		self.MC.setPin(self.BIN2, coils[3])

		return self.currentstep

	def step(self, steps, direction, stepstyle):
		s_per_s = self.sec_per_step
		lateststep = 0
		
		if (stepstyle == Emakefun_MotorHAT.INTERLEAVE):
			s_per_s = s_per_s / 2.0
		if (stepstyle == Emakefun_MotorHAT.MICROSTEP):
			s_per_s /= self.MICROSTEPS
			steps *= self.MICROSTEPS
			print (s_per_s , " sec per step")

		for s in range(steps):
			lateststep = self.oneStep(direction, stepstyle)
			time.sleep(s_per_s)

		if (stepstyle == Emakefun_MotorHAT.MICROSTEP):
			# this is an edge case, if we are in between full steps, lets just keep going
			# so we end on a full step
			while (lateststep != 0) and (lateststep != self.MICROSTEPS):
				lateststep = self.oneStep(dir, stepstyle)
				time.sleep(s_per_s)
		
class Emakefun_DCMotor:
	def __init__(self, controller, num):
		self.MC = controller
		self.motornum = num
		in1 = in2 = 0
		self._speed = 0

		if (num == 0):
			in2 = 13
			in1 = 11
		elif (num == 1):
			in2 = 8
			in1 = 10
		elif (num == 2):
			in2 = 2
			in1 = 4
		elif (num == 3):
			in2 = 5
			in1 = 7
		else:
			raise NameError('MotorHAT Motor must be between 1 and 4 inclusive')
		#self.PWMpin = pwm
		self.IN1pin = in1
		self.IN2pin = in2

	def run(self, command):
		if not self.MC:
			return
		if (command == Emakefun_MotorHAT.FORWARD):
			self.MC.setPin(self.IN2pin, 0)
			self.MC.setPWM(self.IN1pin, self._speed*16)
		if (command == Emakefun_MotorHAT.BACKWARD):
			self.MC.setPin(self.IN1pin, 0)
			self.MC.setPWM(self.IN2pin, self._speed*16)
		if (command == Emakefun_MotorHAT.RELEASE):
			self.MC.setPin(self.IN1pin, 0)
			self.MC.setPin(self.IN2pin, 0)

	def setSpeed(self, speed):
		if (speed < 0):
			speed = 0
		if (speed > 255):
			speed = 255
		#self.MC._pwm.setPWM(self.PWMpin, 0, speed*16)
		self._speed = speed

class Emakefun_Servo:
  def __init__(self, controller, num):
    self.MC = controller
    self.pin = [0, 1, 14, 15, 9, 12, 3, 6]
    self.PWM_pin = self.pin[num]
    self.currentAngle = 0

  def writeServo(self, angle):
    pulse = 4096 * ((angle*11)+500) / 20000
    self.MC.setPWM(self.PWM_pin, pulse)
    self.currentAngle = angle

  def writeServoWithSpeed(self, angle, speed):
    if (speed == 10):
      pulse = 4096 * ((angle * 11) + 500) / 20000
      self.MC.setPWM(self.PWM_pin, pulse)
    else:
      if angle < self.currentAngle:
        for i in range(self.currentAngle, angle, -1):
          time.sleep(4 * (10 - speed) / 1000)
          pulse = 4096 * ((i * 11) + 500) / 20000
          self.MC.setPWM(self.PWM_pin, pulse)
      else:
        for i in range(self.currentAngle, angle, 1):
          time.sleep(4 * (10 - speed) / 1000)
          pulse = 4096 * ((i * 11) + 500) / 20000
          self.MC.setPWM(self.PWM_pin, pulse)
    self.currentAngle = angle

  def readDegrees(self):
    return self.currentAngle

class Emakefun_MotorHAT:
	FORWARD = 1
	BACKWARD = 2
	BRAKE = 3
	RELEASE = 4

	SINGLE = 1
	DOUBLE = 2
	INTERLEAVE = 3
	MICROSTEP = 4

	def __init__(self, addr = 0x60, freq = 50):
		self._i2caddr = addr            # default addr on HAT
		self._frequency = freq		# default @1600Hz PWM freq
		self.servos = [ Emakefun_Servo(self, n) for n in range(8) ]
		self.motors = [ Emakefun_DCMotor(self, m) for m in range(4) ]
		self.steppers = [ Emakefun_StepperMotor(self, 1), Emakefun_StepperMotor(self, 2) ]
		self._pwm =  PWM(addr, debug=False)
		self._pwm.setPWMFreq(self._frequency)

	def setPin(self, pin, value):
		if (pin < 0) or (pin > 15):
			raise NameError('PWM pin must be between 0 and 15 inclusive')
		if (value != 0) and (value != 1):
			raise NameError('Pin value must be 0 or 1!')
		if (value == 0):
			self._pwm.setPWM(pin, 0, 4096)
		if (value == 1):
			self._pwm.setPWM(pin, 4096, 0)

	def setPWM(self, pin, value):
		if (value > 4095):
			self._pwm.setPWM(pin, 4096, 0)
		else:
			self._pwm.setPWM(pin, 0, value)

	def getStepper(self, steps, num):
		if (num < 1) or (num > 2):
			raise NameError('MotorHAT Stepper must be between 1 and 2 inclusive')
		return self.steppers[num-1]

	def getMotor(self, num):
		if (num < 1) or (num > 4):
			raise NameError('MotorHAT Motor must be between 1 and 4 inclusive')
		return self.motors[num-1]

	def getServo(self, num):
		if (num < 1) or (num > 8):
			raise NameError('MotorHAT Motor must be between 1 and 8 inclusive')
		return self.servos[num-1]
