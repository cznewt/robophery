from robophery.base import Interface, Module


class W1Module(Module):
    """
    Base class for implementing 1-wire bus device.
    """

    def __init__(self, *args, **kwargs):
        super(W1Module, self).__init__(*args, **kwargs)


class W1Interface(Interface):
    """
    Base class for implementing 1-wire bus.
    """

    def __init__(self, *args, **kwargs):
        self._addrs_used = []
        super(W1Interface, self).__init__(*args, **kwargs)

    def _get_all_temperatures(self):
        raise NotImplementedError

    def _get_temperature(self, addr, type):
        raise NotImplementedError
