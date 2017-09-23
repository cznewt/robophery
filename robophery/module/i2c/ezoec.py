from robophery.interface.i2c import I2cModule


class EzoEcModule(I2cModule):
    """
    Module for AtlasScientific sensors.
    """
    DEVICE_NAME = 'ezoec'
    DEVICE_ADDR = 100
    SLAVE_ADDR = 0x703
    CMD_READ = 0x52
    CMD_STOP = 0x00
    # the timeout needed to query readings and calibrations
    TIMEOUT_LONG = 700
    # timeout for regular commands
    TIMEOUT_SHORT = 400

    def __init__(self, *args, **kwargs):
        super(EzoEcModule, self).__init__(*args, **kwargs)
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
            vals = "".join(char_list).split(',')
            return float(vals[0]), float(vals[1]), float(vals[2]), float(vals[3])
        else:
            return None

    def read_data(self):
        """
        Get all sensor readings.
        """
        read_start = self._get_time()
        try:
            ec, tds, s, sg = self._read_data()
        except IOError:
            ec, tds, s, sg = None
        read_stop = self._get_time()
        read_time = (read_stop - read_start) / 4
        data = [
            (self._name, 'conductivity', ec, read_time),
            (self._name, 'total_dissolved_solids', tds, read_time),
            (self._name, 'salinity', s, read_time),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'conductivity': {
                'type': 'gauge',
                'unit': 'uS/cm',
                'precision': 100.00,
                'range_low': 0.07,
                'range_high': 500000,
                'sensor': self.DEVICE_NAME
            },
            'total_dissolved_solids': {
                'type': 'gauge',
                'unit': 'ppm',
                'precision': 1000,
                'range_low': 0,
                'range_high': 1000000,
                'sensor': self.DEVICE_NAME
            },
            'salinity': {
                'type': 'gauge',
                'unit': 'ppt',
                'precision': 1,
                'range_low': 0,
                'range_high': 1000,
                'sensor': self.DEVICE_NAME
            },
        }
