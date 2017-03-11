
class I2cInterface(object):
    """
    Base class for implementing I2C bus.
    """

    def __init__(self, *args, **kwargs):
        self._addrs_used = []


    def setup_addr(self, addr):
        """
        Set the specified address.
        """
        self._addrs_used.append(addr)


    def writeRaw8(self, value):
        """
        Write an 8-bit value on the bus (without register).
        """
        raise NotImplementedError


    def write8(self, register, value):
        """
        Write an 8-bit value to the specified register.
        """
        raise NotImplementedError


    def write16(self, register, value):
        """
        Write a 16-bit value to the specified register.
        """
        raise NotImplementedError


    def writeList(self, register, data):
        """
        Write bytes to the specified register.
        """
        raise NotImplementedError


    def readRaw8(self):
        """
        Read an 8-bit value on the bus (without register).
        """
        raise NotImplementedError


    def readU8(self, register):
        """
        Read an unsigned byte from the specified register.
        """
        raise NotImplementedError


    def readS8(self, register):
        """
        Read a signed byte from the specified register.
        """
        raise NotImplementedError


    def readU16(self, register, little_endian=True):
        """
        Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        raise NotImplementedError


    def readS16(self, register, little_endian=True):
        """
        Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        raise NotImplementedError


    def readList(self, register, length):
        """
        Read a length number of bytes from the specified register. Results
        will be returned as a bytearray.
        """
        raise NotImplementedError
