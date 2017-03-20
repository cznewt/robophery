
class GraphiteCarbonComm(object):
    """
    Base class for implementing Graphite communication.
    """

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name')
        self._class = kwargs.get('class', None)
        self._log = self._manager._get_logger(self._name)
        self._log.info("Started communication channel {0}.".format(self))


    def __str__(self):
        return "{0} (connected to tcp://{1}:{2}, prefix {3})".format(self._base_name(), self._host, self._port, self._prefix)


    def _base_name(self):
        return '{0} {1}'.format(self._class.split('.')[-1], self._name)


    def send_data(self, data):
        for name, datum in data.items():
            self.send_datum({name: datum})


    def send_datum(self, datum):
        raise NotImplementedError
