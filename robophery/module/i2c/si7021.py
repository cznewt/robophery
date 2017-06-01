from robophery.interface.i2c import I2cModule


class Si7021Module(I2cModule):
    """
    Module for SI7021 temperature and humidity sensor.
    """
    DEVICE_NAME = 'si7021'
    # SI7021 default address
    DEVICE_ADDR = 0x40
    # Operating modes
    READ_TEMP_CMD = 0xf3
    READ_HUMIDITY_CMD = 0xf5

    def __init__(self, *args, **kwargs):
        super(Si7021Module, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))

    def read_temperature(self):
        # Read data back, 2 bytes, Temperature MSB first
        self._data.writeRaw8(self.READ_TEMP_CMD)
        self._msleep(300)
        data0 = self.readRaw8()
        data1 = self.readRaw8()
        return ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85

    def read_humidity(self):
        self._data.writeRaw8(self.READ_HUMIDITY_CMD)
        self._msleep(300)
        # Read data back, 2 bytes, Humidity MSB first
        data0 = self.readRaw8()
        data1 = self.readRaw8()
        return ((data0 * 256 + data1) * 125 / 65536.0) - 6

    def read_data(self):
        """
        Get all sensor readings.
        """
        temp_time_start = self._get_time()
        try:
            temp = self.read_temperature()
        except IOError:
            temp = None
        temp_time_stop = self._get_time()
        temp_time_delta = temp_time_stop - temp_time_start
        humid_time_start = self._get_time()
        try:
            humid = self.read_humidity()
        except IOError:
            humid = None
        humid_time_stop = self._get_time()
        humid_time_delta = humid_time_stop - humid_time_start
        data = [
            (self._name, 'temperature', temp, temp_time_delta),
            (self._name, 'humidity', humid, humid_time_delta),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'temperature': {
                'type': 'gauge',
                'unit': 'C',
                'precision': 0.4,
                'range_low': -10,
                'range_high': 85,
                'sensor': self.DEVICE_NAME
            },
            'humidity': {
                'type': 'gauge',
                'unit': 'RH',
                'precision': 3,
                'range_low': 0,
                'range_high': 80,
                'sensor': self.DEVICE_NAME
            },
        }
