
class StatsdComm(object):
    """
    Base class for implementing Statsd communication.
    """

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name')
        self._class = kwargs.get('class', None)
        self._log = self._manager._get_logger(self._name)
        self._log.info("Started communication channel {0}.".format(self))


    def __str__(self):
        return "{0} (connected to udp://{1}:{2}, prefix {3})".format(self._base_name(), self._host, self._port, self._prefix)


    def _base_name(self):
        return '{0} {1}'.format(self._class.split('.')[-1], self._name)
