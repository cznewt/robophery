
from prometheus_client import start_http_server
import paho.mqtt.client as mqtt
from pymemcache.client.base import Client as MemcacheClient


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("$robophery/#")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    cache.set('some_key', 'some_value')


cache = MemcacheClient(('localhost', 11211))
result = cache.get('some_key')

message_bus = mqtt.Client()
message_bus.on_connect = on_connect
message_bus.on_message = on_message

message_bus.connect("iot.eclipse.org", 1883, 60)
message_bus.loop_forever()

start_http_server(8000)
