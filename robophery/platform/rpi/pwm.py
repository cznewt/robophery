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
from robophery.interface.pwm import PwmInterface

try:
    import RPi.GPIO
except ImportError:
    raise RuntimeError(
        "Cannot load RPi.GPIO library. Please install the library.")


class RaspberryPiPwmInterface(PwmInterface):
    """
    PWM implementation for the Raspberry Pi using the RPi.GPIO PWM library.
    """

    def __init__(self, *args, **kwargs):
        self._bus = RPi.GPIO
        # Suppress warnings about GPIO in use.
        self._bus.setwarnings(False)
        self._bus.setmode(self._bus.BOARD)
        self._pins = {}
        super(RaspberryPiPwmInterface, self).__init__(*args, **kwargs)
        self._log.info("Started interface {0}.".format(self))

    def setup_pin(self, pin, dutycycle, frequency=2000):
        """
        Enable PWM output on specified pin. Set to initial percent duty cycle
        value (0.0 to 100.0) and frequency (in Hz).
        """
        if dutycycle < 0.0 or dutycycle > 100.0:
            raise ValueError(
                'Invalid duty cycle value, must be between 0 to 100.')
        # Make pin an output.
        self._bus.setup(pin, self._bus.GPIO_MODE_OUT)
        # Create PWM instance and save a reference for later access.
        self.pins[pin] = self._bus.PWM(pin, frequency)
        # Start the PWM at the specified duty cycle.
        self.pins[pin].start(dutycycle)

    def set_duty_cycle(self, pin, dutycycle):
        """
        Set percent duty cycle of PWM output on specified pin. Duty cycle must
        be a value 0.0 to 100.0 (inclusive).
        """
        if dutycycle < 0.0 or dutycycle > 100.0:
            raise ValueError(
                'Invalid duty cycle value, must be between 0 to 100.')
        if pin not in self.pins:
            raise ValueError(
                'Pin {0} is not configured as a PWM.'.format(pin))
        self.pins[pin].ChangeDutyCycle(dutycycle)

    def set_frequency(self, pin, frequency):
        """
        Set frequency (in Hz) of PWM output on specified pin.
        """
        if pin not in self.pins:
            raise ValueError(
                'Pin {0} is not configured as a PWM.'.format(pin))
        self.pins[pin].ChangeFrequency(frequency)

    def stop(self, pin):
        """
        Stop PWM output on specified pin.
        """
        if pin not in self.pins:
            raise ValueError(
                'Pin {0} is not configured as a PWM.'.format(pin))
        self.pins[pin].stop()
        del self.pins[pin]
