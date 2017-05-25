from robophery.interface.i2c import I2cModule

# I2C address of the device
BME280_DEFAULT_ADDRESS = 0x77

# BME280 Register Map
BME280_DIG_T1_LSB_REG = 0x88  # Calibration Data
BME280_DIG_T1_MSB_REG = 0x89  # Calibration Data
BME280_DIG_T2_LSB_REG = 0x8A  # Calibration Data
BME280_DIG_T2_MSB_REG = 0x8B  # Calibration Data
BME280_DIG_T3_LSB_REG = 0x8C  # Calibration Data
BME280_DIG_T3_MSB_REG = 0x8D  # Calibration Data
BME280_DIG_P1_LSB_REG = 0x8E  # Calibration Data
BME280_DIG_P1_MSB_REG = 0x8F  # Calibration Data
BME280_DIG_P2_LSB_REG = 0x90  # Calibration Data
BME280_DIG_P2_MSB_REG = 0x91  # Calibration Data
BME280_DIG_P3_LSB_REG = 0x92  # Calibration Data
BME280_DIG_P3_MSB_REG = 0x93  # Calibration Data
BME280_DIG_P4_LSB_REG = 0x94  # Calibration Data
BME280_DIG_P4_MSB_REG = 0x95  # Calibration Data
BME280_DIG_P5_LSB_REG = 0x96  # Calibration Data
BME280_DIG_P5_MSB_REG = 0x97  # Calibration Data
BME280_DIG_P6_LSB_REG = 0x98  # Calibration Data
BME280_DIG_P6_MSB_REG = 0x99  # Calibration Data
BME280_DIG_P7_LSB_REG = 0x9A  # Calibration Data
BME280_DIG_P7_MSB_REG = 0x9B  # Calibration Data
BME280_DIG_P8_LSB_REG = 0x9C  # Calibration Data
BME280_DIG_P8_MSB_REG = 0x9D  # Calibration Data
BME280_DIG_P9_LSB_REG = 0x9E  # Calibration Data
BME280_DIG_P9_MSB_REG = 0x9F  # Calibration Data
BME280_DIG_H1_REG = 0xA1  # Calibration Data
BME280_CHIP_ID_REG = 0xD0  # Chip ID
BME280_RST_REG = 0xE0  # Softreset Register
BME280_DIG_H2_LSB_REG = 0xE1  # Calibration Data
BME280_DIG_H2_MSB_REG = 0xE2  # Calibration Data
BME280_DIG_H3_REG = 0xE3  # Calibration Data
BME280_DIG_H4_MSB_REG = 0xE4  # Calibration Data
BME280_DIG_H4_LSB_REG = 0xE5  # Calibration Data
BME280_DIG_H5_MSB_REG = 0xE6  # Calibration Data
BME280_DIG_H6_REG = 0xE7  # Calibration Data
BME280_CTRL_HUMIDITY_REG = 0xF2  # Control Humidity Register
BME280_STAT_REG = 0xF3  # Status Register
BME280_CTRL_MEAS_REG = 0xF4  # Control Measure Register
BME280_CONFIG_REG = 0xF5  # Configuration Register
BME280_PRESSURE_MSB_REG = 0xF7  # Pressure MSB
BME280_PRESSURE_LSB_REG = 0xF8  # Pressure LSB
BME280_PRESSURE_XLSB_REG = 0xF9  # Pressure XLSB
BME280_TEMPERATURE_MSB_REG = 0xFA  # Temperature MSB
BME280_TEMPERATURE_LSB_REG = 0xFB  # Temperature LSB
BME280_TEMPERATURE_XLSB_REG = 0xFC  # Temperature XLSB
BME280_HUMIDITY_MSB_REG = 0xFD  # Humidity MSB
BME280_HUMIDITY_LSB_REG = 0xFE  # Humidity LSB

# BME280 Control Humidity Register Configuration
BME280_H_OVERSAMPLE_NONE = 0x00  # Skipped
BME280_H_OVERSAMPLE_1 = 0x01  # Oversampling x 1
BME280_H_OVERSAMPLE_2 = 0x02  # Oversampling x 2
BME280_H_OVERSAMPLE_4 = 0x03  # Oversampling x 4
BME280_H_OVERSAMPLE_8 = 0x04  # Oversampling x 8
BME280_H_OVERSAMPLE_16 = 0x05  # Oversampling x 16

