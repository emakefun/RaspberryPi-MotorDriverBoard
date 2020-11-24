#include "Emakefun_MotorShield.h"

int main () {
	Emakefun_MotorShield Pwm = Emakefun_MotorShield();
	Pwm.begin(50);
	Emakefun_DCMotor *DCmotor1 = Pwm.getMotor(1);
	Emakefun_DCMotor *DCmotor2 = Pwm.getMotor(2);

	DCmotor1->setSpeed(255);
	DCmotor2->setSpeed(255);

	while(1) {
		DCmotor1->run(FORWARD);
		DCmotor2->run(FORWARD);
		delay(5000);
		DCmotor1->run(BACKWARD);
		DCmotor2->run(BACKWARD);
		delay(5000);
	}
}