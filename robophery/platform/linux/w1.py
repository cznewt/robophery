import w1thermsensor
from robophery.platform.w1 import W1Interface


class LinuxW1Interface(W1Interface):

    AVAILABLE_TYPES = [
        "DS18S20",
        "DS1822",
        "DS18B20",
        "DS1825",
        "DS28EA00",
        "MAX31850K"
    ]

    def __init__(self, *args, **kwargs):
        self._parent_interface = kwargs['parent']['interface']
        self._parent_data_pin = kwargs['parent']['data_pin']
#        self._parent_interface.setup_pin(self._parent_data_pin)
        super(LinuxW1Interface, self).__init__(*args, **kwargs)


    def __str__(self):
        return "{0} (connected to {1}, data pin {2})".format(self._base_name(), self._parent_interface._name, self._parent_data_pin)


    def _get_devices(self):
        output = []
        devices = w1thermsensor.W1ThermSensor.get_available_sensors()
        for device in devices:
            output.append(device.id)
        return output 


    def _get_all_temperatures(self):
        data = {}
        for sensor in w1thermsensor.W1ThermSensor.get_available_sensors():
            data[sensor.id] = sensor.get_temperature()
        return data


    def _get_temperature(self, addr, type):
        if type == 'ds18b20':
            sensor_type = w1thermsensor.W1ThermSensor.THERM_SENSOR_DS18B20
        sensor = w1thermsensor.W1ThermSensor(type, addr)
        return sensor.get_temperature()
