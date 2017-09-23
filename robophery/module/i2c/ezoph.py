from robophery.interface.i2c import I2cModule


class EzoHpModule(I2cModule):
    """
    Module for AtlasScientific sensors.
    """
    DEVICE_NAME = 'ezoph'
    DEVICE_ADDR = 99
    SLAVE_ADDR = 0x703

    # the timeout needed to query readings and calibrations
    TIMEOUT_LONG = 1500
    # timeout for regular commands
    TIMEOUT_SHORT = 500

    def __init__(self, *args, **kwargs):
        super(EzoHpModule, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))

    def _write_cmd(self, cmd):
        """
        Appends the null character and sends the string over I2C
        """
        cmd += 0x00
        self.file_write.write(cmd)

    def _cmd_read(self, num_of_bytes=31):
        """
        Reads a specified number of bytes from I2C, then parses and displays
        the result.
        """
        res = self.file_read.read(num_of_bytes)  # read from the board
        # remove the null characters to get the response
        response = filter(lambda x: x != '\x00', res)
        if ord(response[0]) == 1:  # if the response isn't an error
            # change MSB to 0 for all received characters except the first and
            # get a list of characters
            char_list = map(lambda x: chr(ord(x) & ~0x80), list(response[1:]))
            # NOTE: having to change the MSB to 0 is a glitch in the raspberry
            # pi, and you shouldn't have to do this!
            # convert the char list to a string and returns it
            return "Command succeeded " + ''.join(char_list)
        else:
            return "Error " + str(ord(response[0]))

    def _read_data(self):
        """
        Write a command to the board, wait the correct timeout, and read
        the response.
        """
        self._data.writeRaw8(0x52)

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
        print ph
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
