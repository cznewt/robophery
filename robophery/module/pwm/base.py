from robophery.base import Module


class PwmModule(Module):

    def __init__(self, *args, **kwargs):
        super(PwmModule, self).__init__(*args, **kwargs)
        self.setup_pin = self._interface.setup_pin
        self.set_duty_cycle = self._interface.set_duty_cycle
        self.set_frequency = self._interface.set_frequency
        self.stop = self._interface.stop

    def __str__(self):
        return "{0} (connected to {1}, data pin {2})".format(self._base_name(), self._interface._name, self._pin)

    def _normalize_pin(self, pin):
        value = int(pin)
        return value
