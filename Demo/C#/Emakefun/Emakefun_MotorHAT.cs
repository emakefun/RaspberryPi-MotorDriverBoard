using System.Data;

public class Emakefun_StepperMotor
{
    public int AIN1;

    public int AIN2;

    public int BIN1;

    public int BIN2;

    public int currentstep;

    public Emakefun_MotorHAT MC;

    public int motornum;

    public int revsteps;

    public double sec_per_step;

    public int steppingcounter;

    public int MICROSTEPS = 8;

    public List<int> MICROSTEP_CURVE = new List<int> {
            0,
            50,
            98,
            142,
            180,
            212,
            236,
            250,
            255
        };

    public Emakefun_StepperMotor(Emakefun_MotorHAT controller, int num, int steps = 200)
    {
        this.MC = controller;
        this.revsteps = steps;
        this.motornum = num;
        this.sec_per_step = 0.1;
        this.steppingcounter = 0;
        this.currentstep = 0;
        num -= 1;
        if (num == 0)
        {
            this.AIN1 = 0;
            this.AIN2 = 1;
            this.BIN1 = 2;
            this.BIN2 = 3;
        }
        else if (num == 1)
        {
            this.AIN1 = 4;
            this.AIN2 = 5;
            this.BIN1 = 6;
            this.BIN2 = 7;
        }
        else
        {
            throw new Exception("MotorHAT Stepper must be between 1 and 2 inclusive");
        }
    }

    public virtual void setSpeed(int rpm)
    {
        this.sec_per_step = 60.0 / (this.revsteps * rpm);
        this.steppingcounter = 0;
    }

