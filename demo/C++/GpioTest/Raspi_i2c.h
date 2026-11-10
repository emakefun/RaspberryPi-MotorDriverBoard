#ifndef Raspi_i2c_H
#define Raspi_i2c_H

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <wiringPi.h>
#include <wiringPiI2C.h>  //导入树莓派WiringPi编码I2C控制库

#include <cstdio>

class Raspi_I2C {
 public:
  Raspi_I2C() : fd_(-1), address_(0){};
  void init(uint8_t address);
  void WriteReg8(uint8_t reg, uint8_t value);
  void WriteReg16(uint8_t reg, uint16_t value);
  void WriteBit8(uint8_t value);
  uint8_t ReadReg8(uint8_t reg);
  uint16_t ReadReg16(uint8_t reg);
  uint8_t ReadBit8();
  uint32_t Write(uint8_t* data, uint32_t size);

 private:
  int fd_;
  uint8_t address_;
};

#endif