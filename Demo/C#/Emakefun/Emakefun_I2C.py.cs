using System.Device.I2c;

public class Emakefun_I2C
{
    public byte address { get; set; }

    public I2cDevice bus { get; set; }

    public bool debug { get; set; }

    public Emakefun_I2C(byte address, bool debug = false)
    {
        this.address = address;
        this.bus = I2cDevice.Create(new(1, address));
        this.debug = debug;
    }

    public virtual bool errMsg()
    {
        Console.WriteLine(String.Format("Error accessing {0}: Check your I2C address", this.address));
        return false;
    }

    // Writes an 8-bit value to the specified register/address
    public virtual bool write8(byte reg, byte value)
    {
        try
        {
            this.bus.Write(new byte[] { reg, value });
            if (this.debug)
            {
                Console.WriteLine(String.Format("I2C: Wrote {0} to register {1}", value, reg));
            }
            return true;
        }
        catch (Exception ex)
        {
            return this.errMsg();
        }
    }

    /// <summary>
    /// Writes a 16-bit value to the specified register/address pair
    /// </summary>
    /// <param name="reg"></param>
    /// <param name="value"></param>
    /// <returns></returns>
    public virtual bool write16(byte reg, ushort value)
    {
        try
        {
            this.bus.Write(new byte[] { reg, (byte)(value & 0xFF), (byte)(value >> 8) });
            if (this.debug)
            {
                Console.WriteLine(String.Format("I2C: Wrote 0x%02X to register pair 0x%02X,0x%02X", value, reg, reg + 1));
            }
            return true;
        }
        catch (Exception ex)
        {
            return this.errMsg();
        }
    }

    /// <summary>
    /// Writes an 8-bit value on the bus
    /// </summary>
    /// <param name="value"></param>
    /// <returns></returns>
    public virtual bool writeRaw8(byte value)
    {
        try
        {
            this.bus.WriteByte(value);
            if (this.debug)
            {
                Console.WriteLine(String.Format("I2C: Wrote 0x%02X", value));
            }
            return true;
        }
        catch (Exception ex)
        {
            return this.errMsg();
        }
    }

    /// <summary>
    /// Writes an array of bytes using I2C format
    /// </summary>
    /// <param name="reg"></param>
    /// <param name="list"></param>
    /// <returns></returns>
    public virtual bool writeList(byte reg, byte[] list)
    {
        try
        {
            if (this.debug)
            {
                Console.WriteLine(String.Format("I2C: Writing list to register 0x%02X:", reg));
                Console.WriteLine(list);
            }
            byte[] writeData = new byte[list.Length + 1];
            writeData[0] = reg;
            list.CopyTo(writeData, 1);
            this.bus.Write(writeData);
            return true;
        }
        catch (Exception ex)
        {
            return this.errMsg();
        }
    }

    /// <summary>
    /// Read a list of bytes from the I2C device
    /// </summary>
    /// <param name="reg"></param>
    /// <param name="length"></param>
    /// <returns></returns>
    public virtual byte[] readList(byte reg, byte length)
    {
        try
        {
            byte[] writeData = new byte[] { reg };
            byte[] readData = new byte[length];
            this.bus.WriteRead(writeData, readData);
            if (this.debug)
            {
                Console.WriteLine(String.Format("I2C: Device {0} returned the following from reg {1}", this.address, reg));
                Console.WriteLine(readData);
            }
            return readData;
        }
        catch (Exception ex)
        {
            this.errMsg();
            return null;
        }
    }

    /// <summary>
    /// Read an unsigned byte from the I2C device
    /// </summary>
    /// <param name="reg"></param>
    /// <returns></returns>
    public virtual byte readU8(byte reg)
    {
        try
        {
            byte[] data = new byte[1];
            this.bus.WriteRead(new byte[] { reg }, data);
            if (this.debug)
            {
                Console.WriteLine(String.Format("I2C: Device {0} returned {2} from reg {3}", this.address, data[0], reg));
            }
            return data[0];
        }
        catch (Exception ex)
        {
            this.errMsg();
            return 0;
        }
    }

    /// <summary>
    /// Reads a signed byte from the I2C device
    /// </summary>
    /// <param name="reg"></param>
    /// <returns></returns>
    public virtual byte readS8(byte reg)
    {
        try
        {
            this.bus.WriteByte(reg);
            byte result = this.bus.ReadByte();
            if (this.debug)
            {
                Console.WriteLine(String.Format("I2C: Device {0} returned {1} from reg {2}", this.address, result, reg));
            }
            return result;
        }
        catch (Exception ex)
        {
            this.errMsg();
            return 0;
        }
    }

}