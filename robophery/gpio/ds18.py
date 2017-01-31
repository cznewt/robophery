#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from robophery.gpio import GpioModule
from w1thermsensor import W1ThermSensor

logger = logging.getLogger("robophery.gpio.ds18")


class Ds18Module(GpioModule):

    def __init__(self, kwargs)
        self.name = kwargs.get('name')
        self.id = int(kwargs.get("id", '0'))
        self.type = kwargs.get("type", 'DS18B20')
        self.set_port(kwargs.get('port'))


    @property
    def get_data():
        """
        Query Dallas DS18 to get the humidity and temperature readings.
        """
        data = []

        try:
            if id == 0:
                for sensor in W1ThermSensor.get_available_sensors():
                    data.append(('%s-%s.temperature' % (self.name, sensor.id), sensor.get_temperature()))
            else:
                if self.type == 'DS18B20':
                    real_type == W1ThermSensor.THERM_SENSOR_DS18B20
                sensor = W1ThermSensor(real_type, id)
                data.append(('%s.temperature' % (self.name), sensor.get_temperature()))
        except Exception, e:
            logger.error('%s: %s' % (name, e))

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
                'precision': 0.5,
                'range_low': -55,
                'range_high': 125,
                'sensor': 'ds18',
            },
        }
