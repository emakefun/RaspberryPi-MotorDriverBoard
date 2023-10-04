Emakefun_MotorHAT mh = new Emakefun_MotorHAT(addr: 0x60);

mh.getMotor(1).run(Emakefun_MotorHAT.RELEASE);
mh.getMotor(2).run(Emakefun_MotorHAT.RELEASE);
mh.getMotor(3).run(Emakefun_MotorHAT.RELEASE);
mh.getMotor(4).run(Emakefun_MotorHAT.RELEASE);

var myMotor = mh.getMotor(1);

// DC_MotoTest
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

// ServoTest
var myServo = mh.getServo(1);
myServo.writeServo(90);
Thread.Sleep(5000);

myServo.writeServo(45);
Thread.Sleep(5000);

myServo.writeServo(90);
Thread.Sleep(5000);

// ServoTest
var myStepper = mh.getStepper(1);
myStepper.setSpeed(30); // 30 RPM

Console.WriteLine("Single coil steps");
myStepper.step(100, Emakefun_MotorHAT.FORWARD, Emakefun_MotorHAT.SINGLE);
myStepper.step(100, Emakefun_MotorHAT.BACKWARD, Emakefun_MotorHAT.SINGLE);


Console.WriteLine("Double coil steps");
myStepper.step(100, Emakefun_MotorHAT.FORWARD, Emakefun_MotorHAT.DOUBLE);
myStepper.step(100, Emakefun_MotorHAT.BACKWARD, Emakefun_MotorHAT.DOUBLE);


Console.WriteLine("Interleaved coil steps");
myStepper.step(100, Emakefun_MotorHAT.FORWARD, Emakefun_MotorHAT.INTERLEAVE);
myStepper.step(100, Emakefun_MotorHAT.BACKWARD, Emakefun_MotorHAT.INTERLEAVE);


Console.WriteLine("Microsteps");
myStepper.step(100, Emakefun_MotorHAT.FORWARD, Emakefun_MotorHAT.MICROSTEP);
myStepper.step(100, Emakefun_MotorHAT.BACKWARD, Emakefun_MotorHAT.MICROSTEP);