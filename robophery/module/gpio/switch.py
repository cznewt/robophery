from robophery.module.gpio.base import GpioModule


class SwitchModule(GpioModule):
    """
    Module for generic GPIO switch.
    """
    DEVICE_NAME = 'gpio-switch'


    def __init__(self, *args, **kwargs):
        super(SwitchModule, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('data_pin'))
        self.setup_pin(self._pin, self.GPIO_MODE_IN)
        self._event_count = 0
        self._time_count = 0
        edge = self._interface.GPIO_EVENT_RISING
        self.add_event_detect(self._pin, edge, callback=self._process_edge)


    def _process_edge(self, pin):
        self._event_count += 1


    def commit_action(self, action):
        if action == 'read_data':
            return self.read_data()


    def read_data(self):
        """
        Switch status readings.
        """
        data = [
            (self._name, 'on_total', self._event_count, 0),
            (self._name, 'on_delta', self._event_count, 0),
        ]
        self._log_data(data)
        return data



    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'on_total': {
                'type': 'counter',
                'unit': 's',
                'precision': 0.1,
                'range_low': 0,
                'range_high': None,
                'sensor': 'switch'
            },
            'on_delta': {
                'type': 'delta',
                'unit': 's',
                'precision': 0.1,
                'range_low': 0,
                'range_high': None,
                'sensor': 'switch'
            }
        }
