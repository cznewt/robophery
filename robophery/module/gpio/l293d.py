from robophery.interface.gpio import GpioModule


class L293dModule(GpioModule):
    """
    Module for motor controlled by the L293D chip.
    """
    DEVICE_NAME = 'l293d'
    # L293D pin1 or pin9: On or off
    MOTOR_POWER_PIN = 0
    # L293D pin2 or pin10: Anticlockwise positive
    MOTOR_FORWARD_PIN = 0
    # L293D pin7 or pin15: Clockwise positive
    MOTOR_BACKWARD_PIN = 0

    def __init__(self, *args, **kwargs):
        super(L293dModule, self).__init__(*args, **kwargs)
        self._power_pin = self._normalize_pin(
            kwargs.get('power_pin', self.MOTOR_POWER_PIN))
        self._forward_pin = self._normalize_pin(
            kwargs.get('forward_pin', self.MOTOR_FORWARD_PIN))
        self._backward_pin = self._normalize_pin(
            kwargs.get('backward_pin', self.MOTOR_BACKWARD_PIN))
        self._direction = 0
        self._power = 0

        # Set output mode for all pins
        self.setup_pin(self._power_pin, self.GPIO_MODE_OUT)
        self.setup_pin(self._forward_pin, self.GPIO_MODE_OUT)
        self.setup_pin(self._backward_pin, self.GPIO_MODE_OUT)

        # Set state for all pins
        self.set_low(self._power_pin)
        self.set_low(self._forward_pin)
        self.set_low(self._backward_pin)

    def __del__(self):
        self.cleanup(self._power_pin)
        self.cleanup(self._forward_pin)
        self.cleanup(self._backward_pin)

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

    def run_forward(self, power=100):
        """
        Spin the motor clockwise.
        """
        self._run(direction=1, power=100)

    def run_backward(self, power=100):
        """
        Spin motor anticlockwise.
        """
        self._run(direction=-1, power=100)

    def stop(self):
        """
        Stop the motor.
        """
        self._run(direction=0, power=0)

    def commit_action(self, action):
        if action == 'get_data':
            return self.read_data()
        elif action == 'stop':
            self.stop()
            return self.read_data()
        elif action == 'run_forward':
            self.run_forward()
            return self.read_data()
        elif action == 'run_backward':
            self.run_backward()
            return self.read_data()

    def read_data(self):
        """
        L293d motor status readings.
        """
        data = [
            (self._name, 'direction', self._direction, 0),
            (self._name, 'power', self._power, 0),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'direction': {
                'type': 'gauge',
                'unit': 'heading',
                'range_low': -1,
                'range_high': 1,
                'sensor': self.DEVICE_NAME
            },
            'power': {
                'type': 'gauge',
                'unit': '%',
                'range_low': 0,
                'range_high': 100,
                'sensor': self.DEVICE_NAME
            }
        }
