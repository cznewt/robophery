from robophery.base import Interface

class PwmInterface(Interface):
    """
    Base class for implementing PWM interface.
    """

    def __init__(self, *args, **kwargs):
        self._pins_used = []
        super(PwmInterface, self).__init__(*args, **kwargs)


    def _use_pin(pin):
        self._pins_used.append(self, pin)


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
