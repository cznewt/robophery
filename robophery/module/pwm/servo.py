
from robophery.module.pwm.base import PwmModule


class ServoModule(PwmModule):
    """
    Module for generic PWM servo control.
    """
    DEVICE_NAME = 'pwm-servo'


    def __init__(self, *args, **kwargs):
        self._pin = self._normalize_pin(kwargs.get('data_pin'))
        super(ServoModule, self).__init__(*args, **kwargs)
        self.setup_pin(self._pin)
