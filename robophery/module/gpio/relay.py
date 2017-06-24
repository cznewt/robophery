from robophery.interface.gpio import GpioModule


class RelayModule(GpioModule):
    """
    Module for generic GPIO relay control.
    """
    DEVICE_NAME = 'relay'

    def __init__(self, *args, **kwargs):
        super(RelayModule, self).__init__(*args, **kwargs)
        self._state = 0
        self._runtime = 0
        self._runtime_start = None
        self._turn_on_count = 0
        self._turn_off_count = 0
        self._data = self._setup_gpio_iface(kwargs.get('data'))
        self._data.setup_pin(self.GPIO_MODE_OUT)
        self._invert_logic = kwargs.get('invert_logic', False)
	if self._invert_logic:
          self._data.set_high()
        else:
          self._data.set_low()        

    def commit_action(self, action, arg=None):
        if action == 'turn_on':
            self.turn_on()
        elif action == 'turn_off':
            self.turn_off()
        return self.read_data()

    def turn_on(self):
        """
        Turn on the relay.
        """
        if self._invert_logic:
          self._data.set_low()
        else:
          self._data.set_high()
        self._state = 1
        self._turn_on_count += 1
        self._runtime_start = self._get_time()

    def turn_off(self):
        """
        Turn off the relay.
        """
        if self._invert_logic:
          self._data.set_high()
        else:
          self._data.set_low()
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
        read_start = self._get_time()
        self._update_runtime()
        read_stop = self._get_time()
        read_time = (read_stop - read_start) / 4
        data = [
            (self._name, 'state', self._state, read_time),
            (self._name, 'runtime', self._runtime, read_time),
            (self._name, 'turned_on', self._turn_on_count, read_time),
            (self._name, 'turned_off', self._turn_off_count, read_time),
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
