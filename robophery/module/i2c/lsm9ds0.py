from robophery.interface.i2c import I2cModule

# I2C Address of the device
LSM9DS0_MAG_ADDRESS = 0x1E
LSM9DS0_ACCL_ADDRESS = 0x1E
LSM9DS0_GYRO_ADDRESS = 0x6A

# LSM9DS0 gyrometer registers
LSM9DS0_WHO_AM_I_G = 0x0F
LSM9DS0_CTRL_REG1_G = 0x20
LSM9DS0_CTRL_REG4_G = 0x23
LSM9DS0_OUT_X_L_G = 0x28
LSM9DS0_OUT_X_H_G = 0x29
LSM9DS0_OUT_Y_L_G = 0x2A
LSM9DS0_OUT_Y_H_G = 0x2B
LSM9DS0_OUT_Z_L_G = 0x2C
LSM9DS0_OUT_Z_H_G = 0x2D

# Gyro Datarate & Bandwidth configuration
LSM9DS0_GYRO_DR_95 = 0x00  # ODR = 95 Hz
LSM9DS0_GYRO_DR_190 = 0x40  # ODR = 190 Hz
LSM9DS0_GYRO_DR_380 = 0x80  # ODR = 380 Hz
LSM9DS0_GYRO_DR_760 = 0xC0  # ODR = 760 Hz
LSM9DS0_GYRO_BW_12_5 = 0x00  # Cutoff = 12.5
LSM9DS0_GYRO_BW_25 = 0x10  # Cutoff = 25
LSM9DS0_GYRO_BW_50 = 0x20  # Cutoff = 50
LSM9DS0_GYRO_BW_70 = 0x30  # Cutoff = 70

# Gyro Power & Axis configuration
LSM9DS0_GYRO_PD = 0x00  # Power down mode, Axis disabled
LSM9DS0_GYRO_ND = 0x08  # Normal mode
LSM9DS0_GYRO_XAXIS = 0x04  # X-Axis enabled
LSM9DS0_GYRO_YAXIS = 0x02  # Y-Axis enabled
LSM9DS0_GYRO_ZAXIS = 0x01  # Z-Axis enabled

# Gyro Full-scale selection & Mode configuration
LSM9DS0_GYRO_DEFAULT = 0x00  # Continuous update, LSB first, Normal mode
LSM9DS0_GYRO_BDU = 0x80  # Output registers not updated until MSB and LSB read
LSM9DS0_GYRO_BLE_MSB = 0x40  # MSB first
LSM9DS0_GYRO_SCALE_245 = 0x00  # 245 dps
LSM9DS0_GYRO_SCALE_500 = 0x10  # 500 dps
LSM9DS0_GYRO_SCALE_2000 = 0x20  # 2000 dps
LSM9DS0_GYRO_ST_0 = 0x02  # Self-Test 0
LSM9DS0_GYRO_ST_1 = 0x06  # Self-Test 1

# Magnetometer addresses
LSM9DS0_STATUS_REG_M = 0x07
LSM9DS0_OUT_X_L_M = 0x08
LSM9DS0_OUT_X_H_M = 0x09
LSM9DS0_OUT_Y_L_M = 0x0A
LSM9DS0_OUT_Y_H_M = 0x0B
LSM9DS0_OUT_Z_L_M = 0x0C
LSM9DS0_OUT_Z_H_M = 0x0D

# Shared addresses between Magnetometer & Accelerometer
LSM9DS0_WHO_AM_I_XM = 0x0F
LSM9DS0_CTRL_REG1_XM = 0x20
LSM9DS0_CTRL_REG2_XM = 0x21
LSM9DS0_CTRL_REG5_XM = 0x24
LSM9DS0_CTRL_REG6_XM = 0x25
LSM9DS0_CTRL_REG7_XM = 0x26

# Accelerometer addresses
LSM9DS0_OUT_X_L_A = 0x28
LSM9DS0_OUT_X_H_A = 0x29
LSM9DS0_OUT_Y_L_A = 0x2A
LSM9DS0_OUT_Y_H_A = 0x2B
LSM9DS0_OUT_Z_L_A = 0x2C
LSM9DS0_OUT_Z_H_A = 0x2D

