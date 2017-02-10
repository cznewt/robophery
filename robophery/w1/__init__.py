
from w1thermsensor import W1ThermSensor

from robophery.core import Module

class W1Module(Module):

    def __init__(self, **kwargs):
        super(W1Module, self, **kwargs).__init__()


    @property
    def _get_all_temperatures(self):
        data = []
        for sensor in W1ThermSensor.get_available_sensors():
            data.append(('%s-%s.temperature' % (self._name, sensor.id), sensor.get_temperature()))


    @property
    def _get_temperature(self):
        if self._type == 'ds18b20':
            sensor_type = W1ThermSensor.THERM_SENSOR_DS18B20
        sensor = W1ThermSensor(sensor_type, self._id)
        data.append(('%s.temperature' % self._name, sensor.get_temperature()))
