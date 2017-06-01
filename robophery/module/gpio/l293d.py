from robophery.interface.gpio import GpioModule


class L293dModule(GpioModule):
    """
    Module for motor controlled by the L293D chip.
    """
    DEVICE_NAME = 'l293d'

    def __init__(self, *args, **kwargs):
        super(L293dModule, self).__init__(*args, **kwargs)
        self._direction = 0
        self._power = 0
        # L293D pin 1 or pin 9: On or off
        self._power = self._setup_gpio_iface(kwargs.get('power'))
        self._power.setup_pin(self.GPIO_MODE_OUT)
        self._power.set_low()
        # L293D pin 2 or pin 10: Anticlockwise positive
        self._forward = self._setup_gpio_iface(kwargs.get('forward'))
        self._forward.setup_pin(self.GPIO_MODE_OUT)
        self._forward.set_low()
        # L293D pin 7 or pin 15: Clockwise positive
        self._backward = self._setup_gpio_iface(kwargs.get('backward'))
        self._backward.setup_pin(self.GPIO_MODE_OUT)
        self._backward.set_low()

    def __del__(self):
        self._power.cleanup()
        self._forward.cleanup()
        self._backward.cleanup()

    def _run(self, direction=1, power=100):
        """
        Method to drive L293D via GPIO
        """
        self._direction = direction
        self._power = power
        # Stop the motor
        self._log.debug('Set power {0} and direction {1})'.format(
            power, direction))

        if direction == 0:
            self._power.set_low()
            self._forward.set_low()
            self._backward.set_low()
        # Spin the motor
        else:
            if direction == 1:
                self._forward.set_high()
                self._backward.set_low()
            else:
                self._forward.set_low()
                self._backward.set_high()
            self._power.set_high()

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

    def commit_action(self, action, arg=None):
        self._log.debug('Received action {0} with args {1})'.format(
            action, arg))
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
        elif action == 'set_power':
            self.set_power(arg[0])
            return self.read_data()

    def set_power(self, power):
        power = int(power)
        if power < 0:
            self._run(direction=-1)
        elif power > 0:
            self._run(direction=1)
        else:
            self._run(direction=0, power=0)

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
