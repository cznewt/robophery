from robophery.comm.mqtt import MqttComm
from umqtt.simple import MQTTClient


class ModeMcuMqttComm(MqttComm):

    def __init__(self, *args, **kwargs):
        super(ModeMcuMqttComm, self).__init__(*args, **kwargs)
        self._client = MQTTClient(self._manager._name, self._host)
        self._client.set_callback(self._on_message)
        self._client.connect()
        self._client.subscribe(self._subscribe_topic)
        self._client.check_msg()

    def __del__(self):
        self._client.disconnect()

    def _on_message(self, topic, msg):
        """
        The callback for when a PUBLISH message is received from the broker.
        """
        self._log.debug("Received message {0} on topic {1}".format(msg, topic))
        self.receive_data(topic, msg)

    def send_datum(self, datum):
        self._client.publish(self._publish_topic, self._to_string(datum))
        self._log.debug("Published {0} to {1}.".format(datum, self._host))
