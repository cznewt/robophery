from robophery.base import Interface

class W1Interface(Interface):
    """
    Base class for implementing 1-wire bus.
    """

    def __init__(self, *args, **kwargs):
        self._addrs_used = []
        super(W1Interface, self).__init__(*args, **kwargs)
