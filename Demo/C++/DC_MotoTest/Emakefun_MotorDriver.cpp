#include "Emakefun_MotorDriver.h"

Emakefun_MotorDriver::Emakefun_MotorDriver(uint8_t addr) { _i2caddr = addr; }

void Emakefun_MotorDriver::begin(void) {
  Raspi_I2C::init(_i2caddr);
  reset();
}

void Emakefun_MotorDriver::reset(void) { write8(PCA9685_MODE1, 0x00); }

void Emakefun_MotorDriver::setPWMFreq(float freq) {
  // printf("Attempting to set freq :%lf \n",freq);

  // freq *= 0.9;  // Correct for overshoot in the frequency setting (see issue
  // #11).

  float prescaleval = 25000000;
  prescaleval /= 4096;
  prescaleval /= freq;
  prescaleval -= 1;
  uint8_t prescale = floor(prescaleval + 0.5);

  uint8_t oldmode = read8(PCA9685_MODE1);
  uint8_t newmode = (oldmode & 0x7F) | 0x10;  // sleep
  write8(PCA9685_MODE1, newmode);             // go to sleep
  write8(PCA9685_PRESCALE, prescale);         // set the prescaler
  write8(PCA9685_MODE1, oldmode);
  delay(5);
  write8(PCA9685_MODE1,
         oldmode | 0xa1);  //  This sets the MODE1 register to turn on auto increment.
                           // This is why the beginTransmission below was not working.
  //  Serial.print("Mode now 0x"); Serial.println(read8(PCA9685_MODE1), HEX);
}

void Emakefun_MotorDriver::setPWM(uint8_t num, uint16_t on, uint16_t off) {
  // Serial.print("Setting PWM "); Serial.print(num); Serial.print(": ");
  // Serial.print(on); Serial.print("->"); Serial.println(off);

  // write8(LED0_ON_L + (num << 2), on & 0xFF);
  // write8(LED0_ON_H + (num << 2), on >> 8);
  // write8(LED0_OFF_L + (num << 2), off & 0xFF);
  // write8(LED0_OFF_H + (num << 2), off >> 8);

  uint8_t data[] = {static_cast<uint8_t>(LED0_ON_L + (num << 2)), static_cast<uint8_t>(on & 0xFF),
                    static_cast<uint8_t>(on >> 8), static_cast<uint8_t>(off & 0xFF), static_cast<uint8_t>(off >> 8)};
  Write(data, sizeof(data));
}

uint8_t Emakefun_MotorDriver::read8(uint8_t addr) { return ReadReg8(addr); }

void Emakefun_MotorDriver::write8(uint8_t addr, uint8_t d) { WriteReg8(addr, d); }
