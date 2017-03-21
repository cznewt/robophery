
from robophery.module.pwm.base import PwmModule


class ServoModule(PwmModule):
    """
    Module for generic PWM servo control.
    """
    DEVICE_NAME = 'pwm-servo'

    SERVO_MIN_ANGLE = 0
    SERVO_MAX_ANGLE = 180

    SERVO_MIN_PULSE = 150
    SERVO_MAX_PULSE = 600


    def __init__(self, *args, **kwargs):
        self._pin = self._normalize_pin(kwargs.get('data_pin'))
        self._angle = kwargs.get('angle', 90)
        self._reverse_logic = kwargs.get('reverse_logic', False)
        self._offset_angle = kwargs.get('offset_angle', 0)
        super(ServoModule, self).__init__(*args, **kwargs)
        self.setup_pin(self._pin)
        self.set_angle(self._angle)
        self.set_angle(180)
        self.set_angle(0)
        self.set_angle(90)


    def reset(self):
        self._interface._parent_interface.writeRaw8(0x00, 0x06)


    def set_angle(self, angle):
        deg = (angle / 1.8) / 100
        pulse = self.SERVO_MIN_PULSE + (self.SERVO_MAX_PULSE - self.SERVO_MIN_PULSE) * deg
        self._log.debug('Pulse length: {0}'.format(pulse))
        self.set_pulse_length(pulse)


    def set_pulse_length(self, pulse):
        # 1,000,000 us per second
        pulse_length = 1000000
        # 60 Hz
        pulse_length //= 60
        self._log.debug('{0}us per period'.format(pulse_length))
        # 12 bits of resolution
        pulse_length //= 4096     
        self._log.debug('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.set_duty_cycle(self._pin, pulse)


    def read_data(self):
        data = [
            (self._name, 'angle', self._angle, 0),
        ]
        self._log_data(data)
        return data


    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'angle': {
                'type': 'gauge', 
                'unit': 'deg',
                'precision': 0.1,
                'range_low': 0,
                'range_high': 180,
                'sensor': self.DEVICE_NAME
            },
        }
