
class BleInterface(object):
    """
    Base class for implementing bluetooth low-energy bus.
    """

    def __init__(self, *args, **kwargs):
        self._addrs_used = []