# Accl Datarate configuration
LSM9DS0_ACCL_DR_PD = 0x00  # Power down mode
LSM9DS0_ACCL_DR_3_125 = 0x10  # ODR = 3.125 Hz
LSM9DS0_ACCL_DR_6_25 = 0x20  # ODR = 6.25 Hz
LSM9DS0_ACCL_DR_12_5 = 0x30  # ODR = 12.5 Hz
LSM9DS0_ACCL_DR_25 = 0x40  # ODR = 25 Hz
LSM9DS0_ACCL_DR_50 = 0x50  # ODR = 50 Hz
LSM9DS0_ACCL_DR_100 = 0x60  # ODR = 100 Hz
LSM9DS0_ACCL_DR_200 = 0x70  # ODR = 200 Hz
LSM9DS0_ACCL_DR_400 = 0x80  # ODR = 400 Hz
LSM9DS0_ACCL_DR_800 = 0x90  # ODR = 800 Hz
LSM9DS0_ACCL_DR_1600 = 0xA0  # ODR = 1600 Hz

# Accl Data update & Axis configuration
LSM9DS0_ACCL_BDU = 0x00  # Continuous update, Axis disabled
LSM9DS0_ACCL_XAXIS = 0x04  # X-Axis enabled
LSM9DS0_ACCL_YAXIS = 0x02  # Y-Axis enabled
LSM9DS0_ACCL_ZAXIS = 0x01  # Z-Axis enabled

# Acceleration Full-scale selection
LSM9DS0_ACCL_RANGE_2G = 0x00  # Full scale = +/-2g
LSM9DS0_ACCL_RANGE_4G = 0x08  # Full scale = +/-4g
LSM9DS0_ACCL_RANGE_6G = 0x10  # Full scale = +/-6g
LSM9DS0_ACCL_RANGE_8G = 0x18  # Full scale = +/-8g
LSM9DS0_ACCL_RANGE_16G = 0x20  # Full scale = +/-16g

# Magnetic Datarate configuration
LSM9DS0_MAG_DR_3_125 = 0x00  # ODR = 3.125 Hz
LSM9DS0_MAG_DR_6_25 = 0x04  # ODR = 6.25 hz
LSM9DS0_MAG_DR_12_5 = 0x08  # ODR = 12.5 Hz
LSM9DS0_MAG_DR_25 = 0x0C  # ODR = 25 Hz
LSM9DS0_MAG_DR_50 = 0x10  # ODR = 50 Hz
LSM9DS0_MAG_DR_100 = 0x14  # ODR = 100 Hz

# Magnetic Temperature & Resolution configuration
LSM9DS0_MAG_TEMP_DEF = 0x00  # Temperature disabled, Low Resolution
LSM9DS0_MAG_TEMP_EN = 0x80  # Temperature enabled
LSM9DS0_MAG_RES_H = 0x60  # High Resolution

# Magnetic Full-scale selection
LSM9DS0_MAG_GAIN_2 = 0x00  # +/- 2 gauss
LSM9DS0_MAG_GAIN_4 = 0x20  # +/- 4 gauss
LSM9DS0_MAG_GAIN_8 = 0x40  # +/- 8 gauss
LSM9DS0_MAG_GAIN_12 = 0x60  # +/- 12 gauss

# Magnetic Mode selection
LSM9DS0_MAG_FILTER_NRML = 0x00  # Normal Mode
LSM9DS0_MAG_FILTER_REF = 0x40  # Reference signal for filtering
LSM9DS0_MAG_FILTER_RST = 0xC0  # Autoreset on interrupt event
LSM9DS0_MAG_MODE_CNTS = 0x00  # Continuous-conversion mode
LSM9DS0_MAG_MODE_SNGL = 0x01  # Single-conversion mode
LSM9DS0_MAG_MODE_PWR_DWN = 0x02  # Power-down mode


