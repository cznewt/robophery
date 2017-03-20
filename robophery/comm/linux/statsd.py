from robophery.comm.statsd import StatsdComm
from robophery.utils.statsd import StatsdClient

class LinuxStatsdComm(StatsdComm):

    def __init__(self, *args, **kwargs):
        self._host = kwargs.get('host', 'localhost')
        self._port = kwargs.get('port', 8125)
        self._sample_rate = kwargs.get('sample_rate', 1)
        self._manager = kwargs.get('manager', None)
        self._prefix = kwargs.get('prefix', self._manager._name)
        self._client = StatsdClient(host=self._host, port=self._port,
            sample_rate=self._sample_rate, prefix=self._prefix)
        super(LinuxStatsdComm, self).__init__(*args, **kwargs)


    def send_datum(self, datum):
        for name, value in datum.items():
            for value_name, value_value in value.items():
                bucket = "{0}.{1}".format(name, value_name)
                self._log.debug("Published bucket {0} with value {1} to {2}.".format(bucket, value_value, self._host))
                self._client.gauge(bucket, value_value, sample_rate=self._sample_rate)
