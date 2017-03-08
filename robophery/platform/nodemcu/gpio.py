from robophery.platform.gpio import GpioInterface


class NodeMcuGpioInterface(GpioInterface):
    """
    GPIO implementation for the NodeMCU.
    """

    def __init__(self, *args, **kwargs):
        super(NodeMcuGpioInterface, self).__init__(*args, **kwargs)


    def setup(self, pin, mode, pull_up_down=None):
        """
        Set the input or output mode for a specified pin. Mode should be
        either OUTPUT or INPUT.
        """
        if pull_up_down == None:
            pull_up_down = self.GPIO_PUD_OFF
        self._bus.setup(pin, self._dir_mapping[mode],
                             pull_up_down=self._pud_mapping[pull_up_down])


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


    def add_event_callback(self, pin, callback, bouncetime=-1):
        """
        Add a callback for an event already defined using add_event_detect().
        Pin should be type IN.  Bouncetime is switch bounce timeout in ms for 
        callback
        """
        kwargs = {}
        if bouncetime > 0:
            kwargs['bouncetime']=bouncetime
        self._bus.add_event_callback(pin, callback, **kwargs)


    def event_detected(self, pin):
        """
        Returns True if an edge has occured on a given GPIO.  You need to 
        enable edge detection using add_event_detect() first.   Pin should be 
        type IN.
        """
        return self._bus.event_detected(pin)


    def wait_for_edge(self, pin, edge):
        """
        Wait for an edge.   Pin should be type IN.  Edge must be RISING, 
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
