from robophery.interface.gpio import GpioModule


class RevCounterModule(GpioModule):
    """
    Module for generic GPIO revolution counter.
    """
    DEVICE_NAME = 'rev_counter'

    def __init__(self, *args, **kwargs):
        super(RevCounterModule, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('data_pin'))
        self._revolutions = 0
        self.setup_pin(self._pin, self.GPIO_MODE_IN)
        rise_edge = self._interface.GPIO_EVENT_RISING
        self.add_event_detect(self._pin, rise_edge,
                              callback=self._process_rise)

    def _process_rise(self, pin):
        self._revolutions += 1

    def read_data(self):
        """
        Revolutions status readings.
        """
        data = [
            (self._name, 'revolutions', self._revolutions, 0),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'revolutions': {
                'type': 'counter',
                'unit': 'times',
                'range_low': 0,
                'range_high': None,
                'sensor': self.DEVICE_NAME
            },
        }
