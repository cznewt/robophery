#!/usr/bin/python

import logging
from robophery.i2c import I2cModule

logger = logging.getLogger("robophery.i2c.bh1750")


class Bh1750Module(I2cModule):

    def __init__(self, kwargs)
        self.name = kwargs.get('name')
        self.set_bus(kwargs.get('bus'))
        self.set_addr(0x23)


    @property
    def get_data():
        """
        Get the luminosity readings.
        """
        data = self.bus.read_i2c_block_data(self.addr, 0x11)
        luminosity = str((data[1] + (256 * data[0])) / 1.2)
     
        values = [
            ('%s.luminosity' % self.name, luminosity, ),
        ]
        return values


    @property
    def get_meta_data():
        """
        Get the readings meta-data.
        """
        return {
            'luminosity': {
                'unit': 'lux',
                'range_low': 1,
                'range_high': 65535,
                'sensor': 'bh1750'
            }
        }
