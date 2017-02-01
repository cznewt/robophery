
try:
    import Adafruit_BBIO.GPIO as GPIO
    device = 'bbb'
except:
    pass

try:
    import RPi.GPIO as GPIO
    device = 'rpi'
except:
    pass

from robophery.core import Module

class GpioModule(Module):

    def set_port(self, port):
        """
        Set GPIO port for operation.
        """
        self.port = int(port)
