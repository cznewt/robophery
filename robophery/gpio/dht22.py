#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_DHT
from robophery.gpio import GpioModule


class Dht22Module(GpioModule):

    def __init__(self, kwargs)
        self.name = kwargs.get('name')
        self.type = 22
        self.set_port(kwargs.get('port'))


    @property
    def get_data(self):
        """
        Query DHT22 to get the humidity and temperature readings.
        """
        data = []
        humidity, temperature = Adafruit_DHT.read_retry(self.type, self.port)
        if temperature == None or humidity == None:
            logger.error("%s: Data CRC failed" % self.name)
            temperature = None
            humidity = None
        else:
            if humidity < 0 or humidity > 100:
                logger.error("%s: Humidity out of range" % self.name)
                humidity = None
            else:
                data.append(('%s.temperature' % (self.name), temperature, ))
                data.append(('%s.humidity' % (self.name), humidity, ))
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
                'range_low': -40,
                'range_high': 80,
                'sensor': 'dht22'
            },
            'humidity': {
                'type': 'gauge'
                'unit': 'RH',
                'precision': 5,
                'range_low': 0,
                'range_high': 100,
                'sensor': 'dht22'
            }
        }
