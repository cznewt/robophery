from struct import unpack
from robophery.interface.i2c import I2cModule

AM2320_READ_PARAM = 0x03
AM2320_HUMIDITY_MSB = 0x00
AM2320_HUMIDITY_LSB = 0x01
AM2320_TEMPERATURE_MNB = 0x04
AM2320_TEMPERATURE_MSB = 0x02
AM2320_TEMPERATURE_LSB = 0x03
AM2320_DEVICE_ID_BIT_24_31 = 0x0B


class CommunicationError(Exception):
    pass


class Am2320Module(I2cModule):
    """
    Module for BH1750 light sensor.
    """
    DEVICE_NAME = 'am2320'
    DEVICE_ADDR = 0x5c

    def __init__(self, *args, **kwargs):
        super(Am2320Module, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))

    def _read_raw(self, command, regaddr, regcount):
        try:
            self._data.writeList(0x00, [])
            self._data.writeList(command, [regaddr, regcount])

            self._msleep(1.6)

            data = self._data.readList(0, 8)
        except IOError as exc:
            raise CommunicationError(str(exc))

        # Check data[0] and data[1]
        if data[0] != 0x03 or data[1] != 0x04:
            raise Exception("First two read bytes are a mismatch")

        # CRC check
        if self._calc_crc16(data[0:6]) != self._combine_bytes(data[7], data[6]):
            raise Exception("CRC failed")

        # Temperature resolution is 16Bit, temperature highest bit (Bit15) is
        # equal to 1 indicates a negative temperature, the temperature highest
        # bit (Bit15) is equal to 0 indicates a positive temperature;
        # temperature in addition to the most significant bit (Bit14 ~ Bit0)
        # indicates the temperature sensor string value. Temperature sensor
        # value is a string of 10 times the actual temperature value.

        temp = self._combine_bytes(data[4], data[5])
        if temp & 0x8000:
          temp = -(temp & 0x7FFF)
        temp /= 10.0

        humi = self._combine_bytes(data[2], data[3]) / 10.0

        return (temp, humi)

    def _calc_crc16(data):
        crc = 0xFFFF
        for x in data:
            crc = crc ^ x
            for bit in range(0, 8):
                if (crc & 0x0001) == 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    def _combine_bytes(msb, lsb):
        return msb << 8 | lsb

    def read_uid(self):
        """
        Read and return unique 32bit sensor ID.
        """
        resp = self._read_raw(AM2320_READ_PARAM, AM2320_DEVICE_ID_BIT_24_31, AM2320_TEMPERATURE_MNB)
        uid = unpack('>I', resp)[0]
        return uid

    def read_data(self):
        """
        Query AM2320 to get the humidity and temperature readings.
        """
        read_start = self._get_time()
        temperature, humidity = self._read_raw(AM2320_READ_PARAM, AM2320_HUMIDITY_MSB, AM2320_TEMPERATURE_MNB)
        read_time = (self._get_time() - read_start) / 2
        data = [
            (self._name, 'temperature', temperature, read_time),
            (self._name, 'humidity', humidity, read_time)
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
                'resolution': 0.1,
                'precision': 0.5,
                'range_low': -40,
                'range_high': 80,
                'sensor': self.DEVICE_NAME
            },
            'humidity': {
                'type': 'gauge',
                'unit': 'RH',
                'resolution': 0.1,
                'precision': 3,
                'range_low': 0,
                'range_high': 99.9,
                'sensor': self.DEVICE_NAME
            }
        }
