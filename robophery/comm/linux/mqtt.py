import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from robophery.comm.mqtt import MqttComm

class PahoMqttComm(MqttComm):

    def __init__(self, *args, **kwargs):
        super(PahoMqttComm, self).__init__(*args, **kwargs)
        self._client = mqtt.Client()
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.connect(self._host, self._port, 60)
        self._client.loop_start()


    def _on_connect(self, client, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response from
        the server.
        """
        self._log.info("Connected to {0}:{1} with result code {2}.".format(self._host, self._port, rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("{0}".format(self._subscribe_topic))


    def _on_message(self, client, userdata, msg):
        """
        The callback for when a PUBLISH message is received from the broker.
        """
        self.receive_data(msg.topic, msg.payload)
        self._log.debug("Received message {0} on topic {1}". format(msg.payload, msg.topic))


    def send_datum(self, datum):
        publish.single(self._publish_topic,
            payload=self._to_string(datum),
            hostname=self._host,
            client_id=self._manager._name,
#            auth=auth,
#            tls=tls,
            port=self._port,
            protocol=mqtt.MQTTv311)
        self._log.debug("Published message {0} to {1}.".format(datum, self._host))
