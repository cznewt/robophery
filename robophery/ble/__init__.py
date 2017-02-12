
from bluetooth.ble import GATTRequester, GATTResponse
from robophery.core import Module
import struct

class BleModule(Module):

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr')
        self.requester = GATTRequester(self._addr, False)
        super(BleModule, self).__init__(*args, **kwargs)


    def __del__(self):
        self._disconnect()


    def _connect(self):
        if self.debug:
            self._logger.info("Connecting ...")
        self.requester.connect(True)
        chars = self.requester.discover_characteristics()
        self.characteristic = {}
        for char in chars:
            self.characteristic[char['uuid']] = char['value_handle']
        if self.debug:
            self._logger.info("Connected OK")


    def _disconnect(self):
        self.requester.disconnect()


    def _read_uuid(self, reg, type='float'):
        value = self.requester.read_by_uuid(reg)[0]
        if type == 'float':
            return struct.unpack('H', value)[0] * 1.0;
        elif type == 'string':
            try:
                value = value.decode("utf-8")
            except AttributeError:
                pass
            return value
        else:
            return value

    def _write_uuid(self, reg, value, type='float'):
        if type == 'string':
            value = struct.pack('B', value)
        self.requester.write_by_handle(self.characteristic[reg], value)
