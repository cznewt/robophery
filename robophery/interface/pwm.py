from robophery.base import Interface, Module


class PwmModule(Module):

    def __init__(self, *args, **kwargs):
        super(PwmModule, self).__init__(*args, **kwargs)

    def __str__(self):
        return self._base_name()

    def _setup_pwm_iface(self, data):
        iface = self._manager._interface[data['iface']]
        pin = data['pin']
        return PwmPort(iface, pin)


class PwmPort():

    def __init__(self, iface, pin):
        self._iface = iface
        self._pin = pin
        self._iface._use_pin(pin)

    def _normalize_pin(self, pin):
        value = int(pin)
        return value

    def setup_pin(self, dutycycle, frequency=2000):
        self._iface.setup_pin(self._pin, dutycycle, frequency)

    def set_duty_cycle(self, dutycycle):
        self._iface.set_duty_cycle(self._pin, dutycycle)

    def set_frequency(self, frequency):
        self._iface.set_frequency(self._pin, frequency)

    def set_pulse(self, on, off):
        self._iface.set_pulse(self._pin, on, off)

    def set_pulse_all(self, on, off):
        self._iface.set_pulse_all(on, off)

    def stop(self):
        self._iface.stop(self._pin)

    def reset(self):
        self._iface.reset()

        
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

    def reset(self):
        """
        Stop PWM output on specified pin.
        """
        raise NotImplementedError
