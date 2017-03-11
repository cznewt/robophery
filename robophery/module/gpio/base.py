from robophery.base import Module


class GpioModule(Module):

    GPIO_MODE_OUT = 0
    GPIO_MODE_IN = 1


    def __init__(self, *args, **kwargs):
        super(GpioModule, self).__init__(*args, **kwargs)
        self._setup_interface()


    def _normalize_pin(self, pin):
        if self._platform == self.RASPBERRYPI_PLATFORM:
            data = pin
        elif self._platform == self.BEAGLEBONE_PLATFORM:
            data = pin
        else:
            data = pin
        try:
            value = int(data)
        except:
            raise RuntimeError('Unknown GPIO pin.')
        return value


    def _setup_interface(self):
        self.setup_pin = self._interface.setup_pin
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
