
class W1Interface(object):
    """
    Base class for implementing 1-wire bus.
    """

    def __init__(self, *args, **kwargs):
        self._addrs_used = []