    public virtual int oneStep(int dir, int style)
    {
        object pwm_b;
        var pwm_a = 255;
        // first determine what sort of stepping procedure we're up to
        if (style == Emakefun_MotorHAT.SINGLE)
        {
            if (Convert.ToBoolean(this.currentstep / (this.MICROSTEPS / 2) % 2))
            {
                // we're at an odd step, weird
                if (dir == Emakefun_MotorHAT.FORWARD)
                {
                    this.currentstep += this.MICROSTEPS / 2;
                }
                else
                {
                    this.currentstep -= this.MICROSTEPS / 2;
                }
            }
        }
        else
        {
            // go to next even step
            if (dir == Emakefun_MotorHAT.FORWARD)
            {
                this.currentstep += this.MICROSTEPS;
            }
            else
            {
                this.currentstep -= this.MICROSTEPS;
            }
        }
        if (style == Emakefun_MotorHAT.DOUBLE)
        {
            if (!Convert.ToBoolean((this.currentstep / (this.MICROSTEPS / 2) % 2)))
            {
                // we're at an even step, weird
                if (dir == Emakefun_MotorHAT.FORWARD)
                {
                    this.currentstep += this.MICROSTEPS / 2;
                }
                else
                {
                    this.currentstep -= this.MICROSTEPS / 2;
                }
            }
            else
            {
                // go to next odd step
                if (dir == Emakefun_MotorHAT.FORWARD)
                {
                    this.currentstep += this.MICROSTEPS;
                }
                else
                {
                    this.currentstep -= this.MICROSTEPS;
                }
            }
        }
        if (style == Emakefun_MotorHAT.INTERLEAVE)
        {
            if (dir == Emakefun_MotorHAT.FORWARD)
            {
                this.currentstep += this.MICROSTEPS / 2;
            }
            else
            {
                this.currentstep -= this.MICROSTEPS / 2;
            }
        }
        if (style == Emakefun_MotorHAT.MICROSTEP)
        {
            if (dir == Emakefun_MotorHAT.FORWARD)
            {
                this.currentstep += 1;
            }
            else
            {
                this.currentstep -= 1;
                // go to next 'step' and wrap around
                this.currentstep += this.MICROSTEPS * 4;
                this.currentstep %= this.MICROSTEPS * 4;
                pwm_a = 0;
            }
            if (this.currentstep >= 0 && this.currentstep < this.MICROSTEPS)
            {
                pwm_a = this.MICROSTEP_CURVE[this.MICROSTEPS - this.currentstep];
                pwm_b = this.MICROSTEP_CURVE[this.currentstep];
            }
            else if (this.currentstep >= this.MICROSTEPS && this.currentstep < this.MICROSTEPS * 2)
            {
                pwm_a = this.MICROSTEP_CURVE[this.currentstep - this.MICROSTEPS];
                pwm_b = this.MICROSTEP_CURVE[this.MICROSTEPS * 2 - this.currentstep];
            }
            else if (this.currentstep >= this.MICROSTEPS * 2 && this.currentstep < this.MICROSTEPS * 3)
            {
                pwm_a = this.MICROSTEP_CURVE[this.MICROSTEPS * 3 - this.currentstep];
                pwm_b = this.MICROSTEP_CURVE[this.currentstep - this.MICROSTEPS * 2];
            }
            else if (this.currentstep >= this.MICROSTEPS * 3 && this.currentstep < this.MICROSTEPS * 4)
            {
                pwm_a = this.MICROSTEP_CURVE[this.currentstep - this.MICROSTEPS * 3];
                pwm_b = this.MICROSTEP_CURVE[this.MICROSTEPS * 4 - this.currentstep];
            }
        }
        // go to next 'step' and wrap around
        this.currentstep += this.MICROSTEPS * 4;
        this.currentstep %= this.MICROSTEPS * 4;
        // only really used for microstepping, otherwise always on!
        //self.MC._pwm.setPWM(self.PWMA, 0, pwm_a*16)
        //self.MC._pwm.setPWM(self.PWMB, 0, pwm_b*16)
        // set up coil energizing!
        var coils = new List<int> {
                0,
                0,
                0,
                0
            };
        if (style == Emakefun_MotorHAT.MICROSTEP)
        {
            if (this.currentstep >= 0 && this.currentstep < this.MICROSTEPS)
            {
                coils = new List<int> {
                        1,
                        1,
                        0,
                        0
                    };
            }
            else if (this.currentstep >= this.MICROSTEPS && this.currentstep < this.MICROSTEPS * 2)
            {
                coils = new List<int> {
                        0,
                        1,
                        1,
                        0
                    };
            }
            else if (this.currentstep >= this.MICROSTEPS * 2 && this.currentstep < this.MICROSTEPS * 3)
            {
                coils = new List<int> {
                        0,
                        0,
                        1,
                        1
                    };
            }
            else if (this.currentstep >= this.MICROSTEPS * 3 && this.currentstep < this.MICROSTEPS * 4)
            {
                coils = new List<int> {
                        1,
                        0,
                        0,
                        1
                    };
            }
        }
        else
        {
            var step2coils = new List<List<int>> {
                    new List<int> {
                        1,
                        0,
                        0,
                        0
                    },
                    new List<int> {
                        1,
                        1,
                        0,
                        0
                    },
                    new List<int> {
                        0,
                        1,
                        0,
                        0
                    },
                    new List<int> {
                        0,
                        1,
                        1,
                        0
                    },
                    new List<int> {
                        0,
                        0,
                        1,
                        0
                    },
                    new List<int> {
                        0,
                        0,
                        1,
                        1
                    },
                    new List<int> {
                        0,
                        0,
                        0,
                        1
                    },
                    new List<int> {
                        1,
                        0,
                        0,
                        1
                    }
                };
            coils = step2coils[Convert.ToInt32(this.currentstep / (this.MICROSTEPS / 2))];
        }
        //print "coils state = " + str(coils)
        this.MC.setPin(this.AIN2, coils[0]);
        this.MC.setPin(this.BIN1, coils[1]);
        this.MC.setPin(this.AIN1, coils[2]);
        this.MC.setPin(this.BIN2, coils[3]);
        return this.currentstep;
    }

