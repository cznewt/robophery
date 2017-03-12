import time


class Si7021Module(I2cModule):
    """
    Module for SI7021 temperature and humidity sensor.
    """
    DEVICE_NAME = 'i2c-si7021'
    # SI7021 default address
    DEVICE_ADDR = 0x40
    # Operating modes
    HOLD_MASTER = 0x00
    NOHOLD_MASTER = 0xF5


    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', self.DEVICE_ADDR)
        super(Si7021Module, self).__init__(*args, **kwargs)
        self.writeRaw8(NOHOLD_MASTER)


    def read_temperature(self):
		# Read data back, 2 bytes, Temperature MSB first
		data0 = bus.read_byte(0x40)
		data1 = bus.read_byte(0x40)
		# Convert the data
		return ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85


    def read_humidity(self):
		time.sleep(0.3)
		# Read data back, 2 bytes, Humidity MSB first
		data0 = bus.read_byte(0x40)
		data1 = bus.read_byte(0x40)
		# Convert the data
		return ((data0 * 256 + data1) * 125 / 65536.0) - 6


    def read_data(self):
        """
        Get all sensor readings.
        """
        temp_time_start = time.time()
        temp = self.read_temperature()
        temp_time_stop = time.time()
        temp_time_delta = temp_time_stop - temp_time_start
        humid_time_start = time.time()
        humid = self.read_humidity()
        humid_time_stop = time.time()
        humid_time_delta = humid_time_stop - humid_time_start
        return [
            (self._name, 'temperature', temp, temp_time_delta),
            (self._name, 'humidity', humid, humid_time_delta),
        ]
