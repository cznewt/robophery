
import smbus
from robophery.core import Module

#Type of I2C interface to manage system device
I2C_SMBUS_INTERFACE = 1
I2C_ADAFRUIT_I2C_INTERFACE = 2

class I2cModule(Module):

    def set_bus(self, bus):
        """
        Set bus for reading.
        """
        self.bus = smbus.SMBus(int(bus))


    def set_addr(self, addr):
        """
        Set address for reading.
        """
        self.addr = addr
