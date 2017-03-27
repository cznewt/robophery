import Adafruit_DHT
import time
from robophery.module.gpio.base import GpioModule


class Dht11Module(GpioModule):
    """
    Module for DHT11 temperature and humidity sensor.
    """
    DEVICE_NAME = 'dht11'

    def __init__(self, *args, **kwargs):
        super(Dht11Module, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('data_pin'))
        self._type = 11

    def commit_action(self, action):
        if action == 'read_data':
            return self.read_data()

    def read_data(self):
        """
        Query DHT11 to get the humidity and temperature readings.
        """
        read_time_start = time.time()
        humidity, temperature = Adafruit_DHT.read(self._type, self._pin)
        read_time_stop = time.time()
        read_time_delta = (read_time_stop - read_time_start) / 2
        if temperature == None or humidity == None:
            self._log.error("Data CRC failed while reading data.")
            data = [
                (self._name, 'temperature', None, read_time_delta),
                (self._name, 'humidity', None, read_time_delta)
            ]
        else:
            if humidity > 0 and humidity < 100:
                data = [
                    (self._name, 'temperature', temperature, read_time_delta),
                    (self._name, 'humidity', humidity, read_time_delta)
                ]
            else:
                self._log.error('Humidity out of range')
                data = [
                    (self._name, 'temperature', None, read_time_delta),
                    (self._name, 'humidity', None, read_time_delta)
                ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'temperature': {
                'type': 'gauge',
                'unit': 'C',
                'precision': 2,
                'range_low': 0,
                'range_high': 50,
                'sensor': 'dht11',
            },
            'humidity': {
                'type': 'gauge',
                'unit': 'RH',
                'precision': 5,
                'range_low': 20,
                'range_high': 80,
                'sensor': 'dht11',
            }
        }
