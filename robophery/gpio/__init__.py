
from robophery.core import Module

class GpioModule(Module):

    GPIO_MODE_OUT = 0
    GPIO_MODE_IN = 1


    def __init__(self, *args, **kwargs):
        super(GpioModule, self).__init__(*args, **kwargs)
        self._setup_device


    def _normalize_pin(self, pin):
        if self._platform == self.RASPBERRYPI_PLATFORM:
            data = pin
        elif self._platform == self.BEAGLEBONE_PLATFORM:
            data = pin
        else:
            data = pin
        return int(data)


    @property
    def _setup_device(self):

        if self._platform == self.RASPBERRYPI_PLATFORM:
            from robophery.gpio.interface.raspberrypi import RaspberrypiGpioInterface
            self._interface = RaspberrypiGpioInterface()
        elif self._platform == self.BEAGLEBONE_PLATFORM:
            from robophery.gpio.interface.beaglebone import BeagleboneGpioInterface
            self._interface = BeagleboneGpioInterface()
        elif self._platform == self.MINNOWBOARD_PLATFORM:
            from robophery.gpio.interface.minnowboard import MinnowboardGpioInterface
            self._interface = MinnowboardGpioInterface()
        elif self._platform == self.FT232H_PLATFORM:
            from robophery.gpio.interface.minnowboard import Ft232hGpioInterface
            self._interface = Ft232hGpioInterface()
        else:
            raise RuntimeError('Platform not supported for GPIO interface.')

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
