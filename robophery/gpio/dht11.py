#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_DHT
import logging
from robophery.gpio import GpioModule

logger = logging.getLogger("robophery.gpio.dht11")


class Dht11Module(GpioModule):

    def __init__(self, kwargs)
        self.name = kwargs.get('name')
        self.type = 11
        self.set_port(kwargs.get('port'))


    @property
    def get_data():
        """
        Query DHT11 to get the humidity and temperature readings.
        """

        data = []

        humidity, temperature = Adafruit_DHT.read_retry(self.type, self.port)

        if temperature == None or humidity == None:
            logger.error("%s: Data CRC failed" % name)
            temperature = None
            humidity = None
        else:
            if humidity < 0 or humidity > 100:
                logger.error("%s: Humidity out of range" % name)
                humidity = None
            else:
                data.append(('%s.temperature' % (self.name), temperature, ))
                data.append(('%s.humidity' % (self.name), humidity, ))

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
