from robophery.interface.gpio import GpioModule


class RelayModule(GpioModule):
    """
    Module for generic GPIO relay control.
    """
    DEVICE_NAME = 'relay'

    def __init__(self, *args, **kwargs):
        super(RelayModule, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('data_pin'))
        self._state = 0
        self._runtime = 0
        self._runtime_start = None
        self._turn_on_count = 0
        self._turn_off_count = 0
        self.setup_pin(self._pin, self.GPIO_MODE_OUT)
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
        self.set_high(self._pin)
        self._state = 1
        self._turn_on_count += 1
        self._runtime_start = self._get_time()

    def turn_off(self):
        """
        Turn off the relay.
        """
        self.set_low(self._pin)
        self._update_runtime()
        self._state = 0
        self._turn_off_count += 1
        self._runtime_start = None

    def _update_runtime(self):
        if self._runtime_start is not None:
            now = self._get_time()
            self._runtime = self._runtime + (now - self._runtime_start)
            self._runtime_start = now

    def read_data(self):
        """
        Switch status readings.
        """
        self._update_runtime()
        data = [
            (self._name, 'state', self._state, 0),
            (self._name, 'runtime', self._runtime, 0),
            (self._name, 'turned_on', self._turn_on_count, 0),
            (self._name, 'turned_off', self._turn_off_count, 0),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'state': {
                'type': 'gauge',
                'unit': '',
                'range_low': 0,
                'range_high': 1,
                'sensor': self.DEVICE_NAME
            },
            'runtime': {
                'type': 'counter',
                'unit': 's',
                'range_low': 0,
                'range_high': None,
                'sensor': self.DEVICE_NAME
            },
            'turned_on': {
                'type': 'counter',
                'unit': 'times',
                'range_low': 0,
                'range_high': None,
                'sensor': self.DEVICE_NAME
            },
            'turned_off': {
                'type': 'counter',
                'unit': 'times',
                'range_low': 0,
                'range_high': None,
                'sensor': self.DEVICE_NAME
            },
        }
