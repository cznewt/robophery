
#import smbus
from robophery.core import Module

#Type of I2C interface to manage system device
#I2C_SMBUS_INTERFACE = 1
#I2C_ADAFRUIT_I2C_INTERFACE = 2

class I2cModule(Module):
    I2C_LINUX_DEV_PLATFORM = 1
    I2C_NODEMCU_DEV_PLATFORM = 2
    I2C_FT232_DEV_PLATFORM = 3

    def setup_device(self, address, busnum=0, platform=I2C_LINUX_DEV_PLATFORM):
        if platform is I2C_LINUX_DEV_PLATFORM:
            self._interface = SMBusInterface(address, busnum)
        elif platform is I2C_NODEMCU_DEV_PLATFORM:
            self._interface = NodeMcuInterface(address)
        elif platform is I2C_FT232_DEV_PLATFORM:
            self._interface = FT232Interface(address)

        self.writeRaw8 = self._interface.writeRaw8
        self.write8 = self._interface.write8
        self.write16 = self._interface.write16
        self.writeList = self._interface.writeList
        self.readRaw8 = self._interface.readRaw8
        self.readU8 = self._interface.readU8
        self.readS8 = self._interface.readS8
        self.readU16 = self._interface.readU16
        self.readS16 = self._interface.readS16
        self.readList = self._interface.readList

    def set_device(self, address, busnum):
        """
        Set up I2C device for drivers using Adafruit_GPIO.I2C.
        """
        import Adafruit_GPIO.I2C as I2C
        #i2c = I2C
        self._device = I2C.get_i2c_device(address, busnum)

    def set_bus(self, busnum):
        """
        Set up bus for drivers using SMBus directly. 
        """
        import smbus
        self.bus = smbus.SMBus(busnum)

    def set_addr(self, addr):
        """
        Set address for reading.
        """
        self.addr = addr

class SMBusInterface():

    def __init__(address, busnum):
        import smbus
        self._bus = smbus.SMBus(busnum)
        self._address = address

    def writeRaw8(self, value):
        """Write an 8-bit value on the bus (without register)."""
        value = value & 0xFF
        self._bus.write_byte(self._address, value)

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""
        value = value & 0xFF
        self._bus.write_byte_data(self._address, register, value)

    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""
        value = value & 0xFFFF
        self._bus.write_word_data(self._address, register, value)

    def writeList(self, register, data):
        """Write bytes to the specified register."""
        self._bus.write_i2c_block_data(self._address, register, data)

    def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        result = self._bus.read_byte(self._address) & 0xFF
        return result

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        result = self._bus.read_byte_data(self._address, register) & 0xFF
        return result

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        result = self.readU8(register)
        if result > 127:
            result -= 256
        return result

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = self._bus.read_word_data(self._address,register) & 0xFFFF
        # Swap bytes if using big endian because read_word_data assumes little
        # endian on ARM (little endian) systems.
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
        return result

    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        result = self.readU16(register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    def readList(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        results = self._bus.read_i2c_block_data(self._address, register, length)
        return results


class NodeMcuInterface():

    def __init__(address):
        from pyb import I2C
        self.i2c = I2C(port, I2C.MASTER)

    def writeRaw8(self, value):
        """Write an 8-bit value on the bus (without register)."""

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""

    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""

    def writeList(self, register, data):
        """Write bytes to the specified register."""

    def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        return result

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        return result

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        return result

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        return result

    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        return result

    def readList(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        return results

class FT232Interface():

    def __init__(address):
        from Adafruit.FT232 import I2C

    def writeRaw8(self, value):
        """Write an 8-bit value on the bus (without register)."""

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""

    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""

    def writeList(self, register, data):
        """Write bytes to the specified register."""

    def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        return result

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        return result

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        return result

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        return result

    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        return result

    def readList(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        return results
