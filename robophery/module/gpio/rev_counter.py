from robophery.interface.gpio import GpioModule


class RevCounterModule(GpioModule):
    """
    Module for generic GPIO revolution counter.
    """
    DEVICE_NAME = 'rev_counter'

    def __init__(self, *args, **kwargs):
        super(RevCounterModule, self).__init__(*args, **kwargs)
        self._revolutions = 0
        self._data = self._setup_gpio_iface(kwargs.get('data'))
        self._data.setup_pin(self.GPIO_MODE_IN)
        self.add_event_detect(self._data._iface.GPIO_EVENT_RISING,
                              callback=self._process_rise)

    def _process_rise(self, pin):
        self._revolutions += 1

    def read_data(self):
        """
        Revolutions status readings.
        """
        read_start = self._get_time()
        revolutions = self._revolutions
        read_time = self._get_time() - read_start
        data = [
            (self._name, 'revolutions', revolutions, read_time),
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
