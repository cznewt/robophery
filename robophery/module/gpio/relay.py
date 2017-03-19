from robophery.module.gpio.base import GpioModule


class RelayModule(GpioModule):
    """
    Module for generic GPIO relay control.
    """
    DEVICE_NAME = 'gpio-relay'


    def __init__(self, *args, **kwargs):
        super(RelayModule, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('data_pin'))
        self.setup_pin(self._pin, self.GPIO_MODE_OUT)
        self._power = 0
        self.set_low(self._pin)


    def commit_action(self, action):
        if action == 'read_data':
            return self.read_data()
        elif action == 'turn_on':
            self.turn_on()
            return self.read_data()
        elif action == 'turn_off':
            self.turn_off()
            return self.read_data()


    def turn_on(self):
        """
        Turn on the relay.
        """
        self._power = 1
        self.set_high(self._pin)


    def turn_off(self):
        """
        Turn off the relay.
        """
        self._power = 0
        self.set_low(self._pin)


    def read_data(self):
        """
        Relay status readings.
        """
        data = [
            (self._name, 'on_count', self._power, 0),
            (self._name, 'on_delta', self._power, 0),
        ]
        self._log_data(data)
        return data


    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'on_count': {
                'type': 'counter',
                'unit': 's',
                'range_low': 0,
                'range_high': None,
                'sensor': 'relay'
            },
            'on_delta': {
                'type': 'delta',
                'unit': 's',
                'range_low': 0,
                'range_high': None,
                'sensor': 'relay'
            }
        }
