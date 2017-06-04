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
