import Adafruit_DHT
from robophery.module.gpio.base import GpioModule


class Dht11Module(GpioModule):
    """
    Module for DHT11 temperature and humidity sensor.
    """
    DEVICE_NAME = 'gpio-dht11'


    def __init__(self, *args, **kwargs):
        super(Dht11Module, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('data_pin'))
        self._type = 11


    def commit_action(self, action):
        if action == 'get_data':
            return self.get_data


    def read_data(self):
        """
        Query DHT11 to get the humidity and temperature readings.
        """
        humidity, temperature = Adafruit_DHT.read(self._type, self._pin)
        if temperature == None or humidity == None:
            self._log.error('Data CRC failed')
            return None
        else:
            if humidity > 0 and humidity < 100:
                return [
                    (self._name, 'temperature', temperature),
                    (self._name, 'humidity', humidity)
                ]
            else:
                self._log.error('Humidity out of range')
                return None


    def meta_data():
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
