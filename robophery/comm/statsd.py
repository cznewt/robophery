
class StatsdComm(object):
    """
    Base class for implementing Statsd communication.
    """

    def __init__(self, *args, **kwargs):
        self._manager = kwargs.get('manager', None)
