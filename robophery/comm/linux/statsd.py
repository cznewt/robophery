from robophery.comm.statsd import StatsdComm
from robophery.utils.statsd import StatsdClient

class GenericStatsdComm(StatsdComm):

    def __init__(self, *args, **kwargs):
        self._host = kwargs.get('host', 'localhost')
        self._port = kwargs.get('port', 8125)
        self._sample_rate = kwargs.get('sample_rate', 1)
        self._manager = kwargs.get('manager', None)
        self._prefix = kwargs.get('prefix', self._manager._name)
        self._client = StatsdClient(host=self._host, port=self._port,
            sample_rate=self._sample_rate, prefix=self._prefix)
        super(GenericStatsdComm, self).__init__(*args, **kwargs)

    def send_data(self, data):
        self._client.gauge
