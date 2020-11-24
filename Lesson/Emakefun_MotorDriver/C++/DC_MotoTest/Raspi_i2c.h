#ifndef Raspi_i2c_H
#define Raspi_i2c_H

#include <wiringPi.h>
#include <wiringPiI2C.h>//导入树莓派WiringPi编码I2C控制库
#include <stdint.h>
#include <stdio.h>
#include <cstdio>
#include <math.h>
class Raspi_I2C 
{
	public:
		int fd;
		uint8_t address;
		void init(uint8_t address);
		void WriteReg8(uint8_t reg, uint8_t value);
		void WriteReg16(uint8_t reg, uint16_t value);
		void WriteBit8(uint8_t value);
		uint8_t ReadReg8(uint8_t reg);
		uint16_t ReadReg16(uint8_t reg);
		uint8_t ReadBit8();
};

#endif