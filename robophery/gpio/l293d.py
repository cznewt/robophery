#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from robophery.gpio import GpioModule
import RPi.GPIO as GPIO

logger = logging.getLogger("robophery.gpio.l293d")


class L293dModule(GpioModule):
    """
    A class for a motor wired to the L293D chip where
    motor_pins[0] is pinA is L293D pin1 or pin9 : On or off
    motor_pins[1] is pinB is L293D pin2 or pin10 : Anticlockwise positive
    motor_pins[2] is pinC is L293D pin7 or pin15 : Clockwise positive
    """

    motor_pins = [0 for x in range(3)]

    def __init__(self, kwargs)
        self.name = kwargs.get('name')
        self.motor_pins[0] = kwargs.get('port_a', 0)
        self.motor_pins[1] = kwargs.get('port_b', 0)
        self.motor_pins[2] = kwargs.get('port_c', 0)

        self.direction = 0
        self.gpio_setup(self.motor_pins)

    @staticmethod
    def gpio_setup(pins):
        """
        Set GPIO.OUT for each pin in use
        """
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)

    def drive_motor(self, direction=1, duration=None, wait=True):
        """
        Method to drive L293D via GPIO
        """
        self.direction = direction
        if direction == 0:  # Then stop motor
            GPIO.output(self.motor_pins[0], GPIO.LOW)
        else:  # Spin motor
            # Set first direction GPIO level
            GPIO.output(self.motor_pins[direction], GPIO.HIGH)
            # Set second direction GPIO level
            GPIO.output(self.motor_pins[direction * -1], GPIO.LOW)
            # Turn the motor on
            GPIO.output(self.motor_pins[0], GPIO.HIGH)
        # If duration has been specified, sleep then stop
        if duration is not None and direction != 0:
            stop_thread = Thread(target=self.stop, args=(duration,))
            # Sleep in thread
            stop_thread.start()
            if wait:
                # If wait is true, the main thread is blocked
                stop_thread.join()


    def spin_clockwise(self, duration=None, wait=True):
        """
        Spin the motor clockwise.
        """
        self.drive_motor(direction=1, duration=duration, wait=wait)


    def spin_anticlockwise(self, duration=None, wait=True):
        """
        Spin motor anticlockwise.
        """
        self.drive_motor(direction=-1, duration=duration, wait=wait)


    def stop(self, after=0):
        """
        If 'after' is specified, sleep for amount of time
        """
        if after > 0:
            sleep(after)
        # Call drive_motor to stop motor after sleep
        self.drive_motor(direction=0, duration=after, wait=True)

    @property
    def get_data():
        """
        L293d motor status readings.
        """
        values = [
            ('%s.direction' % self.name, self.direction, ),
        ]
        return values
