from robophery.base import Interface, Module


class GpioModule(Module):

    GPIO_MODE_OUT = 0
    GPIO_MODE_IN = 1

    def __init__(self, *args, **kwargs):
        super(GpioModule, self).__init__(*args, **kwargs)
        if kwargs.get('data', {}).get('pin', False):
            self._log.info("Started device {0} (using {1}, pin {2}).".format(
                self._base_name(),
                kwargs.get('data').get('iface'),
                kwargs.get('data').get('pin')
            ))

    def _setup_gpio_iface(self, data):
        iface = self._manager._interface[data['iface']]
        pin = data['pin']
        return GpioPort(iface, pin)

    def __str__(self):
        return self._base_name()


class GpioPort():

    def __init__(self, iface, pin):
        self._iface = iface
        self._pin = pin
        self._iface._use_pin(pin)

    def setup_pin(self, mode, pull_up_down=None):
        self._iface.setup_pin(self._pin, mode, pull_up_down)

    def get_pin(self):
        return self._iface.get_pin(self, self._pin)

    def output(self, value):
        self._iface.output(self._pin, value)

    def input(self):
        self._iface.input(self._pin)

    def set_high(self):
        self._iface.set_high(self._pin)

    def set_low(self):
        self._iface.set_low(self._pin)

    def is_high(self):
        return self._iface.is_high(self._pin)

    def is_low(self):
        return self._iface.is_low(self._pin)

    def setup_pins(self, pins):
        self._iface.setup_pins(pins)

    def output_pins(self, pins):
        self._iface.output_pins(pins)

    def input_pins(self, pins):
        self._iface.input_pins(self, pins)
        return [self.input(pin) for pin in pins]

    def add_event_detect(self, edge, callback=None, bouncetime=-1):
        self._iface.add_event_detect(self._pin, edge, callback=callback, bouncetime=bouncetime)

    def remove_event_detect(self):
        self._iface.remove_event_detect(self._pin)

    def add_event_callback(self, callback):
        self._iface.add_event_callback(self._pin, callback)

    def event_detected(self):
        self._iface.event_detected(self._pin)

    def wait_for_edge(self, edge):
        self._iface.wait_for_edge(self._pin, edge)

    def cleanup(self):
        self._iface.cleanup(self._pin)


class GpioInterface(Interface):
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
        self._pins_used = []
        super(GpioInterface, self).__init__(*args, **kwargs)

    def _use_pin(self, pin):
        self._pins_used.append(pin)

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
        Read multiple pins specified in the given list and return list of pin
        values GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False
        if pulled low.
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
            raise ValueError(
                'Invalid GPIO value, must be between 0 and {0}.'.format(self.NUM_GPIO))

    def _bit2(self, src, bit, val):
        bit = 1 << bit
        return (src | bit) if val else (src & ~bit)
