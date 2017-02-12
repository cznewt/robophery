from robophery.gpio import GpioModule


class RelayModule(GpioModule):
    """
    Module for generic GPIO relay control.
    """
    DEVICE_NAME = 'gpio-relay'


    def __init__(self, *args, **kwargs):
        super(RelayModule, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('pin'))
        self.setup(self._pin, self.GPIO_MODE_OUT)
        self._power = 0
        self.set_low(self._pin)


    def on(self):
        """
        Turn on the relay.
        """
        self._power = 1
        self.set_high(self._pin)


    def off(self):
        """
        Turn off the relay.
        """
        self._power = 0
        self.set_low(self._pin)


    @property
    def get_data(self):
        """
        Relay status readings.
        """
        return [
            (self._name, 'runtime_count', self._power),
            (self._name, 'runtime_delta', self._power),
        ]


    @property
    def get_meta_data():
        """
        Get the readings meta-data.
        """
        return {
            'runtime_count': {
                'type': 'counter',
                'unit': 's',
                'range_low': 0,
                'range_high': None,
                'sensor': 'relay'
            },
            'runtime_delta': {
                'type': 'delta',
                'unit': 's',
                'range_low': 0,
                'range_high': None,
                'sensor': 'relay'
            }
        }
