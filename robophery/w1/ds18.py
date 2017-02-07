#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from robophery.w1 import W1Module

logger = logging.getLogger("robophery.w1.ds18")


class Ds18Module(W1Module):

    def __init__(self, kwargs):
        self.name = kwargs.get('name')
        self.set_port(kwargs.get('port'))
        self.addr = int(kwargs.get("addr", '0'))
        self.type = kwargs.get("type", 'ds18b20')
        super(Ds18Module, self).__init__()

    @property
    def get_data(self):
        """
        Query Dallas DS18 family sensor to get the temperature readings.
        """
        data = []

        if self.addr == 0:
            for sensor in W1ThermSensor.get_available_sensors():
                data.append(('%s-%s.temperature' % (self.name, sensor.id), sensor.get_temperature()))
        else:
            if self.type == 'ds18b20':
                real_type == W1ThermSensor.THERM_SENSOR_DS18B20
            sensor = W1ThermSensor(real_type, self.addr)
            data.append(('%s.temperature' % self.name, sensor.get_temperature()))

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
