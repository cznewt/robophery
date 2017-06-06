from robophery.base import Module


class Vr618Module(Module):
    """
    Module for Allbot 6 legged 18 servos spider.
    """
    DEVICE_NAME = 'vr618'

    def __init__(self, *args, **kwargs):
        super(Vr618Module, self).__init__(*args, **kwargs)

    def read_data(self):
        data = []
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {}
