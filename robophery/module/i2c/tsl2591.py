from robophery.interface.i2c import I2cModule


class Tls2591Module(I2cModule):
    """
    Module for TSL2591 luminosity sensor.
    """
    DEVICE_NAME = 'tsl2591'

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', self.DEVICE_ADDR)
        super(Tls2591Module, self).__init__(*args, **kwargs)
