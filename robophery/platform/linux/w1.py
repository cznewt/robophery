try:
    import w1thermsensor
except ImportError:
    raise RuntimeError(
        "Cannot load w1thermsensor library. Please install the library.")

from robophery.interface.w1 import W1Interface
from robophery.interface.gpio import GpioPort


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
        super(LinuxW1Interface, self).__init__(*args, **kwargs)
        self._data = self._setup_parent(kwargs['data'])
        self._log.info("Started interface {0}.".format(self))

    def __str__(self):
        return "{0} (using {1}, pin {2})".format(
            self._base_name(),
            self._data._iface._name,
            self._data._pin
        )

    def _setup_parent(self, data):
        iface = self._manager._interface[data['iface']]
        pin = data['pin']
        return GpioPort(iface, pin)

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
        if type.lower() == 'ds18b20':
            sensor_type = w1thermsensor.W1ThermSensor.THERM_SENSOR_DS18B20
        sensor = w1thermsensor.W1ThermSensor(sensor_type, addr)
        return sensor.get_temperature()
