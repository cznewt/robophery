#from w1thermsensor import W1ThermSensor
from robophery.platform.w1 import W1Interface


class LinuxW1Interface(W1Interface):

    def __init__(self, *args, **kwargs):
        super(LinuxW1Interface, self).__init__(*args, **kwargs)
