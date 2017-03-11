from robophery.base import Module


class I2cModule(Module):

    def __init__(self, *args, **kwargs):
        self_bus = kwargs.get('interface')
        super(I2cModule, self).__init__(*args, **kwargs)
