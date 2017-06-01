from robophery.interface.i2c import I2cModule

# I2C Address of the device
TCS34725_DEFAULT_ADDRESS = 0x29

# TCS34725 Register Set
TCS34725_COMMAND_BIT = 0x80
TCS34725_REG_ENABLE = 0x00  # Enables states and interrupts
TCS34725_REG_ATIME = 0x01  # RGBC integration time
TCS34725_REG_WTIME = 0x03  # Wait time
TCS34725_REG_CONFIG = 0x0D  # Configuration register
TCS34725_REG_CONTROL = 0x0F  # Control register
TCS34725_REG_CDATAL = 0x14  # Clear/IR channel low data register
TCS34725_REG_CDATAH = 0x15  # Clear/IR channel high data register
TCS34725_REG_RDATAL = 0x16  # Red ADC low data register
TCS34725_REG_RDATAH = 0x17  # Red ADC high data register
TCS34725_REG_GDATAL = 0x18  # Green ADC low data register
TCS34725_REG_GDATAH = 0x19  # Green ADC high data register
TCS34725_REG_BDATAL = 0x1A  # Blue ADC low data register
TCS34725_REG_BDATAH = 0x1B  # Blue ADC high data register

# TCS34725 Enable Register Configuration
TCS34725_REG_ENABLE_SAI = 0x40  # Sleep After Interrupt
TCS34725_REG_ENABLE_AIEN = 0x10  # ALS Interrupt Enable
TCS34725_REG_ENABLE_WEN = 0x08  # Wait Enable
TCS34725_REG_ENABLE_AEN = 0x02  # ADC Enable
TCS34725_REG_ENABLE_PON = 0x01  # Power ON

# TCS34725 Time Register Configuration
TCS34725_REG_ATIME_2_4 = 0xFF  # Atime = 2.4 ms, Cycles = 1
TCS34725_REG_ATIME_24 = 0xF6  # Atime = 24 ms, Cycles = 10
TCS34725_REG_ATIME_101 = 0xDB  # Atime = 101 ms, Cycles = 42
TCS34725_REG_ATIME_154 = 0xC0  # Atime = 154 ms, Cycles = 64
TCS34725_REG_ATIME_700 = 0x00  # Atime = 700 ms, Cycles = 256
TCS34725_REG_WTIME_2_4 = 0xFF  # Wtime = 2.4 ms
TCS34725_REG_WTIME_204 = 0xAB  # Wtime = 204 ms
TCS34725_REG_WTIME_614 = 0x00  # Wtime = 614 ms

# TCS34725 Gain Configuration
TCS34725_REG_CONTROL_AGAIN_1 = 0x00  # 1x Gain
TCS34725_REG_CONTROL_AGAIN_4 = 0x01  # 4x Gain
TCS34725_REG_CONTROL_AGAIN_16 = 0x02  # 16x Gain
TCS34725_REG_CONTROL_AGAIN_60 = 0x03  # 60x Gain


class Tcs34725Module(I2cModule):

    DEVICE_NAME = 'tcs34725'

    def __init__(self, *args, **kwargs):
        super(Tcs34725Module, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))
        self.enable_selection()
        self.time_selection()
        self.gain_selection()

    def enable_selection(self):
        """
        Select the ENABLE register configuration from the given provided values
        """
        ENABLE_CONFIGURATION = (TCS34725_REG_ENABLE_AEN |
                                TCS34725_REG_ENABLE_PON)
        self._data.write8(TCS34725_REG_ENABLE |
                    TCS34725_COMMAND_BIT, ENABLE_CONFIGURATION)

    def time_selection(self):
        """
        Select the ATIME register configuration from the given provided values
        """
        self._data.write8(TCS34725_REG_ATIME |
                    TCS34725_COMMAND_BIT, TCS34725_REG_ATIME_700)
        self._data.write8(TCS34725_REG_WTIME |
                    TCS34725_COMMAND_BIT, TCS34725_REG_WTIME_2_4)

    def gain_selection(self):
        """
        Select the gain register configuration from the given provided values
        """
        self._data.write8(TCS34725_REG_CONTROL |
                    TCS34725_COMMAND_BIT, TCS34725_REG_CONTROL_AGAIN_1)

    def read_luminance(self):
        """
        Read data back from TCS34725_REG_CDATAL(0x94), 8 bytes, with
        TCS34725_COMMAND_BIT, (0x80) cData LSB, cData MSB, Red LSB, Red MSB,
        Green LSB, Green MSB, Blue LSB, Blue MSB
        """
        data = self._data.readList(TCS34725_REG_CDATAL | TCS34725_COMMAND_BIT, 8)

        # Convert the data
        cData = data[1] * 256 + data[0]
        red = data[3] * 256 + data[2]
        green = data[5] * 256 + data[4]
        blue = data[7] * 256 + data[6]

        # Calculate luminance
        luminance = (-0.32466 * red) + (1.57837 * green) + (-0.73191 * blue)

        return {'c': cData, 'r': red, 'g': green, 'b': blue, 'l': luminance}

    def read_data(self):
        """
        Get all sensor readings.
        """
        read_start = self._get_time()
        try:
            data = self.read_luminance()
        except IOError:
            data = {'c': None, 'r': None, 'g': None, 'b': None, 'l': None}
        read_time = (self._get_time() - read_start) / 5
        data = [
            (self._name, 'red_luminosity', data['r'], read_time),
            (self._name, 'green_luminosity', data['g'], read_time),
            (self._name, 'blue_luminosity', data['b'], read_time),
            (self._name, 'clear_luminosity', data['c'], read_time),
            (self._name, 'ambient_luminosity', data['l'], read_time),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'red_luminosity': {
                'type': 'gauge',
                'unit': 'lx',
                'precision': 1,
                'range_low': 0,
                'range_high': 40000,
                'sensor': self.DEVICE_NAME
            },
            'green_luminosity': {
                'type': 'gauge',
                'unit': 'lx',
                'precision': 1,
                'range_low': 0,
                'range_high': 40000,
                'sensor': self.DEVICE_NAME
            },
            'blue_luminosity': {
                'type': 'gauge',
                'unit': 'lx',
                'precision': 1,
                'range_low': 0,
                'range_high': 40000,
                'sensor': self.DEVICE_NAME
            },
            'ambient_luminosity': {
                'type': 'gauge',
                'unit': 'lx',
                'precision': 1,
                'range_low': 0,
                'range_high': 40000,
                'sensor': self.DEVICE_NAME
            },
            'clear_luminosity': {
                'type': 'gauge',
                'unit': 'lx',
                'precision': 1,
                'range_low': 0,
                'range_high': 40000,
                'sensor': self.DEVICE_NAME
            },
        }
