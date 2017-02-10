
import RPi.GPIO
from robophery.gpio.interface import GpioInterface

class RaspberrypiInterface(GpioInterface):
    """
    GPIO implementation for the Raspberry Pi using the RPi.GPIO library.
    """

    def __init__(self, mode=None):
        self.gpio = RPi.GPIO
        # Suppress warnings about GPIO in use.
        GPIO.setwarnings(False)
        # Setup board pin mode.
        if mode == gpio.BOARD or mode == gpio.BCM:
            self.gpio.setmode(mode)
        elif mode is not None:
            raise ValueError('Unexpected value for mode.  Must be BOARD or BCM.')
        else:
            self.gpio.setmode(self.gpio.BOARD)
        self._dir_mapping = { OUT:      self.gpio.OUT,
                              IN:       self.gpio.IN }
        self._pud_mapping = { PUD_OFF:  self.gpio.PUD_OFF,
                              PUD_DOWN: self.gpio.PUD_DOWN,
                              PUD_UP:   self.gpio.PUD_UP }
        self._edge_mapping = { RISING:  self.gpio.RISING,
                               FALLING: self.gpio.FALLING,
                               BOTH:    self.gpio.BOTH }

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
