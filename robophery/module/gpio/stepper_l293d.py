from robophery.interface.gpio import GpioModule
import time

class StepperL293dModule(GpioModule):
    """
    Module for motor controlled by the L293D chip.
    """
    DEVICE_NAME = 'stepper_l293d'

    def __init__(self, *args, **kwargs):
        super(StepperL293dModule, self).__init__(*args, **kwargs)
        self._speed = kwargs.get('speed')
        # L293D pin 1 or pin 9: On or off
        self._power = self._setup_gpio_iface(kwargs.get('power'))
        self._power.setup_pin(self.GPIO_MODE_OUT)
        self._power.set_high()
        self._coil_a1 = self._setup_gpio_iface(kwargs.get('coil_a1'))
        self._coil_a1.setup_pin(self.GPIO_MODE_OUT)
        self._coil_a1.set_low()
        self._coil_a2 = self._setup_gpio_iface(kwargs.get('coil_a2'))
        self._coil_a2.setup_pin(self.GPIO_MODE_OUT)
        self._coil_a2.set_low()
        self._coil_b1 = self._setup_gpio_iface(kwargs.get('coil_b1'))
        self._coil_b1.setup_pin(self.GPIO_MODE_OUT)
        self._coil_b1.set_low()
        self._coil_b2 = self._setup_gpio_iface(kwargs.get('coil_b2'))
        self._coil_b2.setup_pin(self.GPIO_MODE_OUT)
        self._coil_b2.set_low()

    def __del__(self):
        self._power.cleanup()
        self._coil_a1.cleanup()
        self._coil_a2.cleanup()

    def _run(self, direction=1, power=1, steps=10):
        """
        Method to drive L293D stepper motor via GPIO
        """
        # enable motor
        self._power.set_low()

        if direction == 1:
            self._coil_a2.set_low()
        else:
            self._coil_a2.set_high()

        if direction == 0:
            self._power.set_low()
            self._coil_a1.set_low()
            self._coil_a2.set_low()
        # Spin the motor
        else:
            self._power.set_high()
            if direction == 1:
                delay = 40
                steps = 10
                self.forward(int(delay) / 1000.0, int(steps))
            else:
                self.backward(int(delay) / 1000.0, int(steps))


    def forward(self, delay, steps):
        """
        Spin the motor clockwise.
        """
        for i in range(0, steps):
            self.set_step(1, 0, 1, 0)
            time.sleep(delay)
            self.set_step(0, 1, 1, 0)
            time.sleep(delay)
            self.set_step(0, 1, 0, 1)
            time.sleep(delay)
            self.set_step(1, 0, 0, 1)
            time.sleep(delay)

    def backward(self, delay, steps):
        """
        Spin motor anticlockwise.
        """
        for i in range(0, steps):
            self.set_step(1, 0, 0, 1)
            time.sleep(delay)
            self.set_step(0, 1, 0, 1)
            time.sleep(delay)
            self.set_step(0, 1, 1, 0)
            time.sleep(delay)
            self.set_step(1, 0, 1, 0)
            time.sleep(delay)

    def set_step(self, w1, w2, w3, w4):
        if w1 == 1:
            self._coil_a1.set_high()
        else:
            self._coil_a1.set_low()
        if w2 == 1:
            self._coil_a2.set_high()
        else:
            self._coil_a2.set_low()
        if w3 == 1:
            self._coil_b1.set_high()
        else:
            self._coil_b1.set_low()
        if w4 == 1:
            self._coil_b2.set_high()
        else:
            self._coil_b2.set_low()

    def run_forward(self, power=1):
        """
        Spin the motor clockwise.
        """
        self._run(direction=1, power=power)

    def run_backward(self, power=1):
        """
        Spin motor anticlockwise.
        """
        self._run(direction=-1, power=power)

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
            (self._name, 'coil_a1', self._coil_a1, 0),
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
                'unit': '',
                'range_low': 0,
                'range_high': 1,
                'sensor': self.DEVICE_NAME
            }
        }
