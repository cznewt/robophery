# Copyright (c) 2014 Adafruit Industries
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

from robophery.platform.pwm import PwmInterface

try:
    import Adafruit_BBIO.PWM
except:
    raise RuntimeError("Cannot load RPi.GPIO library. Please install the library.")

class BeaglebonePwmInterface(PwmInterface):
    """
    PWM implementation for the BeagleBone Black using the Adafruit_BBIO.PWM library.
    """
    AVAILABLE_PINS = [
        'P8_13',
        'P8_19',
        'P8_34',
        'P8_36',
        'P8_45',
        'P8_46',
        'P9_14',
        'P9_16',
        'P9_21',
        'P9_22',
        'P9_28',
        'P9_29',
        'P9_31',
        'P9_42',
    ]


    def __init__(self, *args, **kwargs):
        self._bus = Adafruit_BBIO.PWM
        self._pins_available = self.AVAILABLE_PINS
        super(BeaglebonePwmInterface, self).__init__(*args, **kwargs)


    def setup_pin(self, pin, dutycycle, frequency=2000):
        """
        Enable PWM output on specified pin. Set to initial percent duty cycle
        value (0.0 to 100.0) and frequency (in Hz).
        """
        if dutycycle < 0.0 or dutycycle > 100.0:
            raise ValueError('Invalid duty cycle value, must be between 0.0 to 100.0 (inclusive).')
        self._bus.start(pin, dutycycle, frequency)


    def set_duty_cycle(self, pin, dutycycle):
        """
        Set percent duty cycle of PWM output on specified pin. Duty cycle must
        be a value 0.0 to 100.0 (inclusive).
        """
        if dutycycle < 0.0 or dutycycle > 100.0:
            raise ValueError('Invalid duty cycle value, must be between 0.0 to 100.0 (inclusive).')
        self._bus.set_duty_cycle(pin, dutycycle)


    def set_frequency(self, pin, frequency):
        """
        Set frequency (in Hz) of PWM output on specified pin.
        """
        self._bus.set_frequency(pin, frequency)

    def stop(self, pin):
        """
        Stop PWM output on specified pin.
        """
        self._bus.stop(pin)
