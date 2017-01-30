#!/usr/bin/python

import logging
from robophery.gpio import GpioModule

logger = logging.getLogger("robophery.gpio.relay")


class RelayModule(GpioModule):


    def __init__(self, kwargs)
        self.name = kwargs.get('name')
        self.set_port(kwargs.get('port'))


    @property
    def get_data():
        """
        Relay status readings.
        """

        GPIO.setup(port, GPIO.IN)
        state = GPIO.input(self.port)

        runtime_count = runtime_delta = state
     
        values = [
            ('%s.runtime_count' % self.name, runtime_count, ),
            ('%s.runtime_delta' % self.name, runtime_delta, ),
        ]
        return values


    @property
    def get_meta_data():
        """
        Get the readings meta-data.
        """
        return {
            'runtime_count': {
                'type': 
                'unit': 'total seconds running',
                'range_low': 0,
                'range_high': None,
                'sensor': 'relay'
            },
            'runtime_delta': {
                'type': 
                'unit': 'seconds running per period',
                'range_low': 0,
                'range_high': None,
                'sensor': 'relay'
            }
        }
