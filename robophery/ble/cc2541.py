from robophery.ble import BleModule


class Cc2541Module(BleModule):

    def __init__(self, *args, **kwargs):
        super(Cc2541Module, self).__init__(*args, **kwargs)
