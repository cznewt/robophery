import time
from robophery.module.gpio.base import GpioModule


class HcSr04Module(GpioModule):
    """
    Module for range sensor HC-SR04.
    """
    DEVICE_NAME = 'gpio-hcsr04'

    def __init__(self, *args, **kwargs):
        self._trigger_pin = self._normalize_pin(kwargs.get('trigger_pin'))
        self._echo_pin = self._normalize_pin(kwargs.get('echo_pin'))
        super(HcSr04Module, self).__init__(*args, **kwargs)
        self.setup_pin(self._trigger_pin, self.GPIO_MODE_OUT)
        self.set_low(self._trigger_pin)
        self.setup_pin(self._echo_pin, self.GPIO_MODE_IN)
        self._msleep(2000)

    def __del__(self):
        self.cleanup(self._trigger_pin)
        self.cleanup(self._echo_pin)

    def read_data(self):
        """
        Distance reading.
        """
        self.set_high(self._trigger_pin)
        self._usleep(10)
        self.set_low(self._trigger_pin)

        # while self.is_low(self._echo_pin):
        #    pulse_start = time.time()
        # while self.is_high(self._echo_pin):
        #    pulse_end = time.time()

        # pulse_duration = pulse_end - pulse_start
        pulse_duration = 0.001
        distance = pulse_duration * 1715

        data = [
            (self._name, 'distance', distance),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'distance': {
                'type': 'gauge',
                'unit': 'm',
                'precision': 0.01,
                'range_low': 0.03,
                'range_high': 4,
                'sensor': self.DEVICE_NAME
            },
        }
