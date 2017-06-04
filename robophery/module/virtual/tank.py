from robophery.base import Module


class TankModule(Module):
    """
    Module for 2 belted tank.
    """
    DEVICE_NAME = 'tank'

    def __init__(self, *args, **kwargs):
        super(TankModule, self).__init__(*args, **kwargs)
        self._left_belt = self._get_module(kwargs['left_belt'])
        self._right_belt = self._get_module(kwargs['right_belt'])

    def commit_action(self, action, arg=None):
        self._log.debug('Received action {0} with args {1})'.format(
            action, arg))
        if action == 'read_data':
            return self.read_data()
        elif action == 'stop':
            self.stop()
        elif action == 'forward':
            self.forward()
        elif action == 'backward':
            self.backward()
        elif action == 'turn_left':
            self.turn_left()
        elif action == 'turn_right':
            self.turn_left()
        return self.read_data()

    def stop(self):

        """
        Stop the tank movement.
        """
        self._left_belt.commit_action('stop')
        self._right_belt.commit_action('stop')

    def forward(self):
        """
        Run tank forward.
        """
        self._left_belt.run_forward(100)
        self._right_belt.run_forward(100)

    def backward(self):
        """
        Run tank backward.
        """
        self._left_belt.run_backward(100)
        self._right_belt.run_backward(100)

    def turn_left(self):
        """
        Turn tank to the left.
        """
        self._left_belt.run_backward(100)
        self._right_belt.run_forward(100)

    def turn_right(self):
        """
        Turn tank to the left.
        """
        self._left_belt.run_forward(100)
        self._right_belt.run_backward(100)

    def read_data(self):
        data = [
        #    (self._name, 'direction', self._direction, 0),
        ]
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {}
