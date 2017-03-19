import time
import machine
import onewire

from robophery.platform.w1 import W1Interface


class NodeMcuW1Interface(W1Interface):

    def __init__(self, *args, **kwargs):
        self._parent_interface = kwargs['parent']['interface']
        self._parent_data_pin = kwargs['parent']['data_pin']
        data_pin = self._parent_interface.setup_pin(self._parent_data_pin)
        self._ds = onewire.DS18B20(onewire.OneWire(data_pin))
        super(NodeMcuW1Interface, self).__init__(*args, **kwargs)


    def _get_devices(self):
        return self._ds.scan()


    def _get_all_temperatures(self):
        data = {}
        sensors = ds.scan()
        for sensor in sensors():
            data[sensor.id] = sensor.get_temperature()
        return data


    def _get_temperature(self, addr, type):
        for sensor in sensors():
            data[sensor.id] = sensor.get_temperature()
        return sensor.get_temperature()
