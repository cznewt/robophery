from robophery.interface.gpio import GpioInterface
from robophery.interface.i2c import I2cPort


class Pcf8574GpioInterface(GpioInterface):
    """
    GPIO implementation for PCF8574 or PCF8574A GPIO extender.
    """
    NUM_GPIO = 8

    def __init__(self, *args, **kwargs):
        super(Pcf8574GpioInterface, self).__init__(*args, **kwargs)
        self._data = self._setup_parent(kwargs['data'])
        # if self._data._addr in range(0x20, 0x28):
        #     self._device_name = "PCF8574"
        # if self._data._addr in range(0x38, 0x40):
        #     self._device_name = "PCF8574A"
        # else:
        #     raise ValueError("Bad address for PCF8574(A): 0x%02X not in range [0x20..0x27, 0x38..0x3F]" % self._data._addr)
        # Buffer register values so they can be changed without reading.
        self.iodir = 0xff  # Default direction to all inputs is in
        self.gpio = 0x00
        self._write_pins()

    def _setup_parent(self, data):
        iface = self._manager._interface[data['iface']]
        addr = data['addr']
        return I2cPort(iface, addr)

    def __str__(self):
        return "{0} (using {1}, address: {2:#x})".format(
            self._base_name(),
            self._data._iface._name,
            self._data._addr
        )

    def _write_pins(self):
        self._data.writeRaw8(self.gpio | self.iodir)

    def _read_pins(self):
        return self._data.readRaw8() & self.iodir

    def setup_pin(self, pin, mode):
        self.setup_pins({pin: mode})

    def setup_pins(self, pins):
        if False in [y for x,y in [(self._validate_pin(pin), mode in (self.GPIO_MODE_IN, self.GPIO_MODE_OUT)) for pin, mode in pins.iteritems()]]:
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
        return [bool(inp & (1 << pin)) for pin in pins]
