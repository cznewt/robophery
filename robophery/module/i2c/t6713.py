import array
import time
from robophery.module.i2c.base import I2cModule


class T6713Module(I2cModule):
    """
    Module for T6713 CO2 sensor.
    """
    DEVICE_NAME = 't6713'
    # T6713 default address
    DEVICE_ADDR = 0x15

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', self.DEVICE_ADDR)
        super(T6713Module, self).__init__(*args, **kwargs)

    def _status(self):
        buffer = array.array('B', [0x04, 0x13, 0x8a, 0x00, 0x01])
        self.dev.write(buffer)
        time.sleep(0.1)
        data = self.dev.read(4)
        buffer = array.array('B', data)
        return buffer[2] * 256 + buffer[3]

    def _checkABC(self):
        buffer = array.array('B', [0x04, 0x03, 0xee, 0x00, 0x01])
        self.dev.write(buffer)
        time.sleep(0.1)
        data = self.dev.read(4)
        buffer = array.array('B', data)
        return buffer[2] * 256 + buffer[3]

    def _calibrate(self):
        buffer = array.array('B', [0x05, 0x03, 0xec, 0xff, 0x00])
        self.dev.write(buffer)
        time.sleep(0.1)
        data = self.dev.read(5)
        buffer = array.array('B', data)
        return buffer[3] * 256 + buffer[3]

    def read_co2(self):
        buffer = array.array('B', [0x04, 0x13, 0x8b, 0x00, 0x01])
        self.dev.write(buffer)
        time.sleep(0.1)
        data = self.dev.read(4)
        buffer = array.array('B', data)
        return buffer[2] * 256 + buffer[3]

    def read_data(self):
        """
        Get all sensor readings.
        """
        co2_time_start = time.time()
        co2 = self.read_co2()
        co2_time_stop = time.time()
        co2_time_delta = co2_time_stop - co2_time_start
        return [
            (self._name, 'co2_concetration', co2, co2_time_delta),
        ]
