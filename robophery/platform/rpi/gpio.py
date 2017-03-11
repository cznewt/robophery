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

from robophery.platform.gpio import GpioInterface

"""
try:
    import RPi.GPIO
except:
    raise RuntimeError("Cannot load RPi.GPIO library. Please install the library.")
"""

class RaspberryPiGpioInterface(GpioInterface):
    """
    GPIO implementation for the Raspberry Pi using the RPi.GPIO library.
    """

    def __init__(self, *args, **kwargs):
        self._mode = kwargs.get('mode', None)
        """
        #Temp
        self._bus = RPi.GPIO
        # Suppress warnings about GPIO in use.
        self._bus.setwarnings(False)
        # Setup board pin mode.
        if self._mode == self._bus.BOARD or self._mode == self._bus.BCM:
            self._bus.setmode(self._mode)
        elif self._mode is not None:
            raise ValueError('Unexpected value for mode.  Must be BOARD or BCM.')
        else:
            self._bus.setmode(self._bus.BOARD)

        self._dir_mapping = { self.GPIO_MODE_OUT: self._bus.OUT,
                              self.GPIO_MODE_IN: self._bus.IN }
        self._pud_mapping = { self.GPIO_PUD_OFF: self._bus.PUD_OFF,
                              self.GPIO_PUD_DOWN: self._bus.PUD_DOWN,
                              self.GPIO_PUD_UP: self._bus.PUD_UP }
        self._edge_mapping = { self.GPIO_EVENT_RISING: self._bus.RISING,
                               self.GPIO_EVENT_FALLING: self._bus.FALLING,
                               self.GPIO_EVENT_BOTH: self._bus.BOTH }
        """
        super(RaspberryPiGpioInterface, self).__init__(*args, **kwargs)


    def setup_pin(self, pin, mode, pull_up_down=None):
        """
        Set the input or output mode for a specified pin. Mode should be
        either OUTPUT or INPUT.
        """
        if pull_up_down == None:
            pull_up_down = self.GPIO_PUD_OFF
        #Temp
        #self._bus.setup(pin, self._dir_mapping[mode],
        #                     pull_up_down=self._pud_mapping[pull_up_down])


    def output(self, pin, value):
        """
        Set the specified pin the provided high/low value. Value should be
        either HIGH/LOW or a boolean (true = high).
        """
        self._bus.output(pin, value)


    def input(self, pin):
        """
        Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        return self._bus.input(pin)


    def input_pins(self, pins):
        """
        Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        return [self._bus.input(pin) for pin in pins]


    def add_event_detect(self, pin, edge, callback=None, bouncetime=-1):
        """
        Enable edge detection events for a particular GPIO channel. Pin 
        should be type IN. Edge must be RISING, FALLING or BOTH. Callback is a
        function for the event. Bouncetime is switch bounce timeout in ms for
        callback.
        """
        kwargs = {}
        if callback:
            kwargs['callback']=callback
        if bouncetime > 0:
            kwargs['bouncetime']=bouncetime
        self._bus.add_event_detect(pin, self._edge_mapping[edge], **kwargs)


    def remove_event_detect(self, pin):
        """
        Remove edge detection for a particular GPIO channel. Pin should be
        type IN.
        """
        self._bus.remove_event_detect(pin)


    def add_event_callback(self, pin, callback):
        """Add a callback for an event already defined using add_event_detect().
        Pin should be type IN.
        """
        self._bus.add_event_callback(pin, callback)


    def event_detected(self, pin):
        """
        Returns True if an edge has occured on a given GPIO. You need to 
        enable edge detection using add_event_detect() first. Pin should be
        type IN.
        """
        return self._bus.event_detected(pin)


    def wait_for_edge(self, pin, edge):
        """
        Wait for an edge. Pin should be type IN. Edge must be RISING,
        FALLING or BOTH.
        """
        self._bus.wait_for_edge(pin, self._edge_mapping[edge])


    def cleanup(self, pin=None):
        """
        Clean up GPIO event detection for specific pin, or all pins if none 
        is specified.
        """
        if pin is None:
            self._bus.cleanup()
        else:
            self._bus.cleanup(pin)
