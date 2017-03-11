import w1thermsensor
from robophery.platform.w1 import W1Interface


class LinuxW1Interface(W1Interface):

    def __init__(self, *args, **kwargs):
        super(LinuxW1Interface, self).__init__(*args, **kwargs)


    def _get_all_temperatures(self):
        data = []
        for sensor in w1thermsensor.W1ThermSensor.get_available_sensors():
            data.append({sensor.id: sensor.get_temperature()})
        return data


    def _get_temperature(self, dev_type, dev_id):
        if dev_type == 'ds18b20':
            sensor_type = w1thermsensor.W1ThermSensor.THERM_SENSOR_DS18B20
        sensor = w1thermsensor.W1ThermSensor(sensor_type, dev_id)
        return sensor.get_temperature()
