try:
    import smbus
except:
    raise RuntimeError("Cannot load smbus library. Please install the library.")

from robophery.platform.i2c import I2cInterface


class SMBusI2cInterface(I2cInterface):

    def __init__(self, *args, **kwargs):
        self._busnum = int(kwargs.get('busnum', 1))
        self._bus = smbus.SMBus(self._busnum)
        super(SMBusI2cInterface, self).__init__(*args, **kwargs)


    def writeRaw8(self, addr, value):
        """
        Write an 8-bit value on the bus (without register).
        """
        value = value & 0xFF
        self._bus.write_byte(addr, value)


    def write8(self, addr, register, value):
        """
        Write an 8-bit value to the specified register.
        """
        value = value & 0xFF
        self._bus.write_byte_data(addr, register, value)

    def write16(self, addr, register, value):
        """
        Write a 16-bit value to the specified register.
        """
        value = value & 0xFFFF
        self._bus.write_word_data(addr, register, value)

    def writeList(self, addr, register, data):
        """
        Write bytes to the specified register.
        """
        self._bus.write_i2c_block_data(addr, register, data)

    def readRaw8(self):
        """
        Read an 8-bit value on the bus (without register).
        """
        result = self._bus.read_byte(addr) & 0xFF
        return result

    def readU8(self, addr, register):
        """
        Read an unsigned byte from the specified register.
        """
        result = self._bus.read_byte_data(addr, register) & 0xFF
        return result

    def readS8(self, addr, register):
        """
        Read a signed byte from the specified register.
        """
        result = self.readU8(addr, register)
        if result > 127:
            result -= 256
        return result

    def readU16(self, addr, register, little_endian=True):
        """
        Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        result = self._bus.read_word_data(addr, register) & 0xFFFF
        # Swap bytes if using big endian because read_word_data assumes little
        # endian on ARM (little endian) systems.
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result

    def readS16(self, addr, register, little_endian=True):
        """
        Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        result = self.readU16(addr, register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    def readList(self, addr, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        results = self._bus.read_i2c_block_data(addr, register, length)
        return results
