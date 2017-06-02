from robophery.interface.pwm import PwmModule


class ServoModule(PwmModule):
    """
    Module for generic PWM servo control.
    """
    DEVICE_NAME = 'servo'

    SERVO_MIN_ANGLE = 0
    SERVO_MAX_ANGLE = 180

    SERVO_MIN_PULSE = 150
    SERVO_MAX_PULSE = 600

    def __init__(self, *args, **kwargs):
        super(ServoModule, self).__init__(*args, **kwargs)
        self._angle = kwargs.get('angle', None)
        self._offset_angle = kwargs.get('offset_angle', 0)
        self._reverse_logic = kwargs.get('reverse_logic', False)

        self._data = self._setup_pwm_iface(kwargs.get('data'))

        if self._angle is None:
            self._angle = 90
        else:
            self._angle = int(self._angle)
            self.set_angle(self._angle)

    def commit_action(self, fun, arg=None):
        if fun == 'read_data':
            return self.read_data()
        elif fun == 'set_angle':
            self.set_angle(arg[0])
            return self.read_data()
        elif fun == 'reset':
            self.reset()
            return self.read_data()

    def reset(self):
        self._interface.reset()

    def set_angle(self, angle):
        self._angle = angle
        pulse = int(self.SERVO_MIN_PULSE +
                    (self.SERVO_MAX_PULSE - self.SERVO_MIN_PULSE) * angle / 180.0)
        self._log.debug('Set angle {0} deg (pulse {1})'.format(angle, pulse))
        if pulse >= self.SERVO_MIN_PULSE and pulse <= self.SERVO_MAX_PULSE:
            self._data.set_pulse(0, pulse)

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
        read_start = self._get_time()
        angle = self._angle
        read_stop = self._get_time()
        read_time = read_stop - read_start
        data = [
            (self._name, 'angle', angle, read_time),
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
                'precision': 1,
                'range_low': 0,
                'range_high': 180,
                'sensor': self.DEVICE_NAME
            },
        }
