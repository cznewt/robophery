
import struct
try:
    from bluetooth.ble import GATTRequester, GATTResponse
except:
    raise RuntimeError(
        "Cannot load BLE GATT library. Please install the library.")


from robophery.interface.ble import BleInterface


class BluezBleInterface(BleInterface):

    def __init__(self, *args, **kwargs):
        super(BluezBleInterface, self).__init__(*args, **kwargs)
        self._addr = kwargs.get('addr')

    def __del__(self):
        self._disconnect()

    def _connect(self, addr):
        self._log.info("BLE %s connecting ..." % addr)
        self.requester = GATTRequester(addr, False)
        self.requester.connect(True)
        chars = self.requester.discover_characteristics()
        self.characteristic = {}
        for char in chars:
            self.characteristic[char['uuid']] = char['value_handle']
        self._log.info("BLE %s connected OK" % self._addr)

    def _disconnect(self):
        self.requester.disconnect()

    def _read_uuid(self, reg, type='float'):
        value = self.requester.read_by_uuid(reg)[0]
        if type == 'float':
            return struct.unpack('H', value)[0] * 1.0
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
