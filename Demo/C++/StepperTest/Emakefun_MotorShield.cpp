#include "Emakefun_MotorShield.h"

#if (MICROSTEPS == 8)
uint8_t microstepcurve[] = {0, 50, 98, 142, 180, 212, 236, 250, 255};
#elif (MICROSTEPS == 16)
uint8_t microstepcurve[] = {0, 25, 50, 74, 98, 120, 141, 162, 180, 197, 212, 225, 236, 244, 250, 253, 255};
#endif

Emakefun_MotorShield::Emakefun_MotorShield(uint8_t addr) {
  _addr = addr;
  _pwm = Emakefun_MotorDriver(_addr);
}

void Emakefun_MotorShield::begin(uint16_t freq) {
  _pwm.begin();
  _freq = freq;
  _pwm.setPWMFreq(_freq);  // This is the maximum PWM frequency
  for (uint8_t i = 0; i < 16; i++)
    _pwm.setPWM(i, 0, 0);
}

void Emakefun_MotorShield::setPWM(uint8_t pin, uint16_t value) {
  if (value > 4095) {
    _pwm.setPWM(pin, 4096, 0);
  } else
    _pwm.setPWM(pin, 0, value);
}
void Emakefun_MotorShield::setPin(uint8_t pin, uint8_t value) {
  if (value == 0)
    _pwm.setPWM(pin, 0, 0);
  else
    _pwm.setPWM(pin, 4096, 0);
}

Emakefun_DCMotor *Emakefun_MotorShield::getMotor(uint8_t num) {
  if (num > 4) return NULL;

  num--;

  if (dcmotors[num].motornum == 0) {
    dcmotors[num].motornum = num;
    dcmotors[num].MC = this;
    uint8_t in1, in2;
    if (num == 0) {
      in2 = 13; in1 = 11;      
    } else if (num == 1) {
      in2 = 8; in1 = 10;
    } else if (num == 2) {
      in2 = 4; in1 = 2;
    } else if (num == 3) {
      in2 = 7; in1 = 5;
    } 
//    dcmotors[num].PWMpin = pwm;
    dcmotors[num].IN1pin = in1;
    dcmotors[num].IN2pin = in2;
  }
  return &dcmotors[num];
}


Emakefun_StepperMotor *Emakefun_MotorShield::getStepper(uint16_t steps, uint8_t num) {
  if (num > 2) return NULL;

  num--;

  if (steppers[num].steppernum == 0) {
    steppers[num].steppernum = num;
    steppers[num].revsteps = steps;
    steppers[num].MC = this;
    uint8_t pwma, pwmb, ain1, ain2, bin1, bin2;
    if (num == 0) {
      ain1 = 11; ain2 = 13; 
      bin1 = 8;  bin2 = 10;
    } else if (num == 1) {
      ain1 = 4;  ain2 = 2; 
      bin1 = 7;  bin2 = 5;
    }
    steppers[num].PWMApin = pwma;
    steppers[num].PWMBpin = pwmb;
    steppers[num].AIN1pin = ain1;
    steppers[num].AIN2pin = ain2;
    steppers[num].BIN1pin = bin1;
    steppers[num].BIN2pin = bin2;
  }
  return &steppers[num];
}

Emakefun_Servo *Emakefun_MotorShield::getServo(uint8_t num) {
  uint8_t pwm_pin[8] = {0, 1, 14, 15, 9, 12, 3, 6};
  if (num > 8) return NULL;
  if (servos[num].servonum == 0) {
    servos[num].servonum = num;
    servos[num].MC = this;
    servos[num].PWMpin = pwm_pin[num - 1];
    servos[num].PWMfreq = _freq;
  }
  return &servos[num];
}

/******************************************
               SERVOS
******************************************/

Emakefun_Servo::Emakefun_Servo(void) {
  MC = NULL;
  servonum = 0;
  PWMpin = 0;
  currentAngle = 0;
}

