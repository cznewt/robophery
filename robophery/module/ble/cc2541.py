from robophery.interface.ble import BleModule


class Cc2541Module(BleModule):
    """
    Module for CC2541 dev kit device.
    """
    DEVICE_NAME = 'cc2541'

    def __init__(self, *args, **kwargs):
        super(Cc2541Module, self).__init__(*args, **kwargs)

    @property
    def get_data(self):
        return None
