from robophery.interface.i2c import I2cModule


class Tsl2591Module(I2cModule):
    """
    Module for TSL2591 based light-to-digital convertor.
    """
    DEVICE_NAME = 'tsl2591'
    # TSL2591 default address
    DEVICE_ADDR = 0x29

    VISIBLE_LIGHT = 2  # channel 0 - channel 1
    INFRARED_LIGHT = 1  # channel 1
    FULL_SPECTRUM = 0  # channel 0

    READ_BIT = 0x01
    COMMAND_BIT = 0xA0  # bits 7 and 5 for 'command normal'
    CLEAR_BIT = 0x40  # Clears any pending interrupt (write 1 to clear)
    WORD_BIT = 0x20  # 1 = read/write word (rather than byte)
    BLOCK_BIT = 0x10  # 1 = using block read/write

    ENABLE_POWERON = 0x01
    ENABLE_POWEROFF = 0x00
    ENABLE_AEN = 0x02
    ENABLE_AIEN = 0x10
    CONTROL_RESET = 0x80

    LUX_DF = 408.0
    LUX_COEFB = 1.64  # CH0 coefficient
    LUX_COEFC = 0.59  # CH1 coefficient A
    LUX_COEFD = 0.86  # CH2 coefficient B

    REGISTER_ENABLE = 0x00
    REGISTER_CONTROL = 0x01
    REGISTER_THRESHHOLDL_LOW = 0x02
    REGISTER_THRESHHOLDL_HIGH = 0x03
    REGISTER_THRESHHOLDH_LOW = 0x04
    REGISTER_THRESHHOLDH_HIGH = 0x05
    REGISTER_INTERRUPT = 0x06
    REGISTER_CRC = 0x08
    REGISTER_ID = 0x0A
    REGISTER_CHAN0_LOW = 0x14
    REGISTER_CHAN0_HIGH = 0x15
    REGISTER_CHAN1_LOW = 0x16
    REGISTER_CHAN1_HIGH = 0x17

    INTEGRATION_TIME_100MS = 0x00
    INTEGRATION_TIME_200MS = 0x01
    INTEGRATION_TIME_300MS = 0x02
    INTEGRATION_TIME_400MS = 0x03
    INTEGRATION_TIME_500MS = 0x04
    INTEGRATION_TIME_600MS = 0x05

    GAIN_LOW = 0x00  # low gain (1x)
    GAIN_MED = 0x10  # medium gain (25x)
    GAIN_HIGH = 0x20  # medium gain (428x)
    GAIN_MAX = 0x30  # max gain (9876x)

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', self.DEVICE_ADDR)
        super(Tsl2591Module, self).__init__(*args, **kwargs)

        self._channel = self.VISIBLE_LIGHT
        self._gain = self.GAIN_LOW
        self._integration_time = self.INTEGRATION_TIME_100MS

        self._set_timing(self._integration_time)
        self._set_gain(self._gain)
        self._disable()

    def _enable(self):
        self.write8(
            self.COMMAND_BIT | self.REGISTER_ENABLE,
            self.ENABLE_POWERON | self.ENABLE_AEN | self.ENABLE_AIEN
        )

    def _disable(self):
        self.write8(
            self.COMMAND_BIT | self.REGISTER_ENABLE,
            self.ENABLE_POWEROFF
        )

    def _set_timing(self, integration):
        self._enable()
        self._integration_time = integration
        self.write8(
            self.COMMAND_BIT | self.REGISTER_CONTROL,
            self._integration_time | self._gain
        )
        self._disable()

    def _get_timing(self):
        return self._integration_time

    def _set_gain(self, gain):
        self._enable()
        self._gain = gain
        self.write8(
            self.COMMAND_BIT | self.REGISTER_CONTROL,
            self._integration_time | self._gain
        )
        self._disable()

    def _get_gain(self):
        return self._gain

    def calculate_lux(self, full, ir):
        # Check for overflow conditions first
        if (full == 0xFFFF) | (ir == 0xFFFF):
            return 0

        case_integ = {
            self.INTEGRATION_TIME_100MS: 100.,
            self.INTEGRATION_TIME_200MS: 200.,
            self.INTEGRATION_TIME_300MS: 300.,
            self.INTEGRATION_TIME_400MS: 400.,
            self.INTEGRATION_TIME_500MS: 500.,
            self.INTEGRATION_TIME_600MS: 600.,
        }
        if self._integration_time in case_integ.keys():
            atime = case_integ[self._integration_time]
        else:
            atime = 100.

        case_gain = {
            self.GAIN_LOW: 1.,
            self.GAIN_MED: 25.,
            self.GAIN_HIGH: 428.,
            self.GAIN_MAX: 9876.,
        }

        if self._gain in case_gain.keys():
            again = case_gain[self._gain]
        else:
            again = 1.

        # cpl = (ATIME * AGAIN) / DF
        cpl = (atime * again) / self.LUX_DF
        lux1 = (full - (self.LUX_COEFB * ir)) / cpl
        lux2 = ((self.LUX_COEFC * full) - (self.LUX_COEFD * ir)) / cpl

        # The highest value is the approximate lux equivalent
        return max([lux1, lux2])

    def get_full_luminosity(self):
        self._enable()
        # not sure if we need it "// Wait x ms for ADC to complete"
        self._sleep(0.120 * self._integration_time + 1)
        full = self.readU16(self.COMMAND_BIT | self.REGISTER_CHAN0_LOW)
        ir = self.readU16(self.COMMAND_BIT | self.REGISTER_CHAN1_LOW)
        self._disable()
        return full, ir

    def read_data(self):
        """
        Get the luminosity readings.
        """
        read_time_start = self._get_time()
        try:
            full, ir = self.get_full_luminosity()
            luminosity = self.calculate_lux(full, ir)
        except IOError:
            luminosity = None
        read_time_delta = self._get_time() - read_time_start
        data = [
            (self._name, 'luminosity', luminosity, read_time_delta),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'luminosity': {
                'type': 'gauge',
                'unit': 'lx',
                'precision': 0.000180,
                'range_low': 0,
                'range_high': 88000,
                'sensor': self.DEVICE_NAME
            }
        }
