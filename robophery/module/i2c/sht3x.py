# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Based on the BME280 driver with SHT31D changes provided by
# Ralf Mueller, Erfurt
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from robophery.interface.i2c import I2cModule


class Sht3xModule(I2cModule):
    """
    Module for BH1750 light sensor.
    """
    DEVICE_NAME = 'sht3x'
    DEVICE_ADDR = 0x44

    MEAS_HIGHREP_STRETCH = 0x2C06
    MEAS_MEDREP_STRETCH = 0x2C0D
    MEAS_LOWREP_STRETCH = 0x2C10
    MEAS_HIGHREP = 0x2400
    MEAS_MEDREP = 0x240B
    MEAS_LOWREP = 0x2416
    READSTATUS = 0xF32D
    CLEARSTATUS = 0x3041
    SOFTRESET = 0x30A2
    HEATER_ON = 0x306D
    HEATER_OFF = 0x3066

    STATUS_DATA_CRC_ERROR = 0x0001
    STATUS_COMMAND_ERROR = 0x0002
    STATUS_RESET_DETECTED = 0x0010
    STATUS_TEMPERATURE_ALERT = 0x0400
    STATUS_HUMIDITY_ALERT = 0x0800
    STATUS_HEATER_ACTIVE = 0x2000
    STATUS_ALERT_PENDING = 0x8000

    def __init__(self, *args, **kwargs):
        super(Sht3xModule, self).__init__(*args, **kwargs)
        self._data = self._setup_i2c_iface(kwargs.get('data'))

    def _write_command(self, cmd):
        self._data.write8(cmd >> 8, cmd & 0xFF)

    def reset(self):
        self._write_command(self.SOFTRESET)
        self._msleep(10)

    def clear_status(self):
        self._write_command(self.CLEARSTATUS)

    def read_status(self):
        self._write_command(self.READSTATUS)
        buffer = self._data.readList(0, 3)
        stat = buffer[0] << 8 | buffer[1]
        if buffer[2] != self._crc8(buffer[0:2]):
            return None
        return stat

    def is_data_crc_error(self):
        return bool(self.read_status() & self.STATUS_DATA_CRC_ERROR)

    def is_command_error(self):
        return bool(self.read_status() & self.STATUS_COMMAND_ERROR)

    def is_reset_detected(self):
        return bool(self.read_status() & self.STATUS_RESET_DETECTED)

    def is_tracking_temperature_alert(self):
        return bool(self.read_status() & self.STATUS_TEMPERATURE_ALERT)

    def is_tracking_humidity_alert(self):
        return bool(self.read_status() & self.STATUS_HUMIDITY_ALERT)

    def is_heater_active(self):
        return bool(self.read_status() & self.STATUS_HEATER_ACTIVE)

    def is_alert_pending(self):
        return bool(self.read_status() & self.STATUS_ALERT_PENDING)

    def set_heater(self, do_enable=True):
        if do_enable:
            self._write_command(self.HEATER_ON)
        else:
            self._write_command(self.HEATER_OFF)

    def _read_temperature_humidity(self):
        self._write_command(self.MEAS_HIGHREP)
        self._msleep(15)
        buffer = self._data.readList(0, 6)
        if buffer[2] != self._crc8(buffer[0:2]):
            return (float("nan"), float("nan"))
        raw_temperature = buffer[0] << 8 | buffer[1]
        temperature = 175.0 * raw_temperature / 0xFFFF - 45.0

        if buffer[5] != self._crc8(buffer[3:5]):
            return (float("nan"), float("nan"))

        raw_humidity = buffer[3] << 8 | buffer[4]
        humidity = 100.0 * raw_humidity / 0xFFFF

        return (temperature, humidity)

    def _crc8(self, buffer):
        """ Polynomial 0x31 (x8 + x5 +x4 +1) """

        polynomial = 0x31
        crc = 0xFF

        index = 0
        for index in range(0, len(buffer)):
            crc ^= buffer[index]
            for i in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
        return crc & 0xFF

    def read_data(self):
        """
        Query SHT3x to get the humidity and temperature readings.
        """
        read_start = self._get_time()
        try:
            temperature, humidity = self._read_temperature_humidity()
        except IOError:
            temperature = None
            humidity = None
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
                'resolution': 0.015,
                'precision': 0.3,
                'range_low': -40,
                'range_high': 125,
                'sensor': self.DEVICE_NAME
            },
            'humidity': {
                'type': 'gauge',
                'unit': 'RH',
                'resolution': 0.01,
                'precision': 2,
                'range_low': 0,
                'range_high': 100,
                'sensor': self.DEVICE_NAME
            }
        }
