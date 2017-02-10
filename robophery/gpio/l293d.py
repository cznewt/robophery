
from robophery.gpio import GpioModule
import RPi.GPIO as GPIO

class L293dModule(GpioModule):
    """
    A module for a motor controlled the L293D chip
    """

    DEVICE_NAME = 'gpio-l293d'

    # L293D pin1 or pin9: On or off
    MOTOR_POWER_PIN = 0
    # L293D pin2 or pin10: Anticlockwise positive
    MOTOR_FORWARD_PIN = 0
    # L293D pin7 or pin15: Clockwise positive
    MOTOR_BACKWARD_PIN = 0

    def __init__(self, **kwargs):
        super(L293dModule, self, **kwargs).__init__()
        self.power_pin = kwargs.get('port_a', self.MOTOR_POWER_PIN)
        self.forward_pin = kwargs.get('port_b', self.MOTOR_FORWARD_PIN)
        self.backward_pin = kwargs.get('port_c', self.MOTOR_BACKWARD_PIN)

        self.direction = 0
        self.power = 0

        self.gpio_setup()

    @staticmethod
    def gpio_setup(self):
        """
        Set GPIO.OUT for all pins
        """
        GPIO.setup(self.power_pin, GPIO.OUT)
        GPIO.setup(self.forward_pin, GPIO.OUT)
        GPIO.setup(self.backward_pin, GPIO.OUT)

    def drive_motor(self, direction=1, power=100):
        """
        Method to drive L293D via GPIO
        """
        self.direction = direction
        # Stop the motor
        if direction == 0:
            GPIO.output(self.power_pin, GPIO.LOW)
        # Spin the motor
        else:
            if direction == 1:
                GPIO.output(self.forward_pin, GPIO.HIGH)
                GPIO.output(self.backward_pin, GPIO.LOW)
            else:
                GPIO.output(self.forward_pin, GPIO.LOW)
                GPIO.output(self.backward_pin, GPIO.HIGH)
            GPIO.output(self.power_pin, GPIO.HIGH)


    def forward(self, power=100):
        """
        Spin the motor clockwise.
        """
        self.drive_motor(direction=1, power=100)


    def spin_anticlockwise(self, power=100):
        """
        Spin motor anticlockwise.
        """
        self.drive_motor(direction=-1, power=100)


    def stop(self):
        """
        Stop the motor.
        """
        self.drive_motor(direction=0, power=0)


    @property
    def get_data():
        """
        L293d motor status readings.
        """
        values = [
            ('%s.direction' % self.name, self.direction, ),
            ('%s.power' % self.name, self.power, ),
        ]
        return values
