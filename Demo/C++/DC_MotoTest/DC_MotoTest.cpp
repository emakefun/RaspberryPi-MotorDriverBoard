#include "Emakefun_MotorShield.h"

int main() {
  Emakefun_MotorShield Pwm = Emakefun_MotorShield();
  Pwm.begin(50);
  Emakefun_DCMotor *DCmotor1 = Pwm.getMotor(1);
  Emakefun_DCMotor *DCmotor2 = Pwm.getMotor(2);
  Emakefun_DCMotor *DCmotor3 = Pwm.getMotor(3);
  Emakefun_DCMotor *DCmotor4 = Pwm.getMotor(4);

  DCmotor1->setSpeed(255);
  DCmotor2->setSpeed(255);
  DCmotor3->setSpeed(255);
  DCmotor4->setSpeed(255);

  while (1) {
    DCmotor1->run(FORWARD);
    DCmotor2->run(FORWARD);
    DCmotor3->run(FORWARD);
    DCmotor4->run(FORWARD);
    delay(1000);
    DCmotor1->run(BACKWARD);
    DCmotor2->run(BACKWARD);
    DCmotor3->run(BACKWARD);
    DCmotor4->run(BACKWARD);
    delay(1000);
  }
}