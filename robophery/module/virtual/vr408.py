import time
from robophery.base import Module


class Vr408Module(Module):
    """
    Module for Allbot 4 legged 8 servos spider.
    """
    DEVICE_NAME = 'virtual_vr408'

    SERVO_MIN_ANGLE = 0
    SERVO_MAX_ANGLE = 180

    SERVO_MIN_PULSE = 150
    SERVO_MAX_PULSE = 600

    def __init__(self, *args, **kwargs):
