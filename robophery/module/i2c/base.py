from robophery.base import Module


class I2cModule(Module):

    def __init__(self, *args, **kwargs):
        super(I2cModule, self).__init__(*args, **kwargs)
        self._interface.setup_addr(self._addr)


    def writeRaw8(self, value):
        self._interface.writeRaw8(self._addr, value)


    def write8(self, register, value):
        self._interface.write8(self._addr, register, value)


    def write16(self, register, value):
        self._interface.write16(self._addr, register, value)


    def writeList(self, register, data):
        self._interface.writeList(self._addr, register, data)


    def readRaw8(self):
        return self._interface.readRaw8(self._addr)


    def readU8(self, register):
        return self._interface.readU8(self._addr, register)


    def readS8(self, register):
        return self._interface.readS8(self._addr, register)


    def readU16(self, register, little_endian=True):
        return self._interface.readU16(self._addr, register, little_endian)


    def readS16(self, register, little_endian=True):
        return self._interface.readS16(self._addr, register, little_endian)


    def readList(self, register, length):
        return self._interface.readList(self._addr, register, length)
