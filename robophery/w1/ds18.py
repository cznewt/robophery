
import robophery.w1


class Ds18Module(robophery.w1.W1Module):

    def __init__(self, *args, **kwargs):
        super(Ds18Module, self).__init__(*args, **kwargs)
        self._id = int(kwargs.get('id', '0'))
        self._type = kwargs.get('type', 'ds18b20')


    @property
    def get_data(self):
        """
        Query Dallas DS18 family sensor to get the temperature readings.
        """
        if self._id == 0:
            data = self._get_all_temperatures
            if len(data) == 0:
                return None
        else:
            data = self._get_temperature
        return data

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
