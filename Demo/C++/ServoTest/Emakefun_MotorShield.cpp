#include "Emakefun_MotorShield.h"

#if (MICROSTEPS == 8)
static const uint8_t microstepcurve[] = {0, 50, 98, 142, 180, 212, 236, 250, 255};
#elif (MICROSTEPS == 16)
static const uint8_t microstepcurve[] = {0, 25, 50, 74, 98, 120, 141, 162, 180, 197, 212, 225, 236, 244, 250, 253, 255};
#endif

Emakefun_MotorShield::Emakefun_MotorShield(uint8_t addr) {
  _addr = addr;
  _pwm = Emakefun_MotorDriver(_addr);
}

void Emakefun_MotorShield::begin(uint16_t freq) {
  _pwm.begin();
  _freq = freq;
  _pwm.setPWMFreq(_freq);  // This is the maximum PWM frequency
  for (uint8_t i = 0; i < 16; i++) {
    _pwm.setPWM(i, 0, 0);
  }
}

void Emakefun_MotorShield::setPWM(uint8_t pin, uint16_t value) {
  // printf("[%s][%d] pin:%" PRIu8 ", value: %" PRIu16 "\n", __FUNCTION__,
  //        __LINE__, pin, value);
  if (value > 4095) {
    _pwm.setPWM(pin, 4096, 0);
  } else
    _pwm.setPWM(pin, 0, value);
}
void Emakefun_MotorShield::setPin(uint8_t pin, uint8_t value) {
  // printf("[%s][%d] pin:%" PRIu8 ", value: %" PRIu16 "\n", __FUNCTION__,
  //        __LINE__, pin, value);
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
    uint8_t in1 = 0;
    uint8_t in2 = 0;
    if (num == 0) {
      in1 = 0;
      in2 = 1;
    } else if (num == 1) {
      in2 = 2;
      in1 = 3;
    } else if (num == 2) {
      in2 = 5;
      in1 = 4;
    } else if (num == 3) {
      in1 = 7;
      in2 = 6;
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
    // uint8_t pwma = 0;
    // uint8_t pwmb = 0;
    uint8_t ain1 = 0;
    uint8_t ain2 = 0;
    uint8_t bin1 = 0;
    uint8_t bin2 = 0;
    if (num == 0) {
      ain1 = 0;
      ain2 = 1;
      bin1 = 2;
      bin2 = 3;
    } else if (num == 1) {
      ain1 = 4;
      ain2 = 5;
      bin1 = 6;
      bin2 = 7;
    }
    // steppers[num].PWMApin = pwma;
    // steppers[num].PWMBpin = pwmb;
    steppers[num].AIN1pin = ain1;
    steppers[num].AIN2pin = ain2;
    steppers[num].BIN1pin = bin1;
    steppers[num].BIN2pin = bin2;
  }
  return &steppers[num];
}

