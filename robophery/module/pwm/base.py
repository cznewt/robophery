
from robophery.base import Module

class PwmModule(Module):

    def __init__(self, *args, **kwargs):
        super(PwmModule, self).__init__(*args, **kwargs)


    def __str__(self):
        return "{0} (connected to {1}, data pin {2})".format(self._base_name(), self._interface._name, self._pin)
