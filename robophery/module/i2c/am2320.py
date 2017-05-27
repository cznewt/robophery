from struct import unpack
from robophery.interface.i2c import I2cModule

I2C_ADDR_AM2320 = 0x5c  # 0xB8 >> 1
AM2320_READ_PARAM = 0x03
AM2320_HUMIDITY_MSB = 0x00
AM2320_HUMIDITY_LSB = 0x01
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
        self._addr = kwargs.get('addr', self.DEVICE_ADDR)
        super(Am2320Module, self).__init__(*args, **kwargs)

    def _read_raw(self, command, regaddr, regcount):
        try:
            self.writeList(0x00, [])
            self.writeList(command, [regaddr, regcount])

            self._msleep(2)

            buf = self.readList(self.address, 0, 8)
        except IOError, exc:
            raise CommunicationError(str(exc))

        buf_str = "".join(chr(x) for x in buf)

        crc = unpack('<H', buf_str[-2:])[0]
        if crc != self._am_crc16(buf[:-2]):
            raise CommunicationError("AM2320 CRC error.")
        return buf_str[2:-2]

    def _am_crc16(self, buf):
        crc = 0xFFFF
        for c in buf:
            crc ^= c
            for i in range(8):
                if crc & 0x01:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc

    def read_uid(self):
        """
        Read and return unique 32bit sensor ID.
        """
        resp = self._read_raw(AM2320_READ_PARAM, AM2320_DEVICE_ID_BIT_24_31, 4)
        uid = unpack('>I', resp)[0]
        return uid

    def read_data(self):
        """
        Query AM2320 to get the humidity and temperature readings.
        """
        read_start = self._get_time()
        raw_data = self._read_raw(AM2320_READ_PARAM, AM2320_HUMIDITY_MSB, 4)
        temperature = unpack('>H', raw_data[-2:])[0] / 10.0
        humidity = unpack('>H', raw_data[-4:2])[0] / 10.0
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
