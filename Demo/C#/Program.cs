Emakefun_MotorHAT mh = new Emakefun_MotorHAT(addr: 0x60);

mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE);
mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE);
mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE);
mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE);

var myMotor = mh.getMotor(1);

while (true)
{
    myMotor.setSpeed(50);
    myMotor.run(Emakefun_MotorHAT.FORWARD);
    Thread.Sleep(5000);

    myMotor.run(Emakefun_MotorHAT.RELEASE);
    Thread.Sleep(5000);

    myMotor.setSpeed(150);
    myMotor.run(Emakefun_MotorHAT.BACKWARD);
    Thread.Sleep(5000);

    myMotor.setSpeed(50);
    myMotor.run(Emakefun_MotorHAT.RELEASE);
}