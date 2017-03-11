#The MIT License (MIT)
#Copyright (c) 2016 Scott Williamson
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
from robophery.module.i2c.base import I2cModule


class Ina219Module(I2cModule):
    """
    Module for INA219 current and voltage sensor.
    """
    DEVICE_NAME = 'i2c-ina219'
    # INA219 default address
    DEVICE_ADDR = 0x40 
    INA219_READ = 0x01

    INA219_REG_CONFIG                      = 0x00
    INA219_CONFIG_RESET                    = 0x8000  # Reset Bit
    INA219_CONFIG_BVOLTAGERANGE_MASK       = 0x2000  # Bus Voltage Range Mask
    INA219_CONFIG_BVOLTAGERANGE_16V        = 0x0000  # 0-16V Range
    INA219_CONFIG_BVOLTAGERANGE_32V        = 0x2000  # 0-32V Range

    INA219_CONFIG_GAIN_MASK                = 0x1800  # Gain Mask
    INA219_CONFIG_GAIN_1_40MV              = 0x0000  # Gain 1, 40mV Range
    INA219_CONFIG_GAIN_2_80MV              = 0x0800  # Gain 2, 80mV Range
    INA219_CONFIG_GAIN_4_160MV             = 0x1000  # Gain 4, 160mV Range
    INA219_CONFIG_GAIN_8_320MV             = 0x1800  # Gain 8, 320mV Range

    INA219_CONFIG_BADCRES_MASK             = 0x0780  # Bus ADC Resolution Mask
    INA219_CONFIG_BADCRES_9BIT             = 0x0080  # 9-bit bus res = 0..511
    INA219_CONFIG_BADCRES_10BIT            = 0x0100  # 10-bit bus res = 0..1023
    INA219_CONFIG_BADCRES_11BIT            = 0x0200  # 11-bit bus res = 0..2047
    INA219_CONFIG_BADCRES_12BIT            = 0x0400  # 12-bit bus res = 0..4097

    INA219_CONFIG_SADCRES_MASK             = 0x0078  # Shunt ADC Resolution and Averaging Mask
    INA219_CONFIG_SADCRES_9BIT_1S_84US     = 0x0000  # 1 x 9-bit shunt sample
    INA219_CONFIG_SADCRES_10BIT_1S_148US   = 0x0008  # 1 x 10-bit shunt sample
    INA219_CONFIG_SADCRES_11BIT_1S_276US   = 0x0010  # 1 x 11-bit shunt sample
    INA219_CONFIG_SADCRES_12BIT_1S_532US   = 0x0018  # 1 x 12-bit shunt sample
    INA219_CONFIG_SADCRES_12BIT_2S_1060US  = 0x0048  # 2 x 12-bit shunt samples averaged together
    INA219_CONFIG_SADCRES_12BIT_4S_2130US  = 0x0050  # 4 x 12-bit shunt samples averaged together
    INA219_CONFIG_SADCRES_12BIT_8S_4260US  = 0x0058  # 8 x 12-bit shunt samples averaged together
    INA219_CONFIG_SADCRES_12BIT_16S_8510US = 0x0060  # 16 x 12-bit shunt samples averaged together
    INA219_CONFIG_SADCRES_12BIT_32S_17MS   = 0x0068  # 32 x 12-bit shunt samples averaged together
    INA219_CONFIG_SADCRES_12BIT_64S_34MS   = 0x0070  # 64 x 12-bit shunt samples averaged together
    INA219_CONFIG_SADCRES_12BIT_128S_69MS  = 0x0078  # 128 x 12-bit shunt samples averaged together

    INA219_CONFIG_MODE_MASK                = 0x0007  # Operating Mode Mask
    INA219_CONFIG_MODE_POWERDOWN           = 0x0000
    INA219_CONFIG_MODE_SVOLT_TRIGGERED     = 0x0001
    INA219_CONFIG_MODE_BVOLT_TRIGGERED     = 0x0002
    INA219_CONFIG_MODE_SANDBVOLT_TRIGGERED = 0x0003
    INA219_CONFIG_MODE_ADCOFF              = 0x0004
    INA219_CONFIG_MODE_SVOLT_CONTINUOUS    = 0x0005
    INA219_CONFIG_MODE_BVOLT_CONTINUOUS    = 0x0006
    INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS = 0x0007

    INA219_REG_SHUNTVOLTAGE                = 0x01 # SHUNT VOLTAGE REGISTER (R)
    INA219_REG_BUSVOLTAGE                  = 0x02 # BUS VOLTAGE REGISTER (R)
    INA219_REG_POWER                       = 0x03 # POWER REGISTER (R)
    INA219_REG_CURRENT                     = 0x04 # CURRENT REGISTER (R)
    INA219_REG_CALIBRATION                 = 0x05 # CALIBRATION REGISTER (R/W)


    def __init__(self, *args, **kwargs):
        self._addr = self.DEVICE_ADDR
        super(Ina219Module, self).__init__(*args, **kwargs)
        self._set_calibration_32v_2a()

    
    def _twos_to_int(self, val, len):
        # Convert twos compliment to integer
        if(val & (1 << len - 1)):
            val = val - (1<<len)
        return val


    def _set_calibration_32v_2a(self):
        self._cal_value = 4096
        self._current_divider_ma = 10 # Current LSB = 100uA per bit (1000/100 = 10)
        self._power_divider_mw = 2 # Power LSB = 1mW per bit (2/1)

        # Set Calibration register to 'Cal' calculated above    
        bytes = [(self._cal_value >> 8) & 0xFF, self._cal_value & 0xFF]
        self.writeList(self.INA219_REG_CALIBRATION, bytes)
        
        # Set Config register to take into account the settings above
        config = self.INA219_CONFIG_BVOLTAGERANGE_32V | \
                 self.INA219_CONFIG_GAIN_8_320MV | \
                 self.INA219_CONFIG_BADCRES_12BIT | \
                 self.INA219_CONFIG_SADCRES_12BIT_1S_532US | \
                 self.INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS
        
        bytes = [(config >> 8) & 0xFF, config & 0xFF]
        self.writeList(self.INA219_REG_CONFIG, bytes)


    def _get_raw_bus_voltage(self):
        result = self.readU16(self.INA219_REG_BUSVOLTAGE)
        
        # Shift to the right 3 to drop CNVR and OVF and multiply by LSB
        return (result >> 3) * 4

        
    def _get_raw_shunt_voltage(self):
        result = self.readList(self.INA219_REG_SHUNTVOLTAGE,2)
        if (result[0] >> 7 == 1):
            testint = (result[0]*256 + result[1])
            othernew = self._twos_to_int(testint, 16)
            return othernew
        else:
            return (result[0] << 8) | (result[1])


    def _get_raw_current(self):
        # Sometimes a sharp load will reset the INA219, which will
        # reset the cal register, meaning CURRENT and POWER will
        # not be available ... avoid this by always setting a cal
        # value even if it's an unfortunate extra step
        bytes = [(self._cal_value >> 8) & 0xFF, self._cal_value & 0xFF]
        self.writeList(self.INA219_REG_CALIBRATION, bytes)
        # Now we can safely read the CURRENT register!
        result = self.readList(self.INA219_REG_CURRENT,2)
        if (result[0] >> 7 == 1):
            testint = (result[0]*256 + result[1])
            othernew = self._twos_to_int(testint, 16)
            return othernew
        else:
            return (result[0] << 8) | (result[1])


    def _get_raw_power(self):
        result = self.readList(self.INA219_REG_POWER,2)
        if (result[0] >> 7 == 1):
            testint = (result[0]*256 + result[1])
            othernew = self._twos_to_int(testint, 16)
            return othernew
        else:
            return (result[0] << 8) | (result[1])


    def get_shunt_voltage(self):
        """
        Get shunt voltage (mV)
        """
        value = self._get_raw_shunt_voltage()
        return value * 0.01

        
    def get_bus_voltage(self):
        """
        Get bus voltage (V)
        """
        value = self._get_raw_bus_voltage()
        return value * 0.001

        
    def get_current(self):
        """
        Get current (mA)
        """
        valueDec = self._get_raw_current()
        valueDec /= self._current_divider_ma
        return valueDec

        
    def get_power(self):
        """
        Get power (mW)
        """
        valueDec = self._get_raw_power()
        valueDec /= self._power_divider_mw
        return valueDec


    def read_data(self):
        """
        Get all sensor readings.
        """
        return [
            (self._name, 'voltage', self.get_shunt_voltage()),
            (self._name, 'current', self.get_current()),
            (self._name, 'power', self.get_power()),
        ]