class Lsm9ds0Module(I2cModule):

    def __init__(self, *args, **kwargs):
        super(Lsm9ds0Module, self).__init__(*args, **kwargs)
        self._gyro = self._setup_i2c_iface(kwargs.get('gyro'))
        self._accl = self._setup_i2c_iface(kwargs.get('accl'))
        self._mag = self._setup_i2c_iface(kwargs.get('mag'))

        self.gyro_datarate()
        self.gyro_scale_selection()
        self.accl_datarate()
        self.accl_scale_selection()
        self.mag_datarate()
        self.mag_scale_selection()
        self.mag_mode_selection()

    def gyro_datarate(self):
        """
        Select the data rate of the gyroscope from the given provided values.
        """
        GYRO_DATARATE = (LSM9DS0_GYRO_DR_95 | LSM9DS0_GYRO_BW_12_5 |
                         LSM9DS0_GYRO_ND | LSM9DS0_GYRO_XAXIS |
                         LSM9DS0_GYRO_YAXIS | LSM9DS0_GYRO_ZAXIS)
        self._gyro.write8(LSM9DS0_CTRL_REG1_G, GYRO_DATARATE)

    def gyro_scale_selection(self):
        """
        Select the full-scale values of the gyroscope from the given provided
        values.
        """
        GYRO_SCALE = (LSM9DS0_GYRO_DEFAULT | LSM9DS0_GYRO_SCALE_2000)
        self._gyro.write8(LSM9DS0_CTRL_REG4_G, GYRO_SCALE)

        self._msleep(500)

    def read_gyro(self):
        """
        Read data back from LSM9DS0_OUT_X_L_G(0x28), 2 bytes
        X-Axis Mag LSB, X-Axis Mag MSB
        """
        data0 = self._gyro.readU8(LSM9DS0_OUT_X_L_G)
        data1 = self._gyro.readU8(LSM9DS0_OUT_X_H_G)

        xGyro = data1 * 256 + data0
        if xGyro > 32767:
            xGyro -= 65536

        data0 = self._gyro.readU8(LSM9DS0_OUT_Y_L_G)
        data1 = self._gyro.readU8(LSM9DS0_OUT_Y_H_G)

        yGyro = data1 * 256 + data0
        if yGyro > 32767:
            yGyro -= 65536

        data0 = self._gyro.readU8(LSM9DS0_OUT_Z_L_G)
        data1 = self._gyro.readU8(LSM9DS0_OUT_Z_H_G)

        zGyro = data1 * 256 + data0
        if zGyro > 32767:
            zGyro -= 65536

        return {'x': xGyro, 'y': yGyro, 'z': zGyro}

    def accl_datarate(self):
        """
        Select the data rate of the accelerometer from the given provided
        values.
        """
        ACCL_DATARATE = (LSM9DS0_ACCL_DR_100 | LSM9DS0_ACCL_XAXIS |
                         LSM9DS0_ACCL_YAXIS | LSM9DS0_ACCL_ZAXIS)
        self._accl.write8(LSM9DS0_CTRL_REG1_XM, ACCL_DATARATE)

    def accl_scale_selection(self):
        """
        Select the full-scale values of the accelerometer from the given
        provided values.
        """
        ACCL_SCALE = (LSM9DS0_ACCL_RANGE_2G)
        self._accl.write8(LSM9DS0_CTRL_REG2_XM, ACCL_SCALE)

    def mag_datarate(self):
        """
        Select the data rate of the magnetometer from the given provided
        values.
        """
        MAG_DATARATE = (LSM9DS0_MAG_DR_50 | LSM9DS0_MAG_RES_H)
        self._mag.write8(LSM9DS0_CTRL_REG5_XM, MAG_DATARATE)

    def mag_scale_selection(self):
        """
        Select the full-scale values of the magnetometer from the given
        provided values.
        """
        MAG_SCALE = (LSM9DS0_MAG_GAIN_12)
        self._mag.write8(LSM9DS0_CTRL_REG6_XM, MAG_SCALE)

    def mag_mode_selection(self):
        """
        Select the modes of the magnetometer from the given provided values.
        """
        MAG_MODE = (LSM9DS0_MAG_FILTER_NRML | LSM9DS0_MAG_MODE_CNTS)
        self._mag.write8(LSM9DS0_CTRL_REG7_XM, MAG_MODE)

        self._msleep(500)

    def read_accl(self):
        """
        Read data back from LSM9DS0_OUT_X_L_A(0x28), 2 bytes
        X-Axis Mag LSB, X-Axis Mag MSB
        """
        data0 = self._accl.readU8(LSM9DS0_OUT_X_L_A)
        data1 = self._accl.readU8(LSM9DS0_OUT_X_H_A)

        xAccl = data1 * 256 + data0
        if xAccl > 32767:
            xAccl -= 65536

        data0 = self._accl.readU8(LSM9DS0_OUT_Y_L_A)
        data1 = self._accl.readU8(LSM9DS0_OUT_Y_H_A)

        yAccl = data1 * 256 + data0
        if yAccl > 32767:
            yAccl -= 65536

        data0 = self._accl.readU8(LSM9DS0_OUT_Z_L_A)
        data1 = self._accl.readU8(LSM9DS0_OUT_Z_H_A)

        zAccl = data1 * 256 + data0
        if zAccl > 32767:
            zAccl -= 65536

        return {'x': xAccl, 'y': yAccl, 'z': zAccl}

    def read_mag(self):
        """
        Read data back from LSM9DS0_OUT_X_L_M(0x08), 2 bytes
        X-Axis Mag LSB, X-Axis Mag MSB.
        """
        data0 = self._mag.readU8(LSM9DS0_OUT_X_L_M)
        data1 = self._mag.readU8(LSM9DS0_OUT_X_H_M)

        xMag = data1 * 256 + data0
        if xMag > 32767:
            xMag -= 65536

        data0 = self._mag.readU8(LSM9DS0_OUT_Y_L_M)
        data1 = self._mag.readU8(LSM9DS0_OUT_Y_H_M)

        yMag = data1 * 256 + data0
        if yMag > 32767:
            yMag -= 65536

        data0 = self._mag.readU8(LSM9DS0_OUT_Z_L_M)
        data1 = self._mag.readU8(LSM9DS0_OUT_Z_H_M)

        zMag = data1 * 256 + data0
        if zMag > 32767:
            zMag -= 65536

        return {'x': xMag, 'y': yMag, 'z': zMag}

    def read_data(self):
        """
        Get all sensor readings.
        """
        accl_read_start = self._get_time()
        self.accl_datarate()
        self.accl_scale_selection()
        accl = self.read_accl()
        accl_read_time = (self._get_time() - accl_read_start) / 3

        gyro_read_start = self._get_time()
        self.gyro_datarate()
        self.gyro_scale_selection()
        gyro = self.read_gyro()
        gyro_read_time = (self._get_time() - gyro_read_start) / 3

        mag_read_start = self._get_time()
        self.mag_datarate()
        self.mag_scale_selection()
        self.mag_mode_selection()
        mag = self.read_mag()
        mag_read_time = (self._get_time() - mag_read_start) / 3

        data = [
            (self._name, 'rotation_x', gyro['x'], gyro_read_time),
            (self._name, 'rotation_y', gyro['y'], gyro_read_time),
            (self._name, 'rotation_z', gyro['z'], gyro_read_time),
            (self._name, 'acceleration_x', accl['x'], accl_read_time),
            (self._name, 'acceleration_y', accl['y'], accl_read_time),
            (self._name, 'acceleration_z', accl['z'], accl_read_time),
            (self._name, 'magnetic_field_x', mag['x'], mag_read_time),
            (self._name, 'magnetic_field_y', mag['y'], mag_read_time),
            (self._name, 'magnetic_field_z', mag['z'], mag_read_time),
        ]
        self._log_data(data)
        return data
