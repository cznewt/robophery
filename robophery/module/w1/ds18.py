from robophery.module.w1.base import W1Module


class Ds18Module(W1Module):

    def __init__(self, *args, **kwargs):
        super(Ds18Module, self).__init__(*args, **kwargs)
        self._addr = kwargs.get('addr', '0')
        self._type = kwargs.get('type', 'ds18b20')


    def read_data(self):
        """
        Query Dallas DS18 family sensor to get the temperature readings.
        """
        if self._addr in ['0', None]:
            raw_data = self._get_all_temperatures()
            if len(raw_data) == 0:
                return None
            else:
                data = []
                for raw_name, raw_value in raw_data:
                    data.append(('%s-%s' % (self._name, raw_name), 'temperature', raw_value))
        else:
            data = (self._name, 'temperature', self._get_temperature())

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
