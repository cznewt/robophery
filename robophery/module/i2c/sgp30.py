from robophery.interface.i2c import I2cModule


class Sgp30Module(I2cModule):
    """
    Module for SGP30 CO2 sensor.
    """
    DEVICE_NAME = 'sgp30'
    DEVICE_ADDR = 0x58

    REG_ADDR = 0x20

    FEATURESET        = 0x0020

    CRC8_POLYNOMIAL   = 0x31
    CRC8_INIT         = 0xFF

    def __init__(self, *args, **kwargs):
        super(Sgp30Module, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))
        # get unique serial, its 48 bits and store in an array
        self.serial = self._sgp_query(0x36, [0x82], 0.01, 3)
        # check the feature set
        featureset = self._sgp_query(0x20, [0x2f], 0.01, 1)
        if featureset[0] != self.FEATURESET:
            self._log.error('Not right device ID (0x0020): {}'.format(featureset[0]))
        self.iaq_init()
        self.set_iaq_baseline(0x8973, 0x8aae)

    def iaq_init(self):
        """Initialize the IAQ algorithm"""
        self._sgp_query(self.REG_ADDR, [0x03], 0.01, 0)

    def iaq_measure(self):
        """Measure the CO2eq and TVOC"""
        return self._sgp_query(self.REG_ADDR, [0x08], 0.05, 2)

    def get_iaq_baseline(self):
        """Retreive the IAQ algorithm baseline for CO2eq and TVOC"""
        return self._sgp_query(self.REG_ADDR, [0x15], 0.01, 2)

    def set_iaq_baseline(self, co2eq, tvoc):
        """Set the previously recorded IAQ algorithm baseline for CO2eq and TVOC"""
        if co2eq == 0 and tvoc == 0:
            raise RuntimeError('Invalid baseline')
        buffer = []
        for value in [tvoc, co2eq]:
            arr = [value >> 8, value & 0xFF]
            arr.append(self._generate_crc(arr))
            buffer += arr
        self._sgp_query(self.REG_ADDR, [0x1e] + buffer, 0.01, 0)

    def _sgp_query(self, reg, cmd, delay, reply_size):
        """Run an SGP command query, get a reply and CRC results if necessary"""
        self._data.writeList(reg, cmd)
        self._sleep(delay)
        if not reply_size:
            return None
        crc_result = self._data.readList(reply_size)
        #print("\tRaw Read: ", crc_result)
        result = []
        for i in range(reply_size):
            word = [crc_result[3*i], crc_result[3*i+1]]
            crc = crc_result[3*i+2]
            if self._generate_crc(word) != crc:
                raise RuntimeError('CRC Error')
            result.append(word[0] << 8 | word[1])
        #print("\tOK Data: ", [hex(i) for i in result])
        return result

    def _generate_crc(self, data):
        """8-bit CRC algorithm for checking data"""
        crc = self.CRC8_INIT
        # calculates 8-Bit checksum with given polynomial
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ self.CRC8_POLYNOMIAL
                else:
                    crc <<= 1
        return crc & 0xFF

    def read_data(self):
        """
        Query SGP30 to get the CO2 readings.
        """
        read_start = self._get_time()
        try:
            co2eq, tvoc = self.iaq_measure()
        except IOError:
            co2eq = None
            tvoc = None
        read_time = (self._get_time() - read_start) / 2
        data = [
            (self._name, 'co2eq', co2eq, read_time),
            (self._name, 'tvoc', tvoc, read_time),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'co2eq': {
                'type': 'gauge',
                'unit': 'ppm',
                'resolution': 1,
                'precision': 1,
                'range_low': 0,
                'range_high': 60000,
                'sensor': self.DEVICE_NAME
            },
            'tvoc': {
                'type': 'gauge',
                'unit': 'ppb',
                'resolution': 1,
                'precision': 1,
                'range_low': 0,
                'range_high': 60000,
                'sensor': self.DEVICE_NAME
            },
        }
