import struct
from robophery.interface.i2c import I2cModule


class Vl53L0XModule(I2cModule):
    """
    Module for VL53L0X light to distance sensor.
    """
    DEVICE_NAME = 'vl53l0x'
    # VL53L0X default address
    DEVICE_ADDR = 0x29

    VL53L0X_REG_IDENTIFICATION_MODEL_ID = 0x00c0
    VL53L0X_REG_IDENTIFICATION_REVISION_ID = 0x00c2
    VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD = 0x0050
    VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD = 0x0070
    VL53L0X_REG_SYSRANGE_START = 0x000

    VL53L0X_REG_RESULT_INTERRUPT_STATUS = 0x0013
    VL53L0X_REG_RESULT_RANGE_STATUS = 0x0014

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', self.DEVICE_ADDR)
        super(Vl53L0XModule, self).__init__(*args, **kwargs)
        val1 = self.readU8(self.VL53L0X_REG_IDENTIFICATION_REVISION_ID)
        self._revision_id = hex(val1)
        val1 = self.readU8(self.VL53L0X_REG_IDENTIFICATION_MODEL_ID)
        self._device_id = hex(val1)
        val1 = self.readU8(self.VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD)
        val1 = self.readU8(self.VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD)

    def bswap(self, val):
        return struct.unpack('<H', struct.pack('>H', val))[0]

    def mread_word_data(self, reg):
        return self.bswap(self.readU16(reg))

    def mwrite_word_data(self, reg, data):
        return self.write16(reg, self.bswap(data))

    def _makeuint16(self, lsb, msb):
        return ((msb & 0xFF) << 8) | (lsb & 0xFF)

    def _decode_vcsel_period(self, vcsel_period_reg):
        """
        Converts the encoded VCSEL period register value into the real
        period in PLL clocks.
        """
        vcsel_period_pclks = (vcsel_period_reg + 1) << 1
        return vcsel_period_pclks

    def read_distance(self):
        val1 = self.write8(self.VL53L0X_REG_SYSRANGE_START, 0x01)
        cnt = 0
        while (cnt < 100):
            # 1 second waiting time max
            self._msleep(10)
            val = self.readU8(self.VL53L0X_REG_RESULT_RANGE_STATUS)
            if (val & 0x01):
                break
            cnt += 1

        data = self.readList(0x14, 12)
        ambient_count = self._makeuint16(data[7], data[6])
        signal_count = self._makeuint16(data[9], data[8])
        distance = self._makeuint16(data[11], data[10])
        range_status_internal = ((data[0] & 0x78) >> 3)
        return distance * 0.001

    def read_data(self):
        """
        Get sensor reading.
        """
        read_time_start = self._get_time()
        distance = self.read_distance()
        read_time_stop = self._get_time()
        read_time_delta = read_time_stop - read_time_start
        data = [
            (self._name, 'distance', distance, read_time_delta),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'distance': {
                'type': 'gauge',
                'unit': 'm',
                'precision': 0.01,
                'range_low': 0.03,
                'range_high': 1,
                'sensor': self.DEVICE_NAME
            },
        }
