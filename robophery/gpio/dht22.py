#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_DHT
from robophery.gpio import GpioModule


class Dht22Module(GpioModule):

    DEVICE_NAME = 'gpio-dht22'


    def __init__(self, **kwargs)
        super(Dht22Module, self, **kwargs).__init__()
        self._type = 22
        self._port = kwargs.get('port')


    @property
    def get_data(self):
        """
        Query DHT22 to get the humidity and temperature readings.
        """
        data = []
        humidity, temperature = Adafruit_DHT.read_retry(self._type, self._port)
        if temperature == None or humidity == None:
            logger.error("%s: Data CRC failed" % self._name)
            temperature = None
            humidity = None
        else:
            if humidity < 0 or humidity > 100:
                logger.error("%s: Humidity out of range" % self._name)
                humidity = None
            else:
                data.append(('%s.temperature' % (self._name), temperature, ))
                data.append(('%s.humidity' % (self._name), humidity, ))
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
