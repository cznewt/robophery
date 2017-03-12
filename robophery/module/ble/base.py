
from bluetooth.ble import GATTRequester, GATTResponse
from robophery.core import Module
import struct

class BleModule(Module):

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr')
        super(BleModule, self).__init__(*args, **kwargs)


    def _connect(self, addr):
        self._interface._connect(self._addr)


    def _disconnect(self):
        self._interface._disconnect()


    def _read_uuid(self, reg, type='float'):
        return self._interface._read_uuid(reg, type)


    def _write_uuid(self, reg, value, type='float'):
        char = self._interface.characteristic[reg]
        self._interface.write_by_handle(char, value, type)
