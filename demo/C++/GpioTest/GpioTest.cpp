#include "Emakefun_MotorShield.h"

int S1 = 8;
int S2 = 9;
int S3 = 10;
int S4 = 11;
int S5 = 12;
int S6 = 13;
int S7 = 14;
int S8 = 15;

int main() {
  Emakefun_MotorShield gpio = Emakefun_MotorShield();
  gpio.begin(1000);

  while (1) {
    gpio->setPin(S1, 1)
    delay(1000);
    gpio->setPin(S1, 0)
    delay(1000);
  }
}