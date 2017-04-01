from robophery.base import Interface, Module


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


class PwmInterface(Interface):
    """
    Base class for implementing PWM interface.
    """

    def __init__(self, *args, **kwargs):
        self._pins_used = []
        super(PwmInterface, self).__init__(*args, **kwargs)

    def _use_pin(self, pin):
        self._pins_used.append(pin)

    def setup_pin(self, pin, dutycycle, frequency=2000):
        """
        Enable PWM output on specified pin. Set to initial percent duty cycle
        value (0.0 to 100.0) and frequency (in Hz).
        """
        raise NotImplementedError

    def set_duty_cycle(self, pin, dutycycle):
        """
        Set percent duty cycle of PWM output on specified pin. Duty cycle must
        be a value 0.0 to 100.0 (inclusive).
        """
        raise NotImplementedError

    def set_frequency(self, pin, frequency):
        """
        Set frequency (in Hz) of PWM output on specified pin.
        """
        raise NotImplementedError

    def stop(self, pin):
        """
        Stop PWM output on specified pin.
        """
        raise NotImplementedError
