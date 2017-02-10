
from robophery.gpio import GpioModule


class RelayModule(GpioModule):

    DEVICE_NAME = 'gpio-relay'


    def __init__(self, **kwargs):
        super(RelayModule, self, **kwargs).__init__()
        self._pin = kwargs.get('pin')


    @property
    def get_data():
        """
        Relay status readings.
        """

     
        values = [
            ('%s.runtime_count' % self.name, runtime_count, ),
            ('%s.runtime_delta' % self.name, runtime_delta, ),
        ]
        return values


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
