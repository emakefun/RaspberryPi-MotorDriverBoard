#include "Emakefun_MotorShield.h"

int main() {
  Emakefun_MotorShield Pwm;
  Emakefun_StepperMotor *StepperMotor_1 = Pwm.getStepper(200, 1);
  Emakefun_StepperMotor *StepperMotor_2 = Pwm.getStepper(200, 2);
  Pwm.begin(1600);
  StepperMotor_1->setSpeed(400);
  StepperMotor_2->setSpeed(400);

  while (1) {
    StepperMotor_1->step(200, FORWARD, DOUBLE);  // 电机1正转1圈 200步
    StepperMotor_1->release();
    StepperMotor_2->step(200, FORWARD, SINGLE);  // 电机2正转1圈 200步
    StepperMotor_2->release();
    delay(1000);
    StepperMotor_1->step(200, BACKWARD, DOUBLE);  // 电机1反转1圈 200步
    StepperMotor_1->release();
    StepperMotor_2->step(200, BACKWARD, SINGLE);  // 电机2反转1圈 200步
    StepperMotor_2->release();
    delay(1000);
  }
}