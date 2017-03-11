from robophery.module.w1.base import W1Module


class Ds18Module(W1Module):

    def __init__(self, *args, **kwargs):
        super(Ds18Module, self).__init__(*args, **kwargs)
        self._id = kwargs.get('id', '0')
        self._type = kwargs.get('type', 'ds18b20')


    def read_data(self):
        """
        Query Dallas DS18 family sensor to get the temperature readings.
        """
        if self._id == '0':
            data = self._get_all_temperatures()
            if len(data) == 0:
                return None
        else:
            data = self._get_temperature()
        return data


    def meta_data(self):
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
