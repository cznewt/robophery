
class Tls2591Module(I2cModule):
    """
    Module for TSL2591 luminosity sensor.
    """
    DEVICE_NAME = 'i2c-tsl2591'


    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', self.DEVICE_ADDR)
        super(Tls2591Module, self).__init__(*args, **kwargs)
