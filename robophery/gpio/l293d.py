#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from robophery.gpio import GpioModule
import RPi.GPIO as GPIO

logger = logging.getLogger("robophery.gpio.l293d")

# L293D pin1 or pin9 : On or off
MOTOR_POWER_PIN = 0
# L293D pin2 or pin10 : Anticlockwise positive
MOTOR_FORWARD_PIN = 0
# L293D pin7 or pin15 : Clockwise positive
MOTOR_BACKWARD_PIN = 0


class L293dModule(GpioModule):
    """
    A module for a motor controlled the L293D chip
    """

    power_pin = MOTOR_POWER_PIN
    forward_pin = MOTOR_FORWARD_PIN
    backward_pin = MOTOR_BACKWARD_PIN

    def __init__(self, kwargs):
        self.name = kwargs.get('name')
        self.power_port = kwargs.get('port_a', 0)
        self.forward_port = kwargs.get('port_b', 0)
        self.backward_port = kwargs.get('port_c', 0)

        self.direction = 0
        self.power = 0

        self.gpio_setup()

    @staticmethod
    def gpio_setup(self):
        """
        Set GPIO.OUT for all pins
        """
        GPIO.setup(self.power_port, GPIO.OUT)
        GPIO.setup(self.forward_port, GPIO.OUT)
        GPIO.setup(self.backward_port, GPIO.OUT)

    def drive_motor(self, direction=1, power=100):
        """
        Method to drive L293D via GPIO
        """
        self.direction = direction
        # Stop the motor
        if direction == 0:
            GPIO.output(self.power_port, GPIO.LOW)
        # Spin the motor
        else:
            if direction == 1:
                GPIO.output(self.forward_port, GPIO.HIGH)
                GPIO.output(self.backward_port, GPIO.LOW)
            else:
                GPIO.output(self.forward_port, GPIO.LOW)
                GPIO.output(self.backward_port, GPIO.HIGH)
            GPIO.output(self.power_port, GPIO.HIGH)


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
