
from robophery.comm.statsd import StatsdComm

class GenericStatsdComm(StatsdComm):

    def __init__(self, *args, **kwargs):
        super(GenericStatsdComm, self).__init__(*args, **kwargs)

    def send_data(self, data):
        pass
