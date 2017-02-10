
import mraa
from robophery.gpio.interface import GpioInterface

class MinnowboardInterface(GpioInterface):
    """
    GPIO implementation for the Minnowboard + MAX using the mraa library
    """
    
    def __init__(self):
        self.gpio = mraa
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
