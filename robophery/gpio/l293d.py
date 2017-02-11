from robophery.gpio import GpioModule


class L293dModule(GpioModule):
    """
    Module for a motor controlled by the L293D chip
    """
    DEVICE_NAME = 'gpio-l293d'
    # L293D pin1 or pin9: On or off
    MOTOR_POWER_PIN = 0
    # L293D pin2 or pin10: Anticlockwise positive
    MOTOR_FORWARD_PIN = 0
    # L293D pin7 or pin15: Clockwise positive
    MOTOR_BACKWARD_PIN = 0

    def __init__(self, *args, **kwargs):
        super(L293dModule, self).__init__(*args, **kwargs)
        self._power_pin = kwargs.get('power_pin', self.MOTOR_POWER_PIN)
        self._forward_pin = kwargs.get('forward_pin', self.MOTOR_FORWARD_PIN)
        self._backward_pin = kwargs.get('backward_pin', self.MOTOR_BACKWARD_PIN)
        self._direction = 0
        self._power = 0

        #Set output mode for all pins
        self.set_low(self._power_pin)
        self.set_low(self._forward_pin)
        self.set_low(self._backward_pin)


    def _run(self, direction=1, power=100):
        """
        Method to drive L293D via GPIO
        """
        self._direction = direction
        self._power = power
        # Stop the motor
        if direction == 0:
            self.set_low(self._power_pin)
        # Spin the motor
        else:
            if direction == 1:
                self.set_high(self._forward_pin)
                self.set_low(self._backward_pin)
            else:
                self.set_low(self._forward_pin)
                self.set_high(self._backward_pin)
            self.set_high(self._power_pin)


    def forward(self, power=100):
        """
        Spin the motor clockwise.
        """
        self._run(direction=1, power=100)


    def backward(self, power=100):
        """
        Spin motor anticlockwise.
        """
        self._run(direction=-1, power=100)


    def stop(self):
        """
        Stop the motor.
        """
        self._run(direction=0, power=0)


    @property
    def get_data():
        """
        L293d motor status readings.
        """
        data = [
            ('%s.direction' % self._name, self._direction, ),
            ('%s.power' % self._name, self._power, ),
        ]
        return data
