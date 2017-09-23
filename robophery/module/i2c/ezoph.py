from robophery.interface.i2c import I2cModule


class EzoPhModule(I2cModule):
    """
    Module for AtlasScientific sensors.
    """
    DEVICE_NAME = 'ezoph'
    DEVICE_ADDR = 99
    SLAVE_ADDR = 0x703
    CMD_READ = 0x52
    CMD_STOP = 0x00
    # the timeout needed to query readings and calibrations
    TIMEOUT_LONG = 1000
    # timeout for regular commands
    TIMEOUT_SHORT = 400

    def __init__(self, *args, **kwargs):
        super(EzoPhModule, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))

    def _read_data(self):
        """
        Write a command to the board, wait the correct timeout, and read
        the response.
        """
        self._data.writeRaw8(self.CMD_READ)
        self._data.writeRaw8(self.CMD_STOP)
        self._msleep(self.TIMEOUT_LONG)
        response_raw = self._data.readList(0, 31)
        if response_raw[0] == 1:
            response = filter(lambda x: x != 0, response_raw)
            char_list = map(lambda x: chr(x), list(response[1:]))
            return float("".join(char_list))
        else:
            return None

    def read_data(self):
        """
        Get all sensor readings.
        """
        read_start = self._get_time()
        try:
            ph = self._read_data()
        except IOError:
            ph = None
        read_stop = self._get_time()
        read_time = read_stop - read_start
        data = [
            (self._name, 'ph', ph, read_time),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'ph': {
                'type': 'gauge',
                'unit': '',
                'precision': 0.002,
                'range_low': 0.001,
                'range_high': 14.000,
                'sensor': self.DEVICE_NAME
            },
        }