# BME280 Control Measure Register Configuration
BME280_P_OVERSAMPLE_NONE = 0x00  # Skipped
BME280_P_OVERSAMPLE_1 = 0x20  # Oversampling x 1
BME280_P_OVERSAMPLE_2 = 0x40  # Oversampling x 2
BME280_P_OVERSAMPLE_4 = 0x60  # Oversampling x 4
BME280_P_OVERSAMPLE_8 = 0x80  # Oversampling x 8
BME280_P_OVERSAMPLE_16 = 0xA0  # Oversampling x 16
BME280_T_OVERSAMPLE_NONE = 0x00  # Skipped
BME280_T_OVERSAMPLE_1 = 0x04  # Oversampling x 1
BME280_T_OVERSAMPLE_2 = 0x08  # Oversampling x 2
BME280_T_OVERSAMPLE_4 = 0x0C  # Oversampling x 4
BME280_T_OVERSAMPLE_8 = 0x10  # Oversampling x 8
BME280_T_OVERSAMPLE_16 = 0x14  # Oversampling x 16
BME280_MODE_SLEEP = 0x00  # Sleep Mode
BME280_MODE_FORCED = 0x01  # Forced Mode
BME280_MODE_NORMAL = 0x03  # Normal Mode

# BME280 Configuration Register
BME280_STANDBY_MS_0_5 = 0x00  # Standby Time = 0.5ms
BME280_STANDBY_MS_10 = 0xC0  # Standby Time = 10ms
BME280_STANDBY_MS_20 = 0xD0  # Standby Time = 20ms
BME280_STANDBY_MS_62_5 = 0x20  # Standby Time = 62.5ms
BME280_STANDBY_MS_125 = 0x40  # Standby Time = 125ms
BME280_STANDBY_MS_250 = 0x60  # Standby Time = 250ms
BME280_STANDBY_MS_500 = 0x80  # Standby Time = 500ms
BME280_STANDBY_MS_1000 = 0xA0  # Standby Time = 1000ms
BME280_FILTER_OFF = 0x00  # Filter Off
BME280_FILTER_X2 = 0x04  # Filter Coefficient = 2
BME280_FILTER_X4 = 0x08  # Filter Coefficient = 4
BME280_FILTER_X8 = 0x0C  # Filter Coefficient = 8
BME280_FILTER_X16 = 0x10  # Filter Coefficient = 16
BME280_SPI3_EN = 0x01  # Enables 3-wire SPI interface


