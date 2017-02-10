
try:
    import Adafruit_BBIO.GPIO as GPIO
    device = 'bbb'
except:
    pass

try:
    import RPi.GPIO as GPIO
    device = 'rpi'
except:
    pass

from robophery.core import Module


class GpioModule(Module):

    GPIO_MODE_OUT = 0
    GPIO_MODE_IN = 1

    GPIO_MODE_OUT_HIGH = True
    GPIO_MODE_OUT_LOW = False

    GPIO_EVENT_RISING = 1
    GPIO_EVENT_FALLING     = 2
    GPIO_EVENT_BOTH        = 3

    GPIO_PUD_OFF  = 0
    GPIO_PUD_DOWN = 1
    GPIO_PUD_UP   = 2

    def __init__(self, **kwargs):
        super(GpioModule, self, **kwargs).__init__()
        self._setup_device


    @property
    def _setup_device(self):

        if self._platform is self.RASPBERRYPI_PLATFORM:
            self._interface = RpiGpioInterface()
        elif self._platform is self.BEAGLEBONE_PLATFORM:
            self._interface = NodeMcuInterface()
        else:
            raise RuntimeError('Platform not supported Raspberry Pi revision.')

        self.setup = self._interface.setup
        self.output = self._interface.output
        self.input = self._interface.input
        self.set_high = self._interface.set_high
        self.set_low = self._interface.set_low
        self.is_high = self._interface.is_high
        self.is_low = self._interface.is_low
        self.input_pins = self._interface.input_pins
        self.output_pins = self._interface.output_pins
        self.setup_pins = self._interface.setup_pins
        self.add_event_detect = self._interface.add_event_detect
        self.remove_event_detect = self._interface.remove_event_detect
        self.add_event_callback = self._interface.add_event_callback
        self.event_detected = self._interface.event_detected
        self.wait_for_edge = self._interface.wait_for_edge
        self.cleanup = self._interface.cleanup


class BaseGpioInterface(object):
    """
    Base class for implementing simple digital IO for a platform.
    Implementors are expected to subclass from this and provide
    an implementation  of the setup, output, and input functions.
    """

    GPIO_MODE_OUT = 0
    GPIO_MODE_IN = 1

    GPIO_MODE_OUT_HIGH = True
    GPIO_MODE_OUT_LOW = False

    GPIO_EVENT_RISING = 1
    GPIO_EVENT_FALLING     = 2
    GPIO_EVENT_BOTH        = 3

    GPIO_PUD_OFF  = 0
    GPIO_PUD_DOWN = 1
    GPIO_PUD_UP   = 2

    def setup(self, pin, mode, pull_up_down=self.GPIO_PUD_OFF):
        """Set the input or output mode for a specified pin.  Mode should be
        either OUT or IN."""
        raise NotImplementedError


    def output(self, pin, value):
        """Set the specified pin the provided high/low value.  Value should be
        either HIGH/LOW or a boolean (true = high)."""
        raise NotImplementedError


    def input(self, pin):
        """Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low."""
        raise NotImplementedError


    def set_high(self, pin):
        """Set the specified pin HIGH."""
        self.output(pin, self.GPIO_MODE_OUT_HIGH)


    def set_low(self, pin):
        """Set the specified pin LOW."""
        self.output(pin, self.GPIO_MODE_OUT_LOW)


    def is_high(self, pin):
        """Return true if the specified pin is pulled high."""
        return self.input(pin) == self.GPIO_MODE_HIGH


    def is_low(self, pin):
        """Return true if the specified pin is pulled low."""
        return self.input(pin) == self.GPIO_MODE_LOW

