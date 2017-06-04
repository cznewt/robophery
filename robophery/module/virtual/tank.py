from robophery.base import Module


class TankModule(Module):
    """
    Module for 2 belted tank.
    """
    DEVICE_NAME = 'tank'

    def __init__(self, *args, **kwargs):
        super(TankModule, self).__init__(*args, **kwargs)
        self._belt = kwargs['belt']

    def commit_action(self, action, arg=None):
        self._log.debug('Received action {0} with args {1})'.format(
            action, arg))
        if action == 'stop':
            self.stop()
        elif action == 'go_forward':
            self.go_forward()
        elif action == 'go_backward':
            self.go_backward()
        elif action == 'turn_left':
            self.turn_left()
        elif action == 'turn_right':
            self.turn_left()
        return self.read_data()

    def _move(self, belt, action, arg=None):
        self._manager._module[self._belt[belt]].commit_action(action, [arg])

    def stop(self):

        """
        Stop the tank movement.
        """
        self._move('left_belt', 'stop')
        self._move('right_belt', 'stop')

    def go_forward(self):
        """
        Run tank forward.
        """
        self._move('left_belt', 'run_forward', 100)
        self._move('right_belt', 'run_forward', 100)

    def go_backward(self):
        """
        Run tank backward.
        """
        self._move('left_belt', 'run_backward', 100)
        self._move('right_belt', 'run_backward', 100)

    def turn_left(self):
        """
        Turn tank to the left.
        """
        self._move('left_belt', 'run_backward', 100)
        self._move('right_belt', 'run_forward', 100)

    def turn_right(self):
        """
        Turn tank to the left.
        """
        self._move('left_belt', 'run_forward', 100)
        self._move('right_belt', 'run_backward', 100)

    def read_data(self):
        data = [
        ]
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {}
