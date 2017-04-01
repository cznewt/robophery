from robophery.interface.gpio import GpioInterface


class Pcf8574GpioInterface(GpioInterface):
    """
    GPIO implementation for PCF8574 or PCF8574A GPIO extender.
    """
    NUM_GPIO = 8

    def __init__(self, *args, **kwargs):
        self._parent_interface = kwargs['parent']['interface']
        self._parent_address = kwargs['parent']['address']
        self._parent_interface.setup_addr(self._parent_address)
        super(Pcf8574GpioInterface, self).__init__(*args, **kwargs)
        #if self._parent_address in range(0x20, 0x28):
        #    self._device_name = "PCF8574"
        #if self._parent_address in range(0x38, 0x40):
        #    self._device_name = "PCF8574A"
        #else:
        #    raise ValueError("Bad address for PCF8574(A): 0x%02X not in range [0x20..0x27, 0x38..0x3F]" % self._parent_address)
        # Buffer register values so they can be changed without reading.
        self.iodir = 0xFF  # Default direction to all inputs is in
        self.gpio = 0x00
        self._write_pins()


    def __str__(self):
        return "{0} (connected to {1}, address {2:#x})".format(self._base_name(), self._parent_interface._name, self._parent_address)


    def _write_pins(self):
        self._parent_interface.writeRaw8(self._parent_address, self.gpio | self.iodir)


    def _read_pins(self):
        return self._parent_interface.readRaw8(self._parent_address) & self.iodir


    def setup_pin(self, pin, mode):
        self.setup_pins({pin: mode})


    def setup_pins(self, pins):
        if False in [y for x,y in [(self._validate_pin(pin), mode in (self.GPIO_MODE_IN,self.GPIO_MODE_OUT)) for pin, mode in pins.iteritems()]]:
            raise ValueError('Invalid MODE, IN or OUT')
        for pin, mode in pins.iteritems():
            self._log.debug("[{0}] Set pin {1} to mode {2}".format(self._name, pin, mode))
            self.iodir = self._bit2(self.iodir, pin, mode)
        self._write_pins()


    def output(self, pin, value):
        self.output_pins({pin: value})


    def output_pins(self, pins):
        [self._validate_pin(pin) for pin in pins.keys()]
        for pin, value in pins.iteritems():
            self.gpio = self._bit2(self.gpio, pin, bool(value))
        self._write_pins()


    def input(self, pin):
        return self.input_pins([pin])[0]


    def input_pins(self, pins):
        [self._validate_pin(pin) for pin in pins]
        inp = self._read_pins()
        return [bool(inp & (1<<pin)) for pin in pins]
