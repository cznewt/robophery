from robophery.base import Module


class TankModule(Module):
    """
    Module for 2 belted tank.
    """
    DEVICE_NAME = 'tank'

    def __init__(self, *args, **kwargs):
        super(TankModule, self).__init__(*args, **kwargs)
