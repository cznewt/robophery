from w1thermsensor import W1ThermSensor
from robophery.base import Module


class W1Module(Module):

    def __init__(self, *args, **kwargs):
        super(W1Module, self).__init__(*args, **kwargs)


    @property
    def _get_all_temperatures(self):
        data = []
        for sensor in W1ThermSensor.get_available_sensors():
            data.append(('%s-%s' % (self._name, sensor.id), 'temperature', sensor.get_temperature()))
        return data

    @property
    def _get_temperature(self):
        if self._type == 'ds18b20':
            sensor_type = W1ThermSensor.THERM_SENSOR_DS18B20
        sensor = W1ThermSensor(sensor_type, self._id)
        return [(self._name, 'temperature', sensor.get_temperature())]
