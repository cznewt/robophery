
import smbus
from robophery.core import Module

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