    public virtual void step(int steps, int direction, int stepstyle)
    {
        var s_per_s = this.sec_per_step;
        var lateststep = 0;
        if (stepstyle == Emakefun_MotorHAT.INTERLEAVE)
        {
            s_per_s = s_per_s / 2.0;
        }
        if (stepstyle == Emakefun_MotorHAT.MICROSTEP)
        {
            s_per_s /= this.MICROSTEPS;
            steps *= this.MICROSTEPS;
            Console.WriteLine(s_per_s.ToString(), " sec per step");
        }
        foreach (var s in Enumerable.Range(0, steps))
        {
            lateststep = this.oneStep(direction, stepstyle);
            Thread.Sleep(Convert.ToInt32(s_per_s * 1000));
        }
        if (stepstyle == Emakefun_MotorHAT.MICROSTEP)
        {
            // this is an edge case, if we are in between full steps, lets just keep going
            // so we end on a full step
            while (lateststep != 0 && lateststep != this.MICROSTEPS)
            {
                lateststep = this.oneStep(direction, stepstyle);
                Thread.Sleep(Convert.ToInt32(s_per_s * 1000));
            }
        }
    }
}

public class Emakefun_DCMotor
{
    public int _speed;

    public int IN1pin;

    public int IN2pin;

    public Emakefun_MotorHAT MC;

    public object motornum;

    public Emakefun_DCMotor(Emakefun_MotorHAT controller, int num)
    {
        int in2;
        this.MC = controller;
        this.motornum = num;
        var in1 = 0;
        this._speed = 0;
        if (num == 0)
        {
            in1 = 0;
            in2 = 1;
        }
        else if (num == 1)
        {
            in1 = 3;
            in2 = 2;
        }
        else if (num == 2)
        {
            in1 = 4;
            in2 = 5;
        }
        else if (num == 3)
        {
            in1 = 7;
            in2 = 6;
        }
        else
        {
            throw new Exception("MotorHAT Motor must be between 1 and 4 inclusive");
        }
        //self.PWMpin = pwm
        this.IN1pin = in1;
        this.IN2pin = in2;
    }

    public virtual void run(int command)
    {
        if (command == Emakefun_MotorHAT.FORWARD)
        {
            this.MC.setPin(this.IN2pin, 0);
            this.MC.setPWM(this.IN1pin, this._speed * 16);
        }
        if (command == Emakefun_MotorHAT.BACKWARD)
        {
            this.MC.setPin(this.IN1pin, 0);
            this.MC.setPWM(this.IN2pin, this._speed * 16);
        }
        if (command == Emakefun_MotorHAT.RELEASE)
        {
            this.MC.setPin(this.IN1pin, 0);
            this.MC.setPin(this.IN2pin, 0);
        }
    }

    public virtual void setSpeed(int speed)
    {
        if (speed < 0)
        {
            speed = 0;
        }
        if (speed > 255)
        {
            speed = 255;
        }
        //self.MC._pwm.setPWM(self.PWMpin, 0, speed*16)
        this._speed = speed;
    }
}

public class Emakefun_Servo
{
    public int currentAngle;

    public Emakefun_MotorHAT MC;

    public List<int> pin;

    public int PWM_pin;

    public Emakefun_Servo(Emakefun_MotorHAT controller, int num)
    {
        this.MC = controller;
        this.pin = new List<int> {
                8,
                9,
                10,
                11,
                12,
                13,
                14,
                15
            };
        this.PWM_pin = this.pin[num];
        this.currentAngle = 0;
    }

    public virtual void writeServo(int angle)
    {
        var pulse = 4096 * (angle * 11 + 500) / 20000;
        this.MC.setPWM(this.PWM_pin, pulse);
        this.currentAngle = angle;
    }

