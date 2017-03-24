import json


class MqttComm(object):
    """
    Base class for implementing MQTT communication.
    """

    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('name')
        self._manager = kwargs.get('manager', None)
        self._class = kwargs.get('class', None)
        self._host = kwargs.get('host', '127.0.0.1')
        self._port = kwargs.get('port', 1883)
        self._subscribe_topic = kwargs.get(
            'subscribe_topic', 'robophery_sub/{0}#'.format(self._manager._name))
        self._publish_topic = kwargs.get(
            'publish_topic', 'robophery_pub/{0}'.format(self._manager._name))
        self._publish_format = kwargs.get('publish_format', 'SenML')
        self._log = self._manager._get_logger(self._name)
        self._log.info("Started communication channel {0}.".format(self))

    def __str__(self):
        return "{0} (connected to tcp://{1}:{2}, publishing to {3} in {4} format, subscribed to {5})".format(self._base_name(), self._host, self._port, self._publish_topic, self._publish_format, self._subscribe_topic)

    def _base_name(self):
        return '{0} {1}'.format(self._class.split('.')[-1], self._name)

    def _to_string(self, datum):
        return json.dumps(datum)

    def receive_data(self, topic, raw_data):
        data = json.loads(raw_data)
        tgt = data.get('tgt', 'unknown')
        fun = data.get('fun', 'get_data')
        arg = data.get('arg', None)
        if tgt in self._module:
            output = self._module[tgt].commit_action(fun, arg)

    def send_data(self, data):
        for name, datum in data.items():
            self.send_datum({name: datum})

    def send_datum(self, datum):
        raise NotImplementedError
