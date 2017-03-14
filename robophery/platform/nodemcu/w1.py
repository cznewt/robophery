import time
import machine
import onewire

from robophery.platform.w1 import W1Interface


class NodeMcuW1Interface(W1Interface):

    def __init__(self, *args, **kwargs):
    	parent_interface = kwargs['uses']['interface']
    	data_pin = parent_interface.setup_pin(kwargs['uses']['data_pin'])
    	# create the onewire object
	    ds = onewire.DS18B20(onewire.OneWire(dat))
		# scan for devices on the bus
		roms = ds.scan()
        super(NodeMcuW1Interface, self).__init__(*args, **kwargs)


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
