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
try:
    import Adafruit_BBIO.GPIO
except ImportError:
    raise RuntimeError(
        "Cannot load Adafruit_BBIO.GPIO library. Please install the library.")

from robophery.interface.gpio import GpioInterface


class BeagleboneGpioInterface(GpioInterface):
    """
    GPIO implementation for the Beaglebone Black using the Adafruit_BBIO
    library.
    """

    def __init__(self, *args, **kwargs):
        self._bus = Adafruit_BBIO.GPIO
        self._dir_mapping = {self.GPIO_MODE_OUT: self._bus.OUT,
                             self.GPIO_MODE_IN: self._bus.IN}
        self._pud_mapping = {self.GPIO_PUD_OFF: self._bus.PUD_OFF,
                             self.GPIO_PUD_DOWN: self._bus.PUD_DOWN,
                             self.GPIO_PUD_UP: self._bus.PUD_UP}
        self._edge_mapping = {self.GPIO_EVENT_RISING: self._bus.RISING,
                              self.GPIO_EVENT_FALLING: self._bus.FALLING,
                              self.GPIO_EVENT_BOTH: self._bus.BOTH}
        super(BeagleboneGpioInterface, self).__init__(*args, **kwargs)

    def setup_pin(self, pin, mode, pull_up_down=None):
        if pull_up_down is None:
            pull_up_down = self.GPIO_PUD_OFF
        elif pull_up_down == 'up':
            pull_up_down = self.GPIO_PUD_UP
        elif pull_up_down == 'down':
            pull_up_down = self.GPIO_PUD_DOWN
        self._bus.setup(pin, self._dir_mapping[mode],
                        pull_up_down=self._pud_mapping[pull_up_down])
        self._use_pin(pin)

    def output(self, pin, value):
        self._log.debug("Ouput of pin {0} set to {1}.".format(pin, "HIGH" if value else "LOW"))
        self._bus.output(pin, value)

    def input(self, pin):
        return self._bus.input(pin)

    def input_pins(self, pins):
        return [self._bus.input(pin) for pin in pins]

    def add_event_detect(self, pin, edge, callback=None, bouncetime=-1):
        kwargs = {}
        if callback:
            kwargs['callback'] = callback
        if bouncetime > 0:
            kwargs['bouncetime'] = bouncetime
        self._bus.add_event_detect(pin, self._edge_mapping[edge], **kwargs)

    def remove_event_detect(self, pin):
        self._bus.remove_event_detect(pin)

    def add_event_callback(self, pin, callback, bouncetime=-1):
        kwargs = {}
        if bouncetime > 0:
            kwargs['bouncetime'] = bouncetime
        self._bus.add_event_callback(pin, callback, **kwargs)

    def event_detected(self, pin):
        return self._bus.event_detected(pin)

    def wait_for_edge(self, pin, edge):
        self._bus.wait_for_edge(pin, self._edge_mapping[edge])

    def cleanup(self, pin=None):
        if pin is None:
            self._bus.cleanup()
        else:
            self._bus.cleanup(pin)
