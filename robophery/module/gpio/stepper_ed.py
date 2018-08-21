from robophery.interface.gpio import GpioModule
import time

class StepperEasyDriverModule(GpioModule):
    """
    Module for motor controlled by the EasyDriver module.
    """
    DEVICE_NAME = 'stepper_ed'

    def __init__(self, *args, **kwargs):
        super(StepperEasyDriverModule, self).__init__(*args, **kwargs)
        self._speed = kwargs.get('speed')
        # L293D pin 1 or pin 9: On or off
        self._power = self._setup_gpio_iface(kwargs.get('power'))
        self._power.setup_pin(self.GPIO_MODE_OUT)
        self._power.set_high()
        # L293D pin 2 or pin 10: Anticlockwise positive
        self._step = self._setup_gpio_iface(kwargs.get('step'))
        self._step.setup_pin(self.GPIO_MODE_OUT)
        self._step.set_low()
        # L293D pin 7 or pin 15: Clockwise positive
        self._direction = self._setup_gpio_iface(kwargs.get('direction'))
        self._direction.setup_pin(self.GPIO_MODE_OUT)
        self._direction.set_low()

    def __del__(self):
        self._power.cleanup()
        self._step.cleanup()
        self._direction.cleanup()

    def _run(self, direction=1, power=1, steps=10):
        """
        Method to drive L293D stepper motor via GPIO
        """
        # enable motor
        self._power.set_low()

        if direction == 1:
            self._direction.set_low()
        else:
            self._direction.set_high()

        waitTime = 0.000001/power  # waitTime controls speed

        stepCounter = 0
        while stepCounter < steps:
            #gracefully exit if ctr-c is pressed
            #exitHandler.exitPoint(True) #exitHandler.exitPoint(True, cleanGPIO)

            #turning the gpio on and off tells the easy driver to take one step
            self._step.set_high()
            self._step.set_low()

            stepCounter += 1

            #wait before taking the next step thus controlling rotation speed
            time.sleep(waitTime)

        # Stop the motor
        self._log.debug('Set power {0} and direction {1})'.format(
            power, direction))

        if direction == 0:
            self._power.set_low()
            self._step.set_low()
            self._direction.set_low()
        # Spin the motor
        else:
            if direction == 1:
                self._step.set_high()
                self._direction.set_low()
            else:
                self._step.set_low()
                self._direction.set_high()
            self._power.set_high()

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
                'unit': '',
                'range_low': 0,
                'range_high': 1,
                'sensor': self.DEVICE_NAME
            }
        }
