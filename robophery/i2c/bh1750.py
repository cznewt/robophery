#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from robophery.i2c import I2cModule

class Bh1750Module(I2cModule):
    """ Implement BH1750 communication. """
    # Define some constants from the datasheet
    POWER_DOWN = 0x00 # No active state
    POWER_ON   = 0x01 # Power on
    RESET      = 0x07 # Reset data register value
    # Start measurement at 4lx resolution. Time typically 16ms.
    CONTINUOUS_LOW_RES_MODE = 0x13
    # Start measurement at 1lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_1 = 0x10
    # Start measurement at 0.5lx resolution. Time typically 120ms
    CONTINUOUS_HIGH_RES_MODE_2 = 0x11
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_1 = 0x20
    # Start measurement at 0.5lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_HIGH_RES_MODE_2 = 0x21
    # Start measurement at 1lx resolution. Time typically 120ms
    # Device is automatically set to Power Down after measurement.
    ONE_TIME_LOW_RES_MODE = 0x23


    def __init__(self, kwargs):
        self.name = kwargs.get('name')
        #self.set_bus(kwargs.get('bus'))
        self.resolution_mode = kwargs.get('resolution_mode')
        self.additional_delay = kwargs.get('additional_delay')
        #TODO make this as kwarg
        #self.set_addr(0x23)
        self.set_sensitivity()
        self.setup_device(0x23, kwargs.get('bus'))

    def _set_mode(self, mode):
        self.mode = mode
        #self.bus.write_byte(self.addr, self.mode)
        self.writeRaw8(self.mode)

    def set_resolution_mode(self, resolution_mode):
        self.resolution_mode = resolution_mode

    def set_additional_delay(self, additional_delay):
        self.additional_delay = additional_delay

    def power_down(self):
        self._set_mode(self.POWER_DOWN)

    def power_on(self):
        self._set_mode(self.POWER_ON)

    def reset(self):
        self.power_on() #It has to be powered on before resetting
        self._set_mode(self.RESET)

    def cont_low_res(self):
        self._set_mode(self.CONTINUOUS_LOW_RES_MODE)

    def cont_high_res(self):
        self._set_mode(self.CONTINUOUS_HIGH_RES_MODE_1)

    def cont_high_res2(self):
        self._set_mode(self.CONTINUOUS_HIGH_RES_MODE_2)

    def oneshot_low_res(self):
        self._set_mode(self.ONE_TIME_LOW_RES_MODE)

    def oneshot_high_res(self):
        self._set_mode(self.ONE_TIME_HIGH_RES_MODE_1)

    def oneshot_high_res2(self):
        self._set_mode(self.ONE_TIME_HIGH_RES_MODE_2)

    def set_sensitivity(self, sensitivity=69):
        """ Set the sensor sensitivity.
            Valid values are 31 (lowest) to 254 (highest), default is 69.
        """
        if sensitivity < 31:
            self.mtreg = 31
        elif sensitivity > 254:
            self.mtreg = 254
        else:
            self.mtreg = sensitivity
        self.power_on()
        self._set_mode(0x40 | (self.mtreg >> 5))
        self._set_mode(0x60 | (self.mtreg & 0x1f))
        self.power_down()

    def get_result(self):
        """ Return current measurement result in lx. """   
        data = self.readU16(self.mode)
        count = data >> 8 | (data&0xff)<<8
        mode2coeff =  2 if (self.mode & 0x03) == 0x01 else 1
        ratio = 1/(1.2 * (self.mtreg/69.0) * mode2coeff)
        return ratio*count

    def wait_for_result(self):
        basetime = 0.018 if (self.mode & 0x03) == 0x03 else 0.128
        time.sleep(basetime * (self.mtreg/69.0) + self.additional_delay)

    def do_measurement(self, mode):
        """ 
        Perform complete measurement using command
        specified by parameter mode with additional
        delay specified in parameter additional_delay.
        Return output value in Lx.
        """
        self.reset()
        self._set_mode(mode)
        self.wait_for_result()
        return self.get_result()

    @property
    def get_data(self):
        """
        Get the luminosity readings.
        """
        if self.resolution_mode is 0:
            return self.do_measurement(self.ONE_TIME_LOW_RES_MODE)
        elif self.resolution_mode is 1:
            return self.do_measurement(self.ONE_TIME_HIGH_RES_MODE_1)
        elif self.resolution_mode is 2:
            return self.do_measurement(self.ONE_TIME_HIGH_RES_MODE_2)
        else:
            return -1.0

    @property
    def get_meta_data():
        """
        Get the readings meta-data.
        """
        return {
            'luminosity': {
                'type': 'gauge',
                'unit': 'lx',
                'precision': 1,
                'range_low': 1,
                'range_high': 65535,
                'sensor': 'bh1750'
            }
        }
