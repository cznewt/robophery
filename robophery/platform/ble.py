from robophery.base import Interface

class BleInterface(Interface):
    """
    Base class for implementing bluetooth low-energy bus.
    """

    def __init__(self, *args, **kwargs):
        self._addrs_used = []
        super(BleInterface, self).__init__(*args, **kwargs)
