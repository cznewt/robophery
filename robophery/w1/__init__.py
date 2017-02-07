
from w1thermsensor import W1ThermSensor

from robophery.core import Module

class W1Module(Module):

    def __init__(self):
        super(W1Module, self).__init__()


    @property
    def _get_all_temperatures(self):
        data = []
        for sensor in W1ThermSensor.get_available_sensors():
            data.append(('%s-%s.temperature' % (self.name, sensor.id), sensor.get_temperature()))

    @property
    def _get_temperature(self):
        if self.type == 'ds18b20':
            real_type == W1ThermSensor.THERM_SENSOR_DS18B20
        sensor = W1ThermSensor(real_type, self.addr)
        data.append(('%s.temperature' % self.name, sensor.get_temperature()))


    def _set_port(self, port):
        """
        Set GPIO port for operation.
        """
        self.port = int(port)
