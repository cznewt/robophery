# module for controlling ALLBOT VR204 spider
#
# Ported from https://github.com/Velleman/ALLBOT-lib/blob/master/examples/VR204/VR204.ino
#

from robophery.base import Module


class Vr204Module(Module):
    """
    Module for Allbot 2 legged 4 servos spider.
    """
    DEVICE_NAME = 'vr204'

    def __init__(self, *args, **kwargs):
        super(Vr204Module, self).__init__(*args, **kwargs)
        self._joint = kwargs['joint']

    def commit_action(self, action, arg=None):
        self._log.debug('Received action :0} with args :1})'.format(
            action, arg))
        if action == 'stop':
            self.stop()
        elif action == 'scared':
            self.scared(10)
        elif action == 'go_forward':
            self.walk_forward(5, 200)
        elif action == 'go_backward':
            self.walk_backward(5, 200)
        elif action == 'go_left':
            self.walk_left(5, 200)
        elif action == 'go_right':
            self.walk_right(5, 200)
        return self.read_data()

    def _move(self, joint, angle):
        self._manager._module[self._joint[joint]].commit_action('set_angle', [angle])

    def _animate(self, speed):
        self._msleep(speed)

    def _delay(self, speed):
        self._msleep(speed)

    def stop(self):
        """
        Stop the tank movement and stand still.
        """
        self._move("hip_left", 90)
        self._move("hip_right", 90)
        self._move("ankle_left", 90)
        self._move("ankle_right", 90)
        self._animate(50)

    def walk_forward(self, steps, speed):
        self._move("hip_left", 130)
        self._move("hip_right", 40)
        self._animate(speed)

        for i in range(steps):
            self._move("ankle_left", 45)
            self._animate(speed * 2)

            self._move("ankle_right", 135)
            self._animate(speed * 2)

            self._move("ankle_left", 90)
            self._animate(speed * 2)

            self._move("ankle_right", 90)
            self._animate(speed * 2)

        self._move("hip_left", 90)
        self._move("hip_right", 90)
        self._animate(speed)

    def walk_backward(self, steps, speed):
        self._move("hip_left", 130)
        self._move("hip_right", 40)
        self._animate(speed)

        for i in range(steps):
            self._move("ankle_left", 135)
            self._animate(speed * 2)

            self._move("ankle_right", 45)
            self._animate(speed * 2)

            self._move("ankle_left", 90)
            self._animate(speed * 2)

            self._move("ankle_right", 90)
            self._animate(speed * 2)

        self._move("hip_left", 90)
        self._move("hip_right", 90)
        self._animate(speed)

    def walk_right(self, steps, speed):
        for i in range(steps):
            self._move("ankle_right", 45)
            self._animate(speed)

            self._move("ankle_left", 135)
            self._animate(speed)

            self._move("ankle_right", 90)
            self._animate(speed)

            self._move("ankle_left", 90)
            self._animate(speed)

    def walk_left(self, steps, speed):
        for i in range(steps):
            self._move("ankle_left", 45)
            self._animate(speed)

            self._move("ankle_right", 135)
            self._animate(speed)

            self._move("ankle_left", 90)
            self._animate(speed)

            self._move("ankle_right", 90)
            self._animate(speed)

    def look_right(self, speed):
        self._move("hip_left", 45)
        self._move("hip_right", 135)
        self._animate(speed)

        self._delay(speed / 2)

        self._move("hip_left", 90)
        self._move("hip_right", 90)
        self._animate(speed)

    def look_left(self, speed):
        self._move("hip_left", 135)
        self._move("hip_right", 45)
        self._animate(speed)

        self._delay(speed / 2)

        self._move("hip_left", 90)
        self._move("hip_right", 90)
        self._animate(speed)

    def scared(self, shakes):
        for i in range(shakes):
            self._move("ankle_left", 45)
            self._move("ankle_right", 45)
            self._animate(100)

            self._move("ankle_left", 135)
            self._move("ankle_right", 135)
            self._animate(100)

        self._move("ankle_left", 90)
        self._move("ankle_right", 90)
        self._animate(100)
