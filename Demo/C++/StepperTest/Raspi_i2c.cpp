#include "Raspi_i2c.h"

#include <unistd.h>
/*******************************************************
**函数名：
**参数：
**功能：
********************************************************/
void Raspi_I2C::init(uint8_t address) {
  address_ = address;
  fd_ = wiringPiI2CSetup(address_);
  // printf("%d \n",fd);
  if (fd_ == -1) {
    printf("Error accessing 0x%02X: Check your I2C address \n", address);
  }
}
/*******************************************************
**函数名：
**参数：
**功能：
********************************************************/
void Raspi_I2C::WriteReg8(uint8_t reg, uint8_t value) {
  //"Writes an 8-bit value to the specified register/address"
  wiringPiI2CWriteReg8(fd_, reg, value);
}

/*******************************************************
**函数名：
**参数：
**功能：
********************************************************/
void Raspi_I2C::WriteReg16(uint8_t reg, uint16_t value) {
  //"Writes a 16-bit value to the specified register/address pair"
  wiringPiI2CWriteReg16(fd_, reg, value);
}

/*******************************************************
**函数名：
**参数：
**功能：
********************************************************/
void Raspi_I2C::WriteBit8(uint8_t value) {
  //"Writes an 8-bit value the I2C device"
  wiringPiI2CWrite(fd_, value);
}

/*******************************************************
**函数名：
**参数：
**功能：
********************************************************/
uint8_t Raspi_I2C::ReadReg8(uint8_t reg) {
  //"Read an unsigned byte from the specified register/address"
  uint8_t value;
  value = wiringPiI2CReadReg8(fd_, reg);
  // printf("Read value %d \n",value);
  return value;
}

/*******************************************************
**函数名：
**参数：
**功能：
********************************************************/
uint16_t Raspi_I2C::ReadReg16(uint8_t reg) {
  //"Writes an 16-bit value to the specified register/address"
  uint16_t value;
  value = wiringPiI2CReadReg16(fd_, reg);
  // printf("Read value %d \n", value);
  return value;
}

/*******************************************************
**函数名：
**参数：
**功能：
********************************************************/
uint8_t Raspi_I2C::ReadBit8() {
  //"Read an unsigned byte from the I2C device"
  uint32_t value;
  value = wiringPiI2CRead(fd_);
  // printf("Read value %d \n", value);
  return value;
}

uint32_t Raspi_I2C::Write(uint8_t* data, uint32_t size) { return write(fd_, data, size); }