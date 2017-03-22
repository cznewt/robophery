import time
from robophery.module.w1.base import W1Module


class Ds18Module(W1Module):
    """
    Module for Dallas 1-wire DS family temperature sensors.
    """
    DEVICE_NAME = 'w1-ds18'

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('address', '0')
        self._type = kwargs.get('type', 'DS18B20')
        super(Ds18Module, self).__init__(*args, **kwargs)

    def __str__(self):
        if self._addr in ['0', None]:
            return "{0} (addresses {1})".format(self._base_name(), ', '.join(self._interface._get_devices()))
        else:
            return "{0} (address {1})".format(self._base_name(), self._addr)

    def read_data(self):
        """
        Query Dallas DS18 family sensor to get the temperature readings.
        """
        data = []
        if self._addr in ['0', None]:
            read_time_start = time.time()
            raw_data = self._get_all_temperatures()
            read_time_stop = time.time()
            if len(raw_data) == 0:
                return None
            else:
                read_time_delta = (
                    read_time_stop - read_time_start) / len(raw_data)
                for raw_name, raw_value in raw_data.items():
                    data.append(('{0}-{1}'.format(self._name, raw_name),
                                 'temperature', raw_value, read_time_delta))
        else:
            read_time_start = time.time()
            temperature = self._get_temperature(self._addr, self._type)
            read_time_stop = time.time()
            read_time_delta = read_time_stop - read_time_start
            data.append((self._name, 'temperature',
                         temperature, read_time_delta))
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
                'precision': 0.5,
                'range_low': -55,
                'range_high': 125,
                'sensor': 'ds18',
            },
        }
