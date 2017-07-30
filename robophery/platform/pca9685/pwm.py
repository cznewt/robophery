# Copyright (c) 2016 Adafruit Industries
# Author: Tony DiCola
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
from __future__ import division
import math

from robophery.interface.pwm import PwmInterface
from robophery.interface.i2c import I2cPort


class Pca9685PwmInterface(PwmInterface):
    """
    PWM implementation for the PCA9685 PWM LED/servo controller.
    """
    DEVICE_NAME = 'pca9685'
    DEVICE_ADDR = 0x40
    AVAILABLE_PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    # Registers
    MODE1 = 0x00
    MODE2 = 0x01
    SUBADR1 = 0x02
    SUBADR2 = 0x03
    SUBADR3 = 0x04
    PRESCALE = 0xFE
    LED0_ON_L = 0x06
    LED0_ON_H = 0x07
    LED0_OFF_L = 0x08
    LED0_OFF_H = 0x09
    ALL_LED_ON_L = 0xFA
    ALL_LED_ON_H = 0xFB
    ALL_LED_OFF_L = 0xFC
    ALL_LED_OFF_H = 0xFD

    # Commands
    RESTART = 0x80
    SLEEP = 0x10
    ALLCALL = 0x01
    INVRT = 0x10
    OUTDRV = 0x04

    def __init__(self, *args, **kwargs):
        super(Pca9685PwmInterface, self).__init__(*args, **kwargs)
        self._pins_available = self.AVAILABLE_PINS
        self._frequency = None
        self._data = self._setup_parent(kwargs['data'])
        self._log.info("Started interface {0}.".format(self))
        self.set_pulse_all(0, 0)
        self._data.write8(self.MODE2, self.OUTDRV)
        self._data.write8(self.MODE1, self.ALLCALL)
        # wait for oscillator
        self._msleep(5)
        mode1 = self._data.readU8(self.MODE1)
        # wake up (reset sleep)
        mode1 = mode1 & ~self.SLEEP
        self._data.write8(self.MODE1, mode1)
        # wait for oscillator
        self._msleep(5)
        self.set_frequency(kwargs.get('frequency', 60))

    def __str__(self):
        return "{0} (using {1}, address: {2:#x}, available pins: {3})".format(
            self._base_name(),
            self._data._iface._name,
            self._data._addr,
            self._pins_available
        )

    def _setup_parent(self, data):
        iface = self._manager._interface[data['iface']]
        addr = data['addr']
        return I2cPort(iface, addr)

    def reset(self):
        self._data.writeRaw8(0x06)

    def setup_pin(self, pin, dutycycle=0, frequency=2000):
        """
        Enable PWM output on specified pin. Set to initial percent duty cycle
        value (0.0 to 100.0) and frequency (in Hz).
        """
        self._use_pin(pin)

    def set_frequency(self, frequency):
        """
        Set the PWM frequency to the provided value in hertz.
        """
        if frequency != self._frequency:
            prescaleval = 25000000.0    # 25MHz
            prescaleval /= 4096.0       # 12-bit
            prescaleval /= float(frequency)
            prescaleval -= 1.0
            self._log.debug(
                'Setting PWM frequency to {0} Hz'.format(frequency))
            self._log.debug('Estimated pre-scale: {0}'.format(prescaleval))
            prescale = int(math.floor(prescaleval + 0.5))
            self._log.debug('Final pre-scale: {0}'.format(prescale))
            oldmode = self._data.readU8(self.MODE1)
            newmode = (oldmode & 0x7F) | 0x10    # sleep
            self._data.write8(self.MODE1, newmode)  # go to sleep
            self._data.write8(self.PRESCALE, prescale)
            self._data.write8(self.MODE1, oldmode)
            self._msleep(5)
            self._data.write8(self.MODE1, oldmode | 0x80)
        self._frequency = frequency

    def set_pulse(self, pin, on=0, off=0):
        """
        Set PWM pulse start and end for output on specified pin.
        """
        self._data.write8(self.LED0_ON_L + 4 * pin, on & 0xFF)
        self._data.write8(self.LED0_ON_H + 4 * pin, on >> 8)
        self._data.write8(self.LED0_OFF_L + 4 * pin, off & 0xFF)
        self._data.write8(self.LED0_OFF_H + 4 * pin, off >> 8)

    def set_pulse_all(self, on=0, off=0):
        """
        Set PWM pulse start and end for output on specified pin.
        """
        self._data.write8(self.ALL_LED_ON_L, on & 0xFF)
        self._data.write8(self.ALL_LED_ON_H, on >> 8)
        self._data.write8(self.ALL_LED_OFF_L, off & 0xFF)
        self._data.write8(self.ALL_LED_OFF_H, off >> 8)
