from robophery.interface.i2c import I2cModule


class EzoEcModule(I2cModule):
    """
    Module for AtlasScientific sensors.
    """
    DEVICE_NAME = 'ezoec'
    DEVICE_ADDR = 100
    SLAVE_ADDR = 0x703

    # the timeout needed to query readings and calibrations
    LONG_TIMEOUT = 1.5
    # timeout for regular commands
    SHORT_TIMEOUT = 0.5

    def __init__(self, *args, **kwargs):
        super(EzoHpModule, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))

    def write(self, cmd):
        # appends the null character and sends the string over I2C
        cmd += "\00"
        self.file_write.write(cmd)

    def read(self, num_of_bytes=31):
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

    def query(self, string):
        """
        Write a command to the board, wait the correct timeout, and read
        the response.
        """
        self.write(string)

        # the read and calibration commands require a longer timeout
        if((string.upper().startswith("R")) or
                (string.upper().startswith("CAL"))):
            self._sleep(self.long_timeout)
        elif string.upper().startswith("SLEEP"):
            return "sleep mode"
        else:
            self._sleep(self.short_timeout)

        return self.read()
