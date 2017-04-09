
import pytest
from mock import patch
import paho.mqtt.client as mqtt

from robophery.base import ModuleManager


TEST_MODULE_CONF = {
    'module': {},
    'interface': {'test': {
        'host': 'localhost',
        'port': 1883,
        'class': 'robophery.comm.linux.mqtt.PahoMqttComm',
    }},
    'comm': {'test': {
        'host': 'localhost',
        'port': 1883,
        'class': 'robophery.comm.linux.mqtt.PahoMqttComm',
    }}
}


@pytest.fixture(scope='function')
def config():
    """Creates a robophery config for each test."""

    return TEST_MODULE_CONF


@pytest.fixture(scope='function')
def robophery(config):
    """Creates a robophery for each test."""

    with patch.object(mqtt.Client, 'connect',
                      return_value=None) as mock_method:
        client = mqtt.Client()
        client.connect(True)
        manager = ModuleManager(config=config)

    return manager
