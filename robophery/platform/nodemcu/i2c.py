from ustruct import (pack, unpack)

class NodemcuI2cInterface(I2cInterface):
    def __init__(self, gpio_interface, scl_pin=5, sda_pin=4, frequency=100000):
        from machine import Pin, I2C

        gpio_interface.setup_pin(scl_pin)
        gpio_interface.setup_pin(sda_pin)

        self._scl = gpio_interface.get_pin(scl_pin)
        self._sda = gpio_interface.get_pin(sda_pin)

        self._bus = I2C(scl=self._scl, sda=self._sda, freq=frequency)

    def scan_bus():
        """Return list of found addresses on bus"""
        return self._bus.scan()

    def writeRaw8(self, addr, value):
        """Write an 8-bit value on the bus (without register)."""
        value = value & 0xFF
        self._bus.writeto(addr, bytes([value]))

    def write8(self, addr, register, value):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        self._bus.writeto_mem(addr, register, bytes([value]))

    def write16(self, addr, register, value):
        """Write a 16-bit value to the specified register."""
        bvalue = pack('>H', (value & 0xFFFF))
        self._bus.writeto_mem(addr, register, bvalue)

    def writeList(self, addr, register, data):
        """Write bytes to the specified register."""
        bvalue = bytes(data)
        self._bus.writeto_mem(addr, register, bvalue)

    def readRaw8(self, addr):
        """Read an 8-bit value on the bus (without register)."""
        bvalue = self._bus.readfrom(addr, 1)
        result = unpack('B', bvalue)[0]
        return result

    def readU8(self, addr, register):
        """Read an unsigned byte from the specified register."""
        bvalue = self._bus.readfrom_mem(addr, register, 1)
        result = unpack('B', bvalue)[0]
        return result

    def readS8(self, addr, register):
        """Read a signed byte from the specified register."""
        bvalue = self._bus.readfrom_mem(addr, register, 1)
        result = unpack('b', bvalue)[0]
        return result

    def readU16(self, addr, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        bvalue = self._bus.readfrom_mem(addr, register, 2)
        if little_endian is True:
            result = unpack('<H', bvalue)[0]
        else:
            result = unpack('>H', bvalue)[0]
        return result

    def readS16(self, addr, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        bvalue = self._bus.readfrom_mem(addr, register, 2)
        if little_endian is True:
            result = unpack('<h', bvalue)[0]
        else:
            result = unpack('>h', bvalue)[0]
        return result

    def readList(self, addr, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        bvalue = self._bus.readfrom_mem(addr, register, length)
        return list(bvalue)