void Emakefun_Servo::setServoPulse(double pulse) {
  double pulselength;
  pulselength = 1000000;   // 1,000,000 us per second
  pulselength /= 50;   // 50 Hz
  pulselength /= 4096;  // 12 bits of resolution
  pulse *= 1000;
  pulse /= pulselength;
  MC->setPWM(PWMpin, pulse);
}
void Emakefun_Servo::writeServo(uint8_t angle) {
  double pulse;
  pulse = 0.5 + angle / 90.0;
  setServoPulse(pulse);
  currentAngle = angle;
}

uint8_t Emakefun_Servo::readDegrees() {
  return currentAngle;
}

/******************************************
               MOTORS
******************************************/

Emakefun_DCMotor::Emakefun_DCMotor(void) {
  MC = NULL;
  motornum = 0;
  _speed = IN1pin = IN2pin = 0;
}

void Emakefun_DCMotor::run(uint8_t cmd) {
  MDIR=cmd;
  switch (cmd) {
    case FORWARD:
      MC->setPin(IN2pin, 0);  // take 0 first to avoid 'break'
      MC->setPWM(IN1pin, _speed * 16);
      break;
    case BACKWARD:
      MC->setPin(IN1pin, 0);  // take 0 first to avoid 'break'
      MC->setPWM(IN2pin, _speed * 16);
      break;
    case RELEASE:
      MC->setPin(IN1pin, 0);
      MC->setPin(IN2pin, 0);
      break;
    case BRAKE:
      MC->setPin(IN1pin, 1);
      MC->setPin(IN2pin, 1);
      break;
  }
}

void Emakefun_DCMotor::setSpeed(uint8_t speed) {
  _speed = speed;
  run(MDIR);
}

/******************************************
               STEPPERS
******************************************/

Emakefun_StepperMotor::Emakefun_StepperMotor(void) {
  revsteps = steppernum = currentstep = 0;
}


void Emakefun_StepperMotor::setSpeed(uint16_t rpm) {
  usperstep = 50000000 / ((uint32_t)revsteps * (uint32_t)rpm);
}

void Emakefun_StepperMotor::release(void) {
  MC->setPin(AIN1pin, 0);
  MC->setPin(AIN2pin, 0);
  MC->setPin(BIN1pin, 0);
  MC->setPin(BIN2pin, 0);
  MC->setPWM(PWMApin, 0);
  MC->setPWM(PWMBpin, 0);
}

void Emakefun_StepperMotor::step(uint16_t steps, uint8_t dir,  uint8_t style) {
  uint32_t uspers = usperstep;
  uint8_t ret = 0;
  if (style == INTERLEAVE) {
    uspers /= 2;
  }
  else if (style == MICROSTEP) {
    uspers /= MICROSTEPS;
    steps *= MICROSTEPS;
  }

  while (steps--) {
    ret = onestep(dir, style);
    delayMicroseconds(uspers);
  }
}

