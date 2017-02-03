
#import smbus
from robophery.core import Module

#Type of I2C interface to manage system device
#I2C_SMBUS_INTERFACE = 1
#I2C_ADAFRUIT_I2C_INTERFACE = 2

class I2cModule(Module):

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