    public virtual void writeServoWithSpeed(int angle, int speed)
    {
        if (speed == 10)
        {
            var pulse = 4096 * (angle * 11 + 500) / 20000;
            this.MC.setPWM(this.PWM_pin, pulse);
        }
        else if (angle < this.currentAngle)
        {
            foreach (var i in Enumerable.Range(0, Convert.ToInt32(Math.Ceiling(Convert.ToDouble(angle - this.currentAngle) / -1))).Select(_x_1 => this.currentAngle + _x_1 * -1))
            {
                Thread.Sleep(4 * (10 - speed));
                var pulse = 4096 * (i * 11 + 500) / 20000;
                this.MC.setPWM(this.PWM_pin, pulse);
            }
        }
        else
        {
            foreach (var i in Enumerable.Range(0, Convert.ToInt32(Math.Ceiling(Convert.ToDouble(angle - this.currentAngle) / 1))).Select(_x_2 => this.currentAngle + _x_2 * 1))
            {
                Thread.Sleep(4 * (10 - speed));
                var pulse = 4096 * (i * 11 + 500) / 20000;
                this.MC.setPWM(this.PWM_pin, pulse);
            }
        }
        this.currentAngle = angle;
    }

    public virtual object readDegrees()
    {
        return this.currentAngle;
    }
}

public class Emakefun_MotorHAT
{
    public int _frequency;

    public object _i2caddr;

    public PWM _pwm;

    public List<Emakefun_DCMotor> motors;

    public List<Emakefun_Servo> servos;

    public List<Emakefun_StepperMotor> steppers;

    public static int FORWARD = 1;

    public static int BACKWARD = 2;

    public static int BRAKE = 3;

    public static int RELEASE = 4;

    public static int SINGLE = 1;

    public static int DOUBLE = 2;

    public static int INTERLEAVE = 3;

    public static int MICROSTEP = 4;

    public Emakefun_MotorHAT(byte addr = 0x60, int freq = 50)
    {
        this._i2caddr = addr;
        this._frequency = freq;
        this.servos = (from n in Enumerable.Range(0, 8)
                       select new Emakefun_Servo(this, n)).ToList();
        this.motors = (from m in Enumerable.Range(0, 4)
                       select new Emakefun_DCMotor(this, m)).ToList();
        this.steppers = new List<Emakefun_StepperMotor> {
                new Emakefun_StepperMotor(this, 1),
                new Emakefun_StepperMotor(this, 2)
            };
        this._pwm = new PWM(addr, debug: false);
        this._pwm.setPWMFreq(this._frequency);
    }

    public virtual void setPin(int pin, int value)
    {
        if (pin < 0 || pin > 15)
        {
            throw new Exception("PWM pin must be between 0 and 15 inclusive");
        }
        if (value != 0 && value != 1)
        {
            throw new Exception("Pin value must be 0 or 1!");
        }
        if (value == 0)
        {
            this._pwm.setPWM(pin, 0, 4096);
        }
        if (value == 1)
        {
            this._pwm.setPWM(pin, 4096, 0);
        }
    }

    public virtual void setPWM(int pin, int value)
    {
        if (value > 4095)
        {
            this._pwm.setPWM(pin, 4096, 0);
        }
        else
        {
            this._pwm.setPWM(pin, 0, value);
        }
    }

    public virtual Emakefun_StepperMotor getStepper(int num)
    {
        if (num < 1 || num > 2)
        {
            throw new Exception("MotorHAT Stepper must be between 1 and 2 inclusive");
        }
        return this.steppers[num - 1];
    }

    public virtual Emakefun_DCMotor getMotor(int num)
    {
        if (num < 1 || num > 4)
        {
            throw new Exception("MotorHAT Motor must be between 1 and 4 inclusive");
        }
        return this.motors[num - 1];
    }

    public virtual Emakefun_Servo getServo(int num)
    {
        if (num < 1 || num > 8)
        {
            throw new Exception("MotorHAT Motor must be between 1 and 8 inclusive");
        }
        return this.servos[num - 1];
    }
}
