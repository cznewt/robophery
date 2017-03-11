
from pyb import I2C
from robophery.platform.i2c import I2cInterface

class NodeMcuI2cInterface(I2cInterface):

    def __init__(self, address):
        self._bus = I2C(port, I2C.MASTER)
        super(NodeMcuI2cInterface, self).__init__(*args, **kwargs)


    def writeRaw8(self, addr, value):
        """Write an 8-bit value on the bus (without register)."""
        value = value & 0xFF
        self._bus.send(value, addr)


    def write8(self, addr, register, value):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        self._bus.mem_write(value, addr, register)


    def write16(self, addr, register, value):
        """Write a 16-bit value to the specified register."""
        value = value & 0xFFFF
        self._bus.mem_write(value, addr, register)


    def writeList(self, addr, register, data):
        """Write bytes to the specified register."""
        self._bus.mem_write(data, addr, register)


    def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        result = self._bus.recv(1, addr)
        return result


    def readU8(self, addr, register):
        """Read an unsigned byte from the specified register."""
        result = self._bus.mem_read(1, addr, register)
        return result


    def readS8(self, addr, register):
        """Read a signed byte from the specified register."""
        result = readU8(register)
        if result > 127:
            result -= 256
        return result


    def readU16(self, addr, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = self._bus.mem_read(2, addr, register)
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result


    def readS16(self, addr, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = self.readU16(register, little_endian)
        if result > 32767:
            result -= 65536
        return result


    def readList(self, addr, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        #TODO
        #result = self._bus.mem_read(buffer, addr, register)
        #return results
        raise NotImplementedError()
