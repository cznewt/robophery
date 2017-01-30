
try:
    import Adafruit_BBIO.GPIO as GPIO
    device = 'bbb'
except Exception, e:
    pass

try:
    import RPi.GPIO as GPIO
    device = 'rpi'
except Exception, e:
    pass

from robophery.core import Module

class GpioModule(Module):

    def set_port(port):
        """
        Set GPIO port for operation.
        """
        self.port = int(port)
