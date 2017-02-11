
import robophery.w1


class Ds18Module(w1.W1Module):

    def __init__(self, *args, **kwargs):
        super(Ds18Module, self).__init__(*args, **kwargs)
        self._pin = kwargs.get('pin')
        self._type = kwargs.get('type', 'ds18b20')
        self._id = int(kwargs.get('id', '0'))


    @property
    def get_data(self):
        """
        Query Dallas DS18 family sensor to get the temperature readings.
        """
        if self._id == 0:
            return self._get_all_temperatures
        else:
            return self._get_temperature


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
                'range_low': -55,
                'range_high': 125,
                'sensor': 'ds18',
            },
        }