# Basic implementation of multiple pin methods just loops through pins and
# processes each one individually. This is not optimal, but derived classes can
# provide a more optimal implementation that deals with groups of pins
# simultaneously. See MCP230xx or PCF8574 classes for examples of 
# optimized implementations.

    def output_pins(self, pins):
        """Set multiple pins high or low at once.  Pins should be a dict of pin
        name to pin value (HIGH/True for 1, LOW/False for 0).  All provided pins
        will be set to the given values.
        """
        # General implementation just loops through pins and writes them out
        # manually.  This is not optimized, but subclasses can choose to implement
        # a more optimal batch output implementation.  See the MCP230xx class for
        # example of optimized implementation.
        for pin, value in iter(pins.items()):
            self.output(pin, value)


    def setup_pins(self, pins):
        """Setup multiple pins as inputs or outputs at once.  Pins should be a
        dict of pin name to pin type (IN or OUT).
        """
        # General implementation that can be optimized by derived classes.
        for pin, value in iter(pins.items()):
            self.setup(pin, value)


    def input_pins(self, pins):
        """Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        # General implementation that can be optimized by derived classes.
        return [self.input(pin) for pin in pins]


    def add_event_detect(self, pin, edge):
        """Enable edge detection events for a particular GPIO channel.  Pin 
        should be type IN.  Edge must be RISING, FALLING or BOTH.
        """
        raise NotImplementedError


    def remove_event_detect(self, pin):
        """Remove edge detection for a particular GPIO channel.  Pin should be
        type IN.
        """
        raise NotImplementedError


    def add_event_callback(self, pin, callback):
        """Add a callback for an event already defined using add_event_detect().
        Pin should be type IN.
        """
        raise NotImplementedError


    def event_detected(self, pin):
        """Returns True if an edge has occured on a given GPIO.  You need to 
        enable edge detection using add_event_detect() first.   Pin should be 
        type IN.
        """
        raise NotImplementedError


    def wait_for_edge(self, pin, edge):
        """Wait for an edge.   Pin should be type IN.  Edge must be RISING, 
        FALLING or BOTH."""
        raise NotImplementedError


    def cleanup(self, pin=None):
        """Clean up GPIO event detection for specific pin, or all pins if none 
        is specified.
        """
        raise NotImplementedError


# helper functions useful to derived classes

    def _validate_pin(self, pin):
        # Raise an exception if pin is outside the range of allowed values.
        if pin < 0 or pin >= self.NUM_GPIO:
            raise ValueError('Invalid GPIO value, must be between 0 and {0}.'.format(self.NUM_GPIO))


    def _bit2(self, src, bit, val):
        bit = 1 << bit
        return (src | bit) if val else (src & ~bit)


class RpiGpioInterface(BaseGpioInterface):
    """
    GPIO implementation for the Raspberry Pi using the RPi.GPIO library.
    """


    def __init__(self, gpio, mode=None):
        self.gpio = gpio
        # Suppress warnings about GPIO in use.
        rpi_gpio.setwarnings(False)
        # Setup board pin mode.
        if mode == gpio.BOARD or mode == gpio.BCM:
            rpi_gpio.setmode(mode)
        elif mode is not None:
            raise ValueError('Unexpected value for mode.  Must be BOARD or BCM.')
        else:
            # Default to BOARD numbering if not told otherwise.
            rpi_gpio.setmode(rpi_gpio.BOARD)
        # Define mapping of Adafruit GPIO library constants to RPi.GPIO constants.
        self._dir_mapping = { OUT:      rpi_gpio.OUT,
                              IN:       rpi_gpio.IN }
        self._pud_mapping = { PUD_OFF:  rpi_gpio.PUD_OFF,
                              PUD_DOWN: rpi_gpio.PUD_DOWN,
                              PUD_UP:   rpi_gpio.PUD_UP }
        self._edge_mapping = { RISING:  rpi_gpio.RISING,
                               FALLING: rpi_gpio.FALLING,
                               BOTH:    rpi_gpio.BOTH }

    def setup(self, pin, mode, pull_up_down=PUD_OFF):
        """Set the input or output mode for a specified pin.  Mode should be
        either OUTPUT or INPUT.
        """
        self.gpio.setup(pin, self._dir_mapping[mode],
                            pull_up_down=self._pud_mapping[pull_up_down])


    def output(self, pin, value):
        """Set the specified pin the provided high/low value.  Value should be
        either HIGH/LOW or a boolean (true = high).
        """
        self.gpio.output(pin, value)


    def input(self, pin):
        """Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        return self.gpio.input(pin)


    def input_pins(self, pins):
        """Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        # maybe rpi has a mass read...  it would be more efficient to use it if it exists
        return [self.gpio.input(pin) for pin in pins]


    def add_event_detect(self, pin, edge, callback=None, bouncetime=-1):
        """Enable edge detection events for a particular GPIO channel.  Pin 
        should be type IN.  Edge must be RISING, FALLING or BOTH.  Callback is a
        function for the event.  Bouncetime is switch bounce timeout in ms for
        callback
        """
        kwargs = {}
        if callback:
            kwargs['callback']=callback
        if bouncetime > 0:
            kwargs['bouncetime']=bouncetime
        self.gpio.add_event_detect(pin, self._edge_mapping[edge], **kwargs)

    def remove_event_detect(self, pin):
        """Remove edge detection for a particular GPIO channel.  Pin should be
        type IN.
        """
        self.gpio.remove_event_detect(pin)


    def add_event_callback(self, pin, callback):
        """Add a callback for an event already defined using add_event_detect().
        Pin should be type IN.
        """
        self.gpio.add_event_callback(pin, callback)


    def event_detected(self, pin):
        """Returns True if an edge has occured on a given GPIO.  You need to 
        enable edge detection using add_event_detect() first.   Pin should be
        type IN.
        """
        return self.gpio.event_detected(pin)


    def wait_for_edge(self, pin, edge):
        """Wait for an edge.   Pin should be type IN.  Edge must be RISING,
        FALLING or BOTH.
        """
        self.gpio.wait_for_edge(pin, self._edge_mapping[edge])


    def cleanup(self, pin=None):
        """Clean up GPIO event detection for specific pin, or all pins if none 
        is specified.
        """
        if pin is None:
            self.gpio.cleanup()
        else:
            self.gpio.cleanup(pin)


class BeagleboneGpioInterface(BaseGpioInterface):
    """
    GPIO implementation for the Beaglebone Black using the Adafruit_BBIO
    library.
    """

    def __init__(self, gpio):
        self.gpio =.gpio
        # Define mapping of Adafruit GPIO library constants to RPi.GPIO constants.
        self._dir_mapping = { OUT:     self.gpio.OUT,
                              IN:      self.gpio.IN }
        self._pud_mapping = { PUD_OFF: self.gpio.PUD_OFF,
                              PUD_DOWN:self.gpio.PUD_DOWN,
                              PUD_UP:  self.gpio.PUD_UP }
        self._edge_mapping = { RISING: self.gpio.RISING,
                               FALLING:self.gpio.FALLING,
                               BOTH:   self.gpio.BOTH }


    def setup(self, pin, mode, pull_up_down=PUD_OFF):
        """Set the input or output mode for a specified pin.  Mode should be
        either OUTPUT or INPUT.
        """
        self.gpio.setup(pin, self._dir_mapping[mode],
                             pull_up_down=self._pud_mapping[pull_up_down])


    def output(self, pin, value):
        """Set the specified pin the provided high/low value.  Value should be
        either HIGH/LOW or a boolean (true = high).
        """
        self.gpio.output(pin, value)


    def input(self, pin):
        """Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        return self.gpio.input(pin)


    def input_pins(self, pins):
        """Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        # maybe bbb has a mass read...  it would be more efficient to use it if it exists
        return [self.gpio.input(pin) for pin in pins]


    def add_event_detect(self, pin, edge, callback=None, bouncetime=-1):
        """Enable edge detection events for a particular GPIO channel.  Pin 
        should be type IN.  Edge must be RISING, FALLING or BOTH.  Callback is a
        function for the event.  Bouncetime is switch bounce timeout in ms for 
        callback
        """
        kwargs = {}
        if callback:
            kwargs['callback']=callback
        if bouncetime > 0:
            kwargs['bouncetime']=bouncetime
        self.gpio.add_event_detect(pin, self._edge_mapping[edge], **kwargs)


    def remove_event_detect(self, pin):
        """Remove edge detection for a particular GPIO channel.  Pin should be
        type IN.
        """
        self.gpio.remove_event_detect(pin)


    def add_event_callback(self, pin, callback, bouncetime=-1):
        """Add a callback for an event already defined using add_event_detect().
        Pin should be type IN.  Bouncetime is switch bounce timeout in ms for 
        callback
        """
        kwargs = {}
        if bouncetime > 0:
            kwargs['bouncetime']=bouncetime
        self.gpio.add_event_callback(pin, callback, **kwargs)


    def event_detected(self, pin):
        """Returns True if an edge has occured on a given GPIO.  You need to 
        enable edge detection using add_event_detect() first.   Pin should be 
        type IN.
        """
        return self.gpio.event_detected(pin)


    def wait_for_edge(self, pin, edge):
        """Wait for an edge.   Pin should be type IN.  Edge must be RISING, 
        FALLING or BOTH.
        """
        self.gpio.wait_for_edge(pin, self._edge_mapping[edge])


    def cleanup(self, pin=None):
        """Clean up GPIO event detection for specific pin, or all pins if none 
        is specified.
        """
        if pin is None:
            self.gpio.cleanup()
        else:
            self.gpio.cleanup(pin)


class MinnowboardGpioInterface(BaseGpioInterface):
    """
    GPIO implementation for the Minnowboard + MAX using the mraa library
    """
    
    def __init__(self, gpio):
        self.gpio = gpio
        # Define mapping of Adafruit GPIO library constants to mraa constants
        self._dir_mapping = {
            OUT: self.gpio.DIR_OUT,
            IN: self.gpio.DIR_IN
        }
        self._pud_mapping = {
            PUD_OFF: self.gpio.MODE_STRONG,
            PUD_UP: self.gpio.MODE_HIZ,
            PUD_DOWN: self.gpio.MODE_PULLDOWN
        }
        self._edge_mapping = {
            RISING: self.gpio.EDGE_RISING,
            FALLING: self.gpio.EDGE_FALLING,
            BOTH: self.gpio.EDGE_BOTH
        }

    def setup(self, pin, mode):
        """Set the input or output mode for a specified pin.  Mode should be
        either DIR_IN or DIR_OUT.
        """
        self.gpio.Gpio.dir(self.gpio.Gpio(pin),self._dir_mapping[mode])   


    def output(self, pin, value):
        """Set the specified pin the provided high/low value.  Value should be
        either 1 (ON or HIGH), or 0 (OFF or LOW) or a boolean.
        """
        self.gpio.Gpio.write(self.gpio.Gpio(pin), value)

    
    def input(self, pin):
        """Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        return self.gpio.Gpio.read(self.gpio.Gpio(pin))    

    
    def add_event_detect(self, pin, edge, callback=None, bouncetime=-1):
        """Enable edge detection events for a particular GPIO channel.  Pin 
        should be type IN.  Edge must be RISING, FALLING or BOTH.  Callback is a
        function for the event.  Bouncetime is switch bounce timeout in ms for 
        callback
        """
        kwargs = {}
        if callback:
            kwargs['callback']=callback
        if bouncetime > 0:
            kwargs['bouncetime']=bouncetime
        self.gpio.Gpio.isr(self.gpio.Gpio(pin), self._edge_mapping[edge], **kwargs)


    def remove_event_detect(self, pin):
        """Remove edge detection for a particular GPIO channel.  Pin should be
        type IN.
        """
        self.gpio.Gpio.isrExit(self.gpio.Gpio(pin))


    def wait_for_edge(self, pin, edge):
        """Wait for an edge.   Pin should be type IN.  Edge must be RISING, 
        FALLING or BOTH.
        """
        self.gpio.wait_for_edge(self.gpio.Gpio(pin), self._edge_mapping[edge])
