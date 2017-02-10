
import robophery.gpio


class RelayModule(gpio.GpioModule):

    DEVICE_NAME = 'gpio-relay'


    def __init__(self, **kwargs):
        super(RelayModule, self, **kwargs).__init__()
        self._pin = kwargs.get('pin')
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
    def get_data():
        """
        Relay status readings.
        """
        data = [
            ('%s.runtime_count' % self.name, self._power, ),
            ('%s.runtime_delta' % self.name, self._power, ),
        ]
        return data


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
