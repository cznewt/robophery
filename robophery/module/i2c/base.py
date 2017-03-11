from robophery.base import Module


class I2cModule(Module):

    def __init__(self, *args, **kwargs):
        super(I2cModule, self).__init__(*args, **kwargs)
        self._interface.setup_addr(self._addr)