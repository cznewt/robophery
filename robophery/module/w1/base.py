from w1thermsensor import W1ThermSensor
from robophery.base import Module


class W1Module(Module):

    def __init__(self, *args, **kwargs):
        super(W1Module, self).__init__(*args, **kwargs)
        self._get_all_temperatures = self._interface._get_all_temperatures
        self._get_temperature = self._interface._get_temperature
