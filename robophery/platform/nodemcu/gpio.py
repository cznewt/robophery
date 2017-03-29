from robophery.platform.gpio import GpioInterface


class NodeMcuGpioInterface(GpioInterface):
    """
    GPIO implementation for the NodeMCU.
    """
    NODEMCU_GPIO_COUNT = 15

    def __init__(self, *args, **kwargs):
        from machine import Pin
        self._dir_mapping = { self.GPIO_MODE_OUT: Pin.OUT,
                              self.GPIO_MODE_IN: Pin.IN,
                              self.GPIO_MODE_ALT: Pin.ALT,
                              self.GPIO_MODE_NONE: -1 }
        self._pud_mapping = { self.GPIO_PUD_OFF: -1,
                              self.GPIO_PUD_DOWN: Pin.PULL_DOWN,
                              self.GPIO_PUD_UP: Pin.PULL_UP }
        self._edge_mapping = { self.GPIO_EVENT_RISING: Pin.IRQ_RISING,
                               self.GPIO_EVENT_FALLING: Pin.IRQ_FALLING,
                               self.GPIO_EVENT_BOTH: Pin.IRQ_FALLING|Pin.IRQ_RISING }
        self._drive_mapping = { self.GPIO_DRIVE_LOW: Pin.LOW_POWER,
                                self.GPIO_DRIVE_MEDIUM: Pin.MED_POWER,
                                self.GPIO_DRIVE_HIGH: Pin.HIGH_POWER }
        self._pins = {}
        self._pins_irq = {}
        self._pins_irq_triggers = {}

        #super(NodeMcuGpioInterface, self).__init__(*args, **kwargs)


    def setup_pin(self, pin, mode=None, pull_up_down=None, init_value=False, drive=None):
        """
        Set the input or output mode for a specified pin. Mode should be
        either OUTPUT or INPUT.
        """
        from machine import Pin

        if mode == None:
            mode = self.GPIO_MODE_NONE
        if pull_up_down == None:
            pull_up_down = self.GPIO_PUD_OFF
        if drive == None:
            pull_up_down = self.GPIO_DRIVE_LOW

        self._pins[pin] = Pin(pin, 
                        mode=self._dir_mapping[mode], 
                        pull=self._pud_mapping[pull_up_down],
                        value=init_value,
                        drive=self._drive_mapping)
        self._pins_irq[pin] = PinIrq()


    def get_pin(self, pin):
        """
        Return pin object specified by its number
        """
        if pin in self._pins.keys():
            return self._pins[pin]
        else:
            return 'None'

    def output(self, pin, value):
        """
        Set the specified pin the provided high/low value. Value should be
        either HIGH/LOW or a boolean (true = high).
        """
        self._pins[pin].value(value)


    def input(self, pin):
        """
        Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        return self._pins[pin].value()


    def input_pins(self, pins):
        """
        Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        return [self._pins[pin].value() for pin in pins]


    def add_event_detect(self, pin, edge, callback=None, bouncetime=-1, priority=1):
        """
        Enable edge detection events for a particular GPIO channel. Pin 
        should be type IN. Edge must be RISING or FALLING. Callback is a
        function for the event. Bouncetime is switch bounce timeout in ms for 
        callback.
        """
        if callback is not None:
            self._pins_irq[pin].setup_callback(callback)
        self._pins_irq_triggers[pin] = self._edge_mapping(edge)
        self._pins[pin].irq(handler=self._pins_irq[pin].irq_handler, 
                            trigger=self._pins_irq_triggers[pin],
                            priority=priority)

    def remove_event_detect(self, pin):
        """
        Remove edge detection for a particular GPIO channel. Pin should be
        type IN.
        """
        del(self._pins_irq[pin]) 
        del(self._pins_irq_triggers[pin]) 
        #TODO does this work?
        self._pins[pin].irq()
                          

    def add_event_callback(self, pin, callback, bouncetime=-1, priority=1):
        """
        Add a callback for an event already defined using add_event_detect().
        Pin should be type IN.  Bouncetime is switch bounce timeout in ms for 
        callback
        """
        self._pins_irq[pin].setup_callback(callback)


    def event_detected(self, pin):
        """
        Returns True if an edge has occured on a given GPIO.  You need to 
        enable edge detection using add_event_detect() first.   Pin should be 
        type IN.
        """
        return self._pins_irq[pin].is_event_detected()


    def wait_for_edge(self, pin, edge):
        """
        Wait for an edge.   Pin should be type IN.  Edge must be RISING, 
        FALLING or BOTH.
        """
        while self._pins_irq[pin].is_event_detected() == False:
            #TODO timeout
            pass


class PinIrq():
    def __init__(self, callback=None):
        self._pin_event_detected = False
        self._callback = callback


    def is_event_detected(self):
        if self._pin_event_detected == True:
            self._pin_event_detected = False
            return True
        else:
            return False


    def setup_callback(self, callback):
        self._callback = callback


    def irq_handler(self):
        self._pin_event_detected = True
        if self._callback is not None:
            self._callback()