class Bme280Module(I2cModule):

    DEVICE_NAME = 'bme280'

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', BME280_DEFAULT_ADDRESS)
        super(Bme280Module, self).__init__(*args, **kwargs)

    def read_pres_temp_coeff(self):
        """
        Read data back from BME280_DIG_T1_LSB_REG(0x88), 24 bytes
        """
        b1 = self.readList(BME280_DIG_T1_LSB_REG, 24)

        # Temp coefficients
        self.dig_T1 = b1[1] * 256 + b1[0]

        self.dig_T2 = b1[3] * 256 + b1[2]
        if self.dig_T2 > 32767:
            self.dig_T2 -= 65536

        self.dig_T3 = b1[5] * 256 + b1[4]
        if self.dig_T3 > 32767:
            self.dig_T3 -= 65536

        # Pressure coefficients
        self.dig_P1 = b1[7] * 256 + b1[6]

        self.dig_P2 = b1[9] * 256 + b1[8]
        if self.dig_P2 > 32767:
            self.dig_P2 -= 65536

        self.dig_P3 = b1[11] * 256 + b1[10]
        if self.dig_P3 > 32767:
            self.dig_P3 -= 65536

        self.dig_P4 = b1[13] * 256 + b1[12]
        if self.dig_P4 > 32767:
            self.dig_P4 -= 65536

        self.dig_P5 = b1[15] * 256 + b1[14]
        if self.dig_P5 > 32767:
            self.dig_P5 -= 65536

        self.dig_P6 = b1[17] * 256 + b1[16]
        if self.dig_P6 > 32767:
            self.dig_P6 -= 65536

        self.dig_P7 = b1[19] * 256 + b1[18]
        if self.dig_P7 > 32767:
            self.dig_P7 -= 65536

        self.dig_P8 = b1[21] * 256 + b1[20]
        if self.dig_P8 > 32767:
            self.dig_P8 -= 65536

        self.dig_P9 = b1[23] * 256 + b1[22]
        if self.dig_P9 > 32767:
            self.dig_P9 -= 65536

    def read_hum_coeff(self):
        """Read data back from BME280_DIG_H1_REG(0xA1), 1 byte"""
        self.dig_H1 = self.readU8(BME280_DIG_H1_REG)

        """Read data back from BME280_DIG_H2_LSB_REG(0xE1), 7 bytes"""
        b1 = self.readList(BME280_DIG_H2_LSB_REG, 7)

        # Humidity coefficients
        self.dig_H2 = b1[1] * 256 + b1[0]
        if self.dig_H2 > 32767:
            self.dig_H2 -= 65536

        self.dig_H3 = (b1[2] & 0xFF)

        self.dig_H4 = (b1[3] * 16) + (b1[4] & 0xF)
        if self.dig_H4 > 32767:
            self.dig_H4 -= 65536

        self.dig_H5 = (b1[4] / 16) + (b1[5] * 16)
        if self.dig_H5 > 32767:
            self.dig_H5 -= 65536

        self.dig_H6 = b1[6]
        if self.dig_H6 > 127:
            self.dig_H6 -= 256

    def write_configuration(self):
        """
        Select the Control Humidity Register from the given provided value
        """
        HUMIDITY_SAMPLE = (BME280_H_OVERSAMPLE_1)
        self.write8(BME280_CTRL_HUMIDITY_REG, HUMIDITY_SAMPLE)

        # Select the Control Measure Register from the given provided value
        PRES_TEMP_SAMPLE = (BME280_P_OVERSAMPLE_1 |
                            BME280_T_OVERSAMPLE_1 | BME280_MODE_NORMAL)
        self.write8(BME280_CTRL_MEAS_REG, PRES_TEMP_SAMPLE)

        TIME_CONFIG = (BME280_STANDBY_MS_1000 | BME280_FILTER_OFF)
        self.write8(BME280_CONFIG_REG, TIME_CONFIG)

    def read_raw_data(self):
        """
        Read data back from BME280_PRESSURE_MSB_REG(0xF7), 8 bytes
        Pressure MSB, Pressure LSB, Pressure xLSB, Temperature MSB,
        Temperature LSB, Temperature xLSB, Humidity MSB, Humidity LSB.
        """
        data = self.readList(BME280_PRESSURE_MSB_REG, 8)

        # Convert pressure and temperature data to 19-bits
        self.adc_p = ((data[0] * 65536) +
                      (data[1] * 256) + (data[2] & 0xF0)) / 16
        self.adc_t = ((data[3] * 65536) +
                      (data[4] * 256) + (data[5] & 0xF0)) / 16

        # Convert the humidity data
        self.adc_h = data[6] * 256 + data[7]

    def result_calculation(self):
        """
        Offset calculations for the final pressure, humidity and temperature
        """

        # Temperature offset calculations
        var1 = ((self.adc_t) / 16384.0 -
                (self.dig_T1) / 1024.0) * (self.dig_T2)
        var2 = (((self.adc_t) / 131072.0 - (self.dig_T1) / 8192.0) *
                ((self.adc_t) / 131072.0 - (self.dig_T1) / 8192.0)) * (self.dig_T3)
        t_fine = (var1 + var2)
        temp = (var1 + var2) / 5120.0

        # Pressure offset calculations
        var1 = (t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * (self.dig_P6) / 32768.0
        var2 = var2 + var1 * (self.dig_P5) * 2.0
        var2 = (var2 / 4.0) + ((self.dig_P4) * 65536.0)
        var1 = ((self.dig_P3) * var1 * var1 / 524288.0 +
                (self.dig_P2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * (self.dig_P1)
        p = 1048576.0 - self.adc_p
        p = (p - (var2 / 4096.0)) * 6250.0 / var1
        var1 = (self.dig_P9) * p * p / 2147483648.0
        var2 = p * (self.dig_P8) / 32768.0
        pressure = (p + (var1 + var2 + (self.dig_P7)) / 16.0) # Pa

        # Humidity offset calculations
        var_H = ((t_fine) - 76800.0)
        var_H = (self.adc_h - (self.dig_H4 * 64.0 + self.dig_H5 / 16384.0 * var_H)) * (self.dig_H2 /
                                                                                       65536.0 * (1.0 + self.dig_H6 / 67108864.0 * var_H * (1.0 + self.dig_H3 / 67108864.0 * var_H)))
        humidity = var_H * (1.0 - self.dig_H1 * var_H / 524288.0)
        if humidity > 100.0:
            humidity = 100.0
        elif humidity < 0.0:
            humidity = 0.0

        return {'h': humidity, 'p': pressure, 't': temp}

    def read_data(self):
        """
        Get all sensor readings.
        """
        read_start = self._get_time()
        try:
            self.read_pres_temp_coeff()
            self.read_hum_coeff()
            self.write_configuration()
            self.read_raw_data()
            data = self.result_calculation()
        except IOError:
            data = {'h': None, 'p': None, 't': None}
        read_time = (self._get_time() - read_start) / 3
        data = [
            (self._name, 'temperature', data['t'], read_time),
            (self._name, 'humidity', data['h'], read_time),
            (self._name, 'pressure', data['p'], read_time),
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
                'precision': 1,
                'range_low': -40,
                'range_high': 85,
                'sensor': self.DEVICE_NAME
            },
            'humidity': {
                'type': 'gauge',
                'unit': 'RH',
                'precision': 3,
                'range_low': 0,
                'range_high': 100,
                'sensor': self.DEVICE_NAME
            },
            'pressure': {
                'type': 'gauge',
                'unit': 'Pa',
                'precision': 100,
                'range_low': 30000,
                'range_high': 110000,
                'sensor': self.DEVICE_NAME
            }
        }
