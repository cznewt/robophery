from robophery.comm.mqtt import MqttComm

class ModeMcuMqttComm(MqttComm):

    def __init__(self, *args, **kwargs):
        super(ModeMcuMqttComm, self).__init__(*args, **kwargs)


    def send_data(self, data):
        pass