uint8_t Emakefun_StepperMotor::onestep(uint8_t dir, uint8_t style) {
  uint8_t a, b, c, d;
  uint8_t ocrb, ocra;

  ocra = ocrb = 255;

  // next determine what sort of stepping procedure we're up to
  if (style == SINGLE) {
    if ((currentstep / (MICROSTEPS / 2)) % 2) { // we're at an odd step, weird
      if (dir == FORWARD) {
        currentstep += MICROSTEPS / 2;
      }
      else {
        currentstep -= MICROSTEPS / 2;
      }
    } else {           // go to the next even step
      if (dir == FORWARD) {
        currentstep += MICROSTEPS;
      }
      else {
        currentstep -= MICROSTEPS;
      }
    }
  } else if (style == DOUBLE) {
    if (! (currentstep / (MICROSTEPS / 2) % 2)) { // we're at an even step, weird
      if (dir == FORWARD) {
        currentstep += MICROSTEPS / 2;
      } else {
        currentstep -= MICROSTEPS / 2;
      }
    } else {           // go to the next odd step
      if (dir == FORWARD) {
        currentstep += MICROSTEPS;
      } else {
        currentstep -= MICROSTEPS;
      }
    }
  } else if (style == INTERLEAVE) {
    if (dir == FORWARD) {
      currentstep += MICROSTEPS / 2;
    } else {
      currentstep -= MICROSTEPS / 2;
    }
  }
  if (style == MICROSTEP) {
    if (dir == FORWARD) {
      currentstep++;
    } else {
      // BACKWARDS
      currentstep--;
    }
    currentstep += MICROSTEPS * 4;
    currentstep %= MICROSTEPS * 4;

    ocra = ocrb = 0;
    if ( (currentstep >= 0) && (currentstep < MICROSTEPS)) {
      ocra = microstepcurve[MICROSTEPS - currentstep];
      ocrb = microstepcurve[currentstep];
    } else if  ( (currentstep >= MICROSTEPS) && (currentstep < MICROSTEPS * 2)) {
      ocra = microstepcurve[currentstep - MICROSTEPS];
      ocrb = microstepcurve[MICROSTEPS * 2 - currentstep];
    } else if  ( (currentstep >= MICROSTEPS * 2) && (currentstep < MICROSTEPS * 3)) {
      ocra = microstepcurve[MICROSTEPS * 3 - currentstep];
      ocrb = microstepcurve[currentstep - MICROSTEPS * 2];
    } else if  ( (currentstep >= MICROSTEPS * 3) && (currentstep < MICROSTEPS * 4)) {
      ocra = microstepcurve[currentstep - MICROSTEPS * 3];
      ocrb = microstepcurve[MICROSTEPS * 4 - currentstep];
    }
  }
  currentstep += MICROSTEPS * 4;
  currentstep %= MICROSTEPS * 4;

//  if (MC->_version != 5) {
//    MC->setPWM(PWMApin, ocra * 16);
//    MC->setPWM(PWMBpin, ocrb * 16);
//  }
  // release all
  uint8_t latch_state = 0; // all motor pins to 0
  //Serial.println(step, DEC);
  if (style == MICROSTEP) {
    if ((currentstep >= 0) && (currentstep < MICROSTEPS))
      latch_state |= 0x03;
    if ((currentstep >= MICROSTEPS) && (currentstep < MICROSTEPS * 2))
      latch_state |= 0x06;
    if ((currentstep >= MICROSTEPS * 2) && (currentstep < MICROSTEPS * 3))
      latch_state |= 0x0C;
    if ((currentstep >= MICROSTEPS * 3) && (currentstep < MICROSTEPS * 4))
      latch_state |= 0x09;
  } else {
    switch (currentstep / (MICROSTEPS / 2)) {
      case 0:
        latch_state |= 0x1; // energize coil 1 only
        break;
      case 1:
        latch_state |= 0x3; // energize coil 1+2
        break;
      case 2:
        latch_state |= 0x2; // energize coil 2 only
        break;
      case 3:
        latch_state |= 0x6; // energize coil 2+3
        break;
      case 4:
        latch_state |= 0x4; // energize coil 3 only
        break;
      case 5:
        latch_state |= 0xC; // energize coil 3+4
        break;
      case 6:
        latch_state |= 0x8; // energize coil 4 only
        break;
      case 7:
        latch_state |= 0x9; // energize coil 1+4
        break;
    }
  }

    if (latch_state & 0x1) {
      MC->setPin(AIN2pin, LOW);
    } else {
      MC->setPWM(AIN2pin, ocra * 16);
    }
    if (latch_state & 0x2) {
      MC->setPin(BIN1pin, LOW);
    } else {
      MC->setPWM(BIN1pin, ocrb * 16);
    }
    if (latch_state & 0x4) {
      MC->setPin(AIN1pin, LOW);
    } else {
      MC->setPWM(AIN1pin, ocra * 16);
    }
    if (latch_state & 0x8) {
      MC->setPin(BIN2pin, LOW);
    } else {
      MC->setPWM(BIN2pin, ocrb * 16);
    }
  return currentstep;
}
