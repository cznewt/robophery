from w1thermsensor import W1ThermSensor
from robophery.base import Module


class W1Module(Module):

    def __init__(self, *args, **kwargs):
        super(W1Module, self).__init__(*args, **kwargs)


    def _get_all_temperatures(self):
        return self._interface._get_all_temperatures()


    def _get_temperature(self, addr, type):
        return self._interface._get_temperature(addr, type)
