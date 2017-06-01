from robophery.interface.gpio import GpioModule


class HcSr04Module(GpioModule):
    """
    Module for range sensor HC-SR04.
    """
    DEVICE_NAME = 'hcsr04'

    def __init__(self, *args, **kwargs):
        super(HcSr04Module, self).__init__(*args, **kwargs)
        self._trigger = self._setup_gpio_iface(kwargs.get('trigger'))
        self._trigger.setup_pin(self.GPIO_MODE_OUT)
        self._trigger.set_low()
        self._echo = self._setup_gpio_iface(kwargs.get('echo'))
        self._echo.setup_pin(self.GPIO_MODE_IN)
        self._sleep(2)

    def __del__(self):
        self._echo.cleanup()
        self._trigger.cleanup()

    def get_distance(self):
        self._trigger.set_high()
        self._usleep(10)
        self._trigger.set_low()

        # while self._echo.is_low():
        #    pulse_start = self._get_time()
        # while self._echo.is_high():
        #    pulse_end = self._get_time()
        # pulse_duration = pulse_end - pulse_start

        pulse_duration = 0.001
        distance = pulse_duration * 1715
        return distance

    def read_data(self):
        """
        Distance reading.
        """
        read_start = self._get_time()
        distance = self.get_distance()
        read_time = self._get_time() - read_start
        data = [
            (self._name, 'distance', distance, read_time),
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
