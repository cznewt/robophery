import Adafruit_DHT
from robophery.gpio import GpioModule


class Dht11Module(GpioModule):

    DEVICE_NAME = 'gpio-dht11'


    def __init__(self, *args, **kwargs):
        super(Dht11Module, self).__init__(*args, **kwargs)
        self._pin = kwargs.get('pin')
        self._type = 11


    @property
    def get_data(self):
        """
        Query DHT11 to get the humidity and temperature readings.
        """
        data = []
        humidity, temperature = Adafruit_DHT.read_retry(self._type, self._pin)
        if temperature == None or humidity == None:
            self._log('error', 'Data CRC failed')
        else:
            if humidity > 0 and humidity < 100:
                data.append(('%s.temperature' % (self._name), temperature, ))
                data.append(('%s.humidity' % (self._name), humidity, ))
            else:
                self._log('error', 'Humidity out of range')
        return data


    @property
    def get_meta_data():
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
