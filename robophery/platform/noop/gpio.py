
from robophery.interface.gpio import GpioInterface


class NoopGpioInterface(GpioInterface):
    """
    No operation GPIO interface for testing.
    """

    def __init__(self, *args, **kwargs):
        self._bus = {}

        self._dir_mapping = {self.GPIO_MODE_OUT: 1,
                             self.GPIO_MODE_IN: 0}
        self._pud_mapping = {self.GPIO_PUD_OFF: 0,
                             self.GPIO_PUD_DOWN: 1,
                             self.GPIO_PUD_UP: 2}
        self._edge_mapping = {self.GPIO_EVENT_RISING: 0,
                              self.GPIO_EVENT_FALLING: 1,
                              self.GPIO_EVENT_BOTH: 2}
        super(NoopGpioInterface, self).__init__(*args, **kwargs)
        self._log.info("Started interface {0}.".format(self))
        self._pins = {}

    def __del__(self):
        self.cleanup()

    def setup_pin(self, pin, mode, pull_up_down=None):
        """
        Set the input or output mode for a specified pin. Mode should be
        either OUTPUT or INPUT.
        """
        if pull_up_down is None:
            pull_up_down = self.GPIO_PUD_OFF
        elif pull_up_down == 'up':
            pull_up_down = self.GPIO_PUD_UP
        elif pull_up_down == 'down':
            pull_up_down = self.GPIO_PUD_DOWN
        self._pin[pin] = self._dir_mapping[mode]

    def output(self, pin, value):
        """
        Set the specified pin the provided high/low value. Value should be
        either HIGH/LOW or a boolean (true = high).
        """
        self._log.debug("Pin {0} output set to {1}.".format(
            pin, "HIGH" if value else "LOW"))
        self._pin[pin] = value

    def input(self, pin):
        """
        Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        return self._pin[pin]

    def input_pins(self, pins):
        """
        Read multiple pins specified in the given list and return list of pin
        values GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False
        if pulled low.
        """
        return [self._pin[pin] for pin in pins]

    def add_event_detect(self, pin, edge, callback=None, bouncetime=-1):
        """
        Enable edge detection events for a particular GPIO channel. Pin
        should be type IN. Edge must be RISING, FALLING or BOTH. Callback is a
        function for the event. Bouncetime is switch bounce timeout in ms for
        callback.
        """
        kwargs = {}
        if callback:
            kwargs['callback'] = callback
        if bouncetime > 0:
            kwargs['bouncetime'] = bouncetime
        self._bus.add_event_detect(pin, self._edge_mapping[edge], **kwargs)

    def remove_event_detect(self, pin):
        """
        Remove edge detection for a particular GPIO channel. Pin should be
        type IN.
        """
        self._bus.remove_event_detect(pin)

    def add_event_callback(self, pin, callback):
        """
        Add a callback for an event already defined using add_event_detect().
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
        pass
