
class MqttComm(object):
    """
    Base class for implementing MQTT communication.
    """

    def __init__(self, *args, **kwargs):
        self._manager = kwargs.get('manager', None)
