import Adafruit_DHT
from robophery.gpio import GpioModule


class Dht22Module(GpioModule):
    """
    Module for DHT22 temperature and humidity sensor.
    """
    DEVICE_NAME = 'gpio-dht22'

    READ_INTERVAL = 5000


    def __init__(self, *args, **kwargs):
        super(Dht22Module, self).__init__(*args, **kwargs)
        self._pin = self._normalize_pin(kwargs.get('pin'))
        self._type = 22


    @property
    def do_action(self, action):
        if action == 'get_data':
            return self.get_data


    @property
    def get_data(self):
        """
        Query DHT22 to get the humidity and temperature readings.
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


    @property
    def get_meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'temperature': {
                'type': 'gauge', 
                'unit': 'C',
                'precision': 0.5,
                'range_low': -40,
                'range_high': 80,
                'sensor': 'dht22'
            },
            'humidity': {
                'type': 'gauge',
                'unit': 'RH',
                'precision': 5,
                'range_low': 0,
                'range_high': 100,
                'sensor': 'dht22'
            }
        }
