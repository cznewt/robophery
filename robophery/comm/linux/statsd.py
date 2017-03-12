
from robophery.comm.statsd import StatsdComm

class PahoMqttComm(StatsdComm):

    def __init__(self, *args, **kwargs):
        self._client = mqtt.Client()
        #self._client.on_connect = self._on_connect
        #self._client.on_message = self._on_message
        self._host = kwargs.get('host', '172.0.0.1')
        self._port = kwargs.get('host', 1883)
        self._client.connect(self._host, self._port, 60)
        #self._client.loop_forever()
        super(PahoMqttComm, self).__init__(*args, **kwargs)
