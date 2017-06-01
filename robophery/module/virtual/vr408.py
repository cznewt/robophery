from robophery.base import Module


class Vr408Module(Module):
    """
    Module for Allbot 4 legged 8 servos spider.
    """
    DEVICE_NAME = 'vr408'

    def __init__(self, *args, **kwargs):
        super(Vr408Module, self).__init__(*args, **kwargs)
