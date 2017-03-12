import paho.mqtt.client as mqtt
from robophery.platform.mqtt import MqttComm

class PahoMqttComm(MqttComm):

    def __init__(self, *args, **kwargs):
        self._client = mqtt.Client()
        #self._client.on_connect = self._on_connect
        #self._client.on_message = self._on_message
        self._host = kwargs.get('host', '172.0.0.1')
        self._port = kwargs.get('host', 1883)
		self._client.connect(self._host, self._port, 60)
		#self._client.loop_forever()
        super(PahoMqttComm, self).__init__(*args, **kwargs)

	def _on_connect(self, client, userdata, flags, rc):
	    """
	    The callback for when the client receives a CONNACK response from
	    the server.
	    """
	    print("Connected with result code "+str(rc))

	    # Subscribing in on_connect() means that if we lose the connection and
	    # reconnect then subscriptions will be renewed.
	    client.subscribe("$SYS/#")

	def on_message(client, userdata, msg):
	    """
	    The callback for when a PUBLISH message is received from the server.
	    """
	    print(msg.topic+" "+str(msg.payload))
