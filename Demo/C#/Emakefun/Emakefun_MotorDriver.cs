using System;
using UnitsNet;

public class PWM
{
    public byte address;

    public bool debug;

    public Emakefun_I2C i2c;

    public byte @__MODE1 = 0x00;

    public byte @__MODE2 = 0x01;

    public byte @__SUBADR1 = 0x02;

    public byte @__SUBADR2 = 0x03;

    public byte @__SUBADR3 = 0x04;

    public byte @__PRESCALE = 0xFE;

    public byte @__LED0_ON_L = 0x06;

    public byte @__LED0_ON_H = 0x07;

    public byte @__LED0_OFF_L = 0x08;

    public byte @__LED0_OFF_H = 0x09;

    public byte @__ALL_LED_ON_L = 0xFA;

    public byte @__ALL_LED_ON_H = 0xFB;

    public byte @__ALL_LED_OFF_L = 0xFC;

    public byte @__ALL_LED_OFF_H = 0xFD;

    public byte @__RESTART = 0x80;

    public byte @__SLEEP = 0x10;

    public byte @__ALLCALL = 0x01;

    public byte @__INVRT = 0x10;

    public byte @__OUTDRV = 0x04;

    public void softwareReset()
    {
        this.i2c.writeRaw8(0x06);
    }

    public PWM(byte address = 0x60, bool debug = false)
    {
        this.i2c = new Emakefun_I2C(address);
        this.i2c.debug = debug;
        this.address = address;
        this.debug = debug;
        if (this.debug)
        {
            Console.WriteLine("Reseting PCA9685 MODE1 (without SLEEP) and MODE2");
        }
        this.setAllPWM(0, 0);
        this.i2c.write8(this.@__MODE2, this.@__OUTDRV);
        this.i2c.write8(this.@__MODE1, this.@__ALLCALL);
        Thread.Sleep(5);
        var mode1 = this.i2c.readU8(this.@__MODE1);
        mode1 = (byte)(mode1 & ~this.@__SLEEP);
        this.i2c.write8(this.@__MODE1, mode1);
        Thread.Sleep(5);
    }

    /// <summary>
    /// Sets the PWM frequency
    /// </summary>
    /// <param name="freq"></param>
    public virtual void setPWMFreq(int freq)
    {
        var prescaleval = 25000000.0;
        prescaleval /= 4096.0;
        prescaleval /= freq;
        prescaleval -= 1.0;
        if (this.debug)
        {
            Console.WriteLine(String.Format("Setting PWM frequency to %d Hz", freq));
            Console.WriteLine(String.Format("Estimated pre-scale: %d", prescaleval));
        }
        var prescale = Math.Floor(prescaleval + 0.5);
        if (this.debug)
        {
            Console.WriteLine(String.Format("Final pre-scale: %d", prescale));
        }
        var oldmode = this.i2c.readU8(this.@__MODE1);
        var newmode = (byte)((oldmode & 0x7F) | 0x10);
        this.i2c.write8(this.@__MODE1, newmode);
        this.i2c.write8(this.@__PRESCALE, Convert.ToByte(Math.Floor(prescale)));
        this.i2c.write8(this.@__MODE1, oldmode);
        Thread.Sleep(5);
        this.i2c.write8(this.@__MODE1, (byte)(oldmode | 0x80));
    }

    /// <summary>
    /// Sets a single PWM channel
    /// </summary>
    /// <param name="channel"></param>
    /// <param name="on"></param>
    /// <param name="off"></param>
    public virtual void setPWM(int channel, int on, int off)
    {
        byte[] writeData = new byte[] {onvert.ToByte(on & 0xFF), Convert.ToByte(on >> 8), Convert.ToByte(off & 0xFF), Convert.ToByte(off >> 8)};
        this.i2c.writeList(Convert.ToByte(this.@__LED0_ON_L + 4 * channel), writeData);
        //this.i2c.write8(Convert.ToByte(this.@__LED0_ON_L + 4 * channel), Convert.ToByte(on & 0xFF));
        //this.i2c.write8(Convert.ToByte(this.@__LED0_ON_H + 4 * channel), Convert.ToByte(on >> 8));
        //this.i2c.write8(Convert.ToByte(this.@__LED0_OFF_L + 4 * channel), Convert.ToByte(off & 0xFF));
        //this.i2c.write8(Convert.ToByte(this.@__LED0_OFF_H + 4 * channel), Convert.ToByte(off >> 8));
    }

    /// <summary>
    /// Sets a all PWM channels
    /// </summary>
    /// <param name="on"></param>
    /// <param name="off"></param>
    public virtual void setAllPWM(int on, int off)
    {
        byte[] writeData = new byte[] {onvert.ToByte(on & 0xFF), Convert.ToByte(on >> 8), Convert.ToByte(off & 0xFF), Convert.ToByte(off >> 8)};
        this.i2c.writeList(Convert.ToByte(this.@__ALL_LED_ON_L + 4 * channel), writeData);
        //this.i2c.write8(this.@__ALL_LED_ON_L, Convert.ToByte(on & 0xFF));
        //this.i2c.write8(this.@__ALL_LED_ON_H, Convert.ToByte(on >> 8));
        //this.i2c.write8(this.@__ALL_LED_OFF_L, Convert.ToByte(off & 0xFF));
        //this.i2c.write8(this.@__ALL_LED_OFF_H, Convert.ToByte(off >> 8));
    }
}