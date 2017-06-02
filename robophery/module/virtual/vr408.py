from robophery.base import Module


class Vr408Module(Module):
    """
    Module for Allbot 4 legged 8 servos spider.
    """
    DEVICE_NAME = 'vr408'

    def __init__(self, *args, **kwargs):
        super(Vr408Module, self).__init__(*args, **kwargs)
        self._front_left_hip = self._get_module(kwargs['front_left_hip'])
        self._front_left_knee = self._get_module(kwargs['front_left_knee'])
        self._front_right_hip = self._get_module(kwargs['front_right_hip'])
        self._front_right_knee = self._get_module(kwargs['front_right_knee'])

    def commit_action(self, action):
        if action == 'read_data':
            return self.read_data()
        elif action == 'stop':
            self.stop()
        elif action == 'turn_left':
            self.turn_left()
        elif action == 'turn_right':
            self.turn_left()
        return self.read_data()

    def stop(self):
        """
        Stop the tank movement.
        """
        pass

    def turn_left(self):
        """
        Turn tank to the left.
        """
        pass

    def turn_right(self):
        """
        Turn tank to the left.
        """
        pass

    def read_data(self):
        data = []
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {}
