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


class GpioInterface(object):
    """
    Base class for implementing digital IO bus.
    """

    GPIO_MODE_OUT = 0
    GPIO_MODE_IN = 1
    GPIO_MODE_ALT = 2
    GPIO_MODE_NONE = 3

    GPIO_MODE_OUT_HIGH = True
    GPIO_MODE_OUT_LOW = False

    GPIO_EVENT_NONE = 0
    GPIO_EVENT_RISING = 1
    GPIO_EVENT_FALLING = 2
    GPIO_EVENT_BOTH = 3

    GPIO_PUD_OFF = 0
    GPIO_PUD_DOWN = 1
    GPIO_PUD_UP = 2

    GPIO_DRIVE_LOW = 0
    GPIO_DRIVE_MEDIUM = 1
    GPIO_DRIVE_HIGH = 2

    def __init__(self, *args, **kwargs):
        self._pins = {}


    def setup_pin(self, pin, mode, pull_up_down=None):
        """
        Set the input or output mode for a specified pin. Mode should be
        either OUT or IN.
        """
        raise NotImplementedError


    def get_pin(self, pin):
        """
        Return pin object specified by its number
        """
        raise NotImplementedError


    def output(self, pin, value):
        """
        Set the specified pin the provided high/low value. Value should be
        either HIGH/LOW or a boolean (true = high).
        """
        raise NotImplementedError


    def input(self, pin):
        """
        Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        raise NotImplementedError


    def set_high(self, pin):
        """
        Set the specified pin HIGH.
        """
        self.output(pin, self.GPIO_MODE_OUT_HIGH)


    def set_low(self, pin):
        """
        Set the specified pin LOW.
        """
        self.output(pin, self.GPIO_MODE_OUT_LOW)


    def is_high(self, pin):
        """
        Return true if the specified pin is pulled high.
        """
        return self.input(pin) == self.GPIO_MODE_OUT_HIGH


    def is_low(self, pin):
        """Return true if the specified pin is pulled low."""
        return self.input(pin) == self.GPIO_MODE_OUT_LOW


    def output_pins(self, pins):
        """
        Set multiple pins high or low at once. Pins should be a dict of pin
        name to pin value (HIGH/True for 1, LOW/False for 0). All provided pins
        will be set to the given values.

        General implementation just loops through pins and writes them out
        manually. This is not optimized, but subclasses can choose to implement
        a more optimal batch output implementation. See the MCP230xx class for
        example of optimized implementation.
        """
        for pin, value in iter(pins.items()):
            self.output(pin, value)


    def setup_pins(self, pins):
        """
        Setup multiple pins as inputs or outputs at once. Pins should be a
        dict of pin name to pin type (IN or OUT).
        """
        for pin, value in iter(pins.items()):
            self.setup_pin(pin, value)


    def input_pins(self, pins):
        """
        Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        return [self.input(pin) for pin in pins]


    def add_event_detect(self, pin, edge):
        """
        Enable edge detection events for a particular GPIO channel. Pin 
        should be type IN. Edge must be RISING, FALLING or BOTH.
        """
        raise NotImplementedError


    def remove_event_detect(self, pin):
        """
        Remove edge detection for a particular GPIO channel. Pin should be
        type IN.
        """
        raise NotImplementedError


    def add_event_callback(self, pin, callback):
        """
        Add a callback for an event already defined using add_event_detect().
        Pin should be type IN.
        """
        raise NotImplementedError


    def event_detected(self, pin):
        """
        Returns True if an edge has occured on a given GPIO. You need to 
        enable edge detection using add_event_detect() first. Pin should be 
        type IN.
        """
        raise NotImplementedError


    def wait_for_edge(self, pin, edge):
        """
        Wait for an edge. Pin should be type IN. Edge must be RISING, 
        FALLING or BOTH.
        """
        raise NotImplementedError


    def cleanup(self, pin=None):
        """
        Clean up GPIO event detection for specific pin, or all pins if none 
        is specified.
        """
        raise NotImplementedError


    def _validate_pin(self, pin):
        """
        Raise an exception if pin is outside the range of allowed values.
        """
        if pin < 0 or pin >= self.NUM_GPIO:
            raise ValueError('Invalid GPIO value, must be between 0 and {0}.'.format(self.NUM_GPIO))


    def _bit2(self, src, bit, val):
        bit = 1 << bit
        return (src | bit) if val else (src & ~bit)
