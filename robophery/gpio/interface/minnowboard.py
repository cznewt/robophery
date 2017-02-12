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

import mraa
from robophery.gpio.interface import GpioInterface

class MinnowboardGpioInterface(GpioInterface):
    """
    GPIO implementation for the Minnowboard + MAX using the mraa library
    """
    
    def __init__(self):
        self._bus = mraa

        self._dir_mapping = { self.GPIO_MODE_OUT: self._bus.DIR_OUT,
                              self.GPIO_MODE_IN: self._bus.DIR_IN }
        self._pud_mapping = { self.GPIO_PUD_OFF: self._bus.MODE_STRONG,
                              self.GPIO_PUD_DOWN: self._bus.MODE_PULLDOWN,
                              self.GPIO_PUD_UP: self._bus.MODE_HIZ }
        self._edge_mapping = { self.GPIO_EVENT_RISING: self._bus.EDGE_RISING,
                               self.GPIO_EVENT_FALLING: self._bus.EDGE_FALLING,
                               self.GPIO_EVENT_BOTH: self._bus.EDGE_BOTH }


    def setup(self, pin, mode):
        """
        Set the input or output mode for a specified pin. Mode should be
        either DIR_IN or DIR_OUT.
        """
        self._bus.Gpio.dir(self._bus.Gpio(pin),self._dir_mapping[mode])   


    def output(self, pin, value):
        """
        Set the specified pin the provided high/low value. Value should be
        either 1 (ON or HIGH), or 0 (OFF or LOW) or a boolean.
        """
        self._bus.Gpio.write(self._bus.Gpio(pin), value)

    
    def input(self, pin):
        """
        Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        return self._bus.Gpio.read(self._bus.Gpio(pin))    

    
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
        self._bus.Gpio.isr(self._bus.Gpio(pin), self._edge_mapping[edge], **kwargs)


    def remove_event_detect(self, pin):
        """
        Remove edge detection for a particular GPIO channel. Pin should be
        type IN.
        """
        self._bus.Gpio.isrExit(self._bus.Gpio(pin))


    def wait_for_edge(self, pin, edge):
        """
        Wait for an edge. Pin should be type IN. Edge must be RISING, 
        FALLING or BOTH.
        """
        self._bus.wait_for_edge(self._bus.Gpio(pin), self._edge_mapping[edge])
