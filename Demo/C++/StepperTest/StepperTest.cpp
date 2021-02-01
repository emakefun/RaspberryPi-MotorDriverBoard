#include "Emakefun_MotorShield.h"

int main () {
	Emakefun_MotorShield Pwm = Emakefun_MotorShield();
	Pwm.begin(50);
	Emakefun_StepperMotor *StepperMotor1 = Pwm.getStepper(200, 1);
	StepperMotor1->setSpeed(200);
	while(1) {
		StepperMotor1->step(200, BACKWARD,SINGLE);
	}
}