Emakefun_Servo *Emakefun_MotorShield::getServo(uint8_t num) {
  uint8_t pwm_pin[8] = {8, 9, 10, 11, 12, 13, 14, 15};
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
  pulselength = 1000000;  // 1,000,000 us per second
  pulselength /= 50;      // 50 Hz
  pulselength /= 4096;    // 12 bits of resolution
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

void Emakefun_Servo::writeServo(uint8_t angle, uint8_t speed) {
  double pulse;
  if (speed == 10) {
    pulse = 0.5 + angle / 90.0;
    setServoPulse(pulse);
  } else {
    if (angle < currentAngle) {
      for (int i = currentAngle; i > angle; i--) {
        delay(4 * (10 - speed));
        pulse = 0.5 + i / 90.0;
        setServoPulse(pulse);
      }
    } else {
      for (int i = currentAngle; i < angle; i++) {
        delay(4 * (10 - speed));
        pulse = 0.5 + i / 90.0;
        setServoPulse(pulse);
      }
    }
  }
  currentAngle = angle;
}

uint8_t Emakefun_Servo::readDegrees() { return currentAngle; }

/******************************************
               MOTORS
******************************************/

Emakefun_DCMotor::Emakefun_DCMotor(void) {
  MC = NULL;
  motornum = 0;
  _speed = IN1pin = IN2pin = 0;
}

void Emakefun_DCMotor::run(uint8_t cmd) {
  MDIR = cmd;
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
Emakefun_StepperMotor::Emakefun_StepperMotor(void) { revsteps = steppernum = currentstep = 0; }

/**************************************************************************/
/*!
    @brief  Set the delay for the Stepper Motor speed in RPM
    @param  rpm The desired RPM, we will do our best to reach it!
*/
/**************************************************************************/
// 设定一分钟旋转的圈速
void Emakefun_StepperMotor::setSpeed(uint16_t rpm) {
  // Serial.println("steps per rev: "); Serial.println(revsteps);
  // Serial.println("RPM: "); Serial.println(rpm);

  usperstep = 60000000 / ((uint32_t)revsteps * (uint32_t)rpm);
}

/**************************************************************************/
/*!
    @brief  Release all pins of the stepper motor so it free-spins
*/
/**************************************************************************/
void Emakefun_StepperMotor::release(void) {
  MC->setPin(AIN1pin, 0);
  MC->setPin(AIN2pin, 0);
  MC->setPin(BIN1pin, 0);
  MC->setPin(BIN2pin, 0);
}

/**************************************************************************/
/*!
    @brief  Move the stepper motor with the given RPM speed, don't forget to
   call
    {@link Emakefun_StepperMotor.setSpeed} to set the speed!
    @param  steps The number of steps we want to move
    @param  dir The direction to go, can be FORWARD or BACKWARD
    @param  style How to perform each step, can be SINGLE, DOUBLE, INTERLEAVE or
   MICROSTEP
*/
/**************************************************************************/

void Emakefun_StepperMotor::step(uint16_t steps, uint8_t dir, uint8_t style) {
  uint32_t uspers = usperstep;
  // uint8_t ret = 0;
  if (style == INTERLEAVE) {
    uspers /= 2;
  } else if (style == MICROSTEP) {
    uspers /= MICROSTEPS;
    steps *= MICROSTEPS;
#ifdef MOTORDEBUG
    Serial.print("steps = ");
    Serial.println(steps, DEC);
#endif
  }
  // uint64_t time = CurrentTimeMs();
  while (steps--) {
    // Serial.println("step!"); Serial.println(uspers);
    // time = CurrentTimeMs();
    onestep(dir, style);
    // usleep(uspers);
    // LOG();
    // printf("dir:%" PRIu8 ", time:%" PRIu64 ", steps:%" PRIu16 ", uspers:%" PRIu32 "\n", dir, CurrentTimeMs() - time, steps,
    // uspers);
    delayMicroseconds(uspers);
    // yield(); // required for ESP8266
  }
}

/**************************************************************************/
/*!
    @brief  Move the stepper motor one step only, with no delays
    @param  dir The direction to go, can be FORWARD or BACKWARD
    @param  style How to perform each step, can be SINGLE, DOUBLE, INTERLEAVE or
   MICROSTEP
    @returns The current step/microstep index, useful for
   Emakefun_StepperMotor.step to keep track of the current location, especially
   when microstepping
*/
/**************************************************************************/
uint8_t chang_state = 0xF;
uint8_t chang_interleave_arr[8] = {4, 1, 8, 2, 1, 4, 2, 8};

uint8_t Emakefun_StepperMotor::onestep(uint8_t dir, uint8_t style) {
  // uint8_t a, b, c, d;
  // uint8_t ocrb, ocra;

  // ocra = ocrb = 255;

  // next determine what sort of stepping procedure we're up to
  if (style == SINGLE) {
    if ((currentstep / (MICROSTEPS / 2)) % 2) {  // we're at an odd step, weird
      if (dir == FORWARD) {
        currentstep += MICROSTEPS / 2;
      } else {
        currentstep -= MICROSTEPS / 2;
      }
    } else {  // go to the next even step
      if (dir == FORWARD) {
        currentstep += MICROSTEPS;
      } else {
        currentstep -= MICROSTEPS;
      }
    }
  } else if (style == DOUBLE) {
    if (!(currentstep / (MICROSTEPS / 2) % 2)) {  // we're at an even step, weird
      if (dir == FORWARD) {
        currentstep += MICROSTEPS / 2;
      } else {
        currentstep -= MICROSTEPS / 2;
      }
    } else {  // go to the next odd step
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

    // ocra = ocrb = 0;
    // if ((currentstep >= 0) && (currentstep < MICROSTEPS)) {
    //   ocra = microstepcurve[MICROSTEPS - currentstep];
    //   ocrb = microstepcurve[currentstep];
    // } else if ((currentstep >= MICROSTEPS) && (currentstep < MICROSTEPS * 2)) {
    //   ocra = microstepcurve[currentstep - MICROSTEPS];
    //   ocrb = microstepcurve[MICROSTEPS * 2 - currentstep];
    // } else if ((currentstep >= MICROSTEPS * 2) && (currentstep < MICROSTEPS * 3)) {
    //   ocra = microstepcurve[MICROSTEPS * 3 - currentstep];
    //   ocrb = microstepcurve[currentstep - MICROSTEPS * 2];
    // } else if ((currentstep >= MICROSTEPS * 3) && (currentstep < MICROSTEPS * 4)) {
    //   ocra = microstepcurve[currentstep - MICROSTEPS * 3];
    //   ocrb = microstepcurve[MICROSTEPS * 4 - currentstep];
    // }
  }
  currentstep += MICROSTEPS * 4;
  currentstep %= MICROSTEPS * 4;
#ifdef MOTORDEBUG
  Serial.print("current step: ");
  Serial.println(currentstep, DEC);
  Serial.print(" pwmA = ");
  Serial.print(ocra, DEC);
  Serial.print(" pwmB = ");
  Serial.println(ocrb, DEC);
#endif

  // release all
  uint8_t latch_state = 0, stp = 0;
  ;  // all motor pins to 0
  // Serial.println(step, DEC);
  if (style == MICROSTEP) {
    if ((currentstep >= 0) && (currentstep < MICROSTEPS)) latch_state |= 0x03;
    if ((currentstep >= MICROSTEPS) && (currentstep < MICROSTEPS * 2)) latch_state |= 0x06;
    if ((currentstep >= MICROSTEPS * 2) && (currentstep < MICROSTEPS * 3)) latch_state |= 0x0C;
    if ((currentstep >= MICROSTEPS * 3) && (currentstep < MICROSTEPS * 4)) latch_state |= 0x09;
  } else {
    stp = currentstep / (MICROSTEPS / 2);
    switch (stp) {
      case 0:
        latch_state |= 0x1;  // energize coil 1 only
        chang_state = 0xc;
        break;
      case 1:
        latch_state |= 0x3;  // energize coil 1+2
        chang_state = 0x4;
        break;
      case 2:
        latch_state |= 0x2;  // energize coil 2 only
        chang_state = 0x08;
        break;
      case 3:
        latch_state |= 0x6;  // energize coil 2+3
        chang_state = 0x8;
        break;
      case 4:
        latch_state |= 0x4;  // energize coil 3 only
        chang_state = 0x03;
        break;
      case 5:
        latch_state |= 0xC;  // energize coil 3+4
        chang_state = 0x5;
        break;
      case 6:
        latch_state |= 0x8;  // energize coil 4 only
        chang_state = 0x06;
        break;
      case 7:
        latch_state |= 0x9;  // energize coil 1+4
        chang_state = 0xA;
        break;
    }
    if (style == INTERLEAVE) {
      chang_state = chang_interleave_arr[stp];
    }
  }
#ifdef MOTORDEBUG
  Serial.print("chang_state: 0x");
  Serial.println(chang_state, HEX);
  Serial.print("Latch: 0x");
  Serial.println(latch_state, HEX);
#endif
F1_LOOP:
  if (chang_state & 0x1) {
    if (latch_state & 0x2) {
      // Serial.println("AIN1 1");
      MC->setPWM(AIN1pin, 4096);
    } else {
      // Serial.println("AIN1 0");
      MC->setPin(AIN1pin, 0);
    }
  }
  if (chang_state & 0x2) {
    if (latch_state & 0x4) {
      // Serial.println("BIN1 1");
      MC->setPWM(BIN1pin, 4096);
    } else {
      // Serial.println("BIN1 0");
      MC->setPin(BIN1pin, 0);
    }
  }
  if (chang_state & 0x4) {
    if (latch_state & 0x8) {
      // Serial.println("AIN2 1");
      MC->setPWM(AIN2pin, 4096);
    } else {
      // Serial.println("AIN2 0");
      MC->setPin(AIN2pin, 0);
      if (style == DOUBLE) {
        chang_state = 1;
        goto F1_LOOP;
      }
    }
  }
  if (chang_state & 0x8) {
    if (latch_state & 0x1) {
      // Serial.println("BIN2 1");
      MC->setPWM(BIN2pin, 4096);
    } else {
      // Serial.println("BIN2 0");
      MC->setPin(BIN2pin, 0);
      if (style == SINGLE) {
        chang_state = 1;
        goto F1_LOOP;
      } else if (style == DOUBLE) {
        chang_state = 2;
        goto F1_LOOP;
      }
    }
  }
  return currentstep;
}