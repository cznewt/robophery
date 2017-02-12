from robophery.gpio import GpioModule


class SwitchModule(GpioModule):
    """
    Module for generic GPIO switch.
    """
    DEVICE_NAME = 'gpio-switch'


    def __init__(self, *args, **kwargs):
        super(SwitchModule, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('pin'))
        self.setup(self._pin, self.GPIO_MODE_IN)


    @property
    def get_data(self):
        """
        Switch status readings.
        """
        if self.is_low(self._pin):
            state = 0
        else:
            state = 1
        press_count = press_delta = state
        return [
            (self._name, 'press_count', press_count),
            (self._name, 'press_delta', press_delta),
        ]


    @property
    def get_meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'press_count': {
                'type': 'counter',
                'unit': 's',
                'precision': 0.1,
                'range_low': 0,
                'range_high': None,
                'sensor': 'switch'
            },
            'press_delta': {
                'type': 'delta',
                'unit': 's',
                'precision': 0.1,
                'range_low': 0,
                'range_high': None,
                'sensor': 'switch'
            }
        }
