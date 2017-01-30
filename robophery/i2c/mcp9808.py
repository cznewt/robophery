#!/usr/bin/python

import logging
from Adafruit_I2C import Adafruit_I2C
from robophery.i2c import I2cModule

logger = logging.getLogger("robophery.i2c.mcp9808")

MCP9808_I2CADDR_DEFAULT = 0x18
MCP9808_REG_CONFIG_SHUTDOWN = 0x0100
MCP9808_REG_CONFIG_CRITLOCKED = 0x0080
MCP9808_REG_CONFIG_WINLOCKED = 0x0040
MCP9808_REG_CONFIG_INTCLR = 0x0020
MCP9808_REG_CONFIG_ALERTSTAT = 0x0010
MCP9808_REG_CONFIG_ALERTCTRL = 0x0008
MCP9808_REG_CONFIG_ALERTSEL = 0x0002
MCP9808_REG_CONFIG_ALERTPOL = 0x0002
MCP9808_REG_CONFIG_ALERTMODE = 0x0001
MCP9808_REG_CONFIG = 0x01
MCP9808_REG_UPPER_TEMP = 0x02
MCP9808_REG_LOWER_TEMP = 0x03
MCP9808_REG_CRIT_TEMP = 0x04
MCP9808_REG_AMBIENT_TEMP = 0x05
MCP9808_REG_MANUF_ID = 0x06
MCP9808_REG_DEVICE_ID = 0x07


class Mcp9808Module(I2cModule):

    def __init__(self, kwargs)
        self.name = kwargs.get('name', 'mcp9808')
        self.set_bus(kwargs.get('bus', -1))
        self.set_addr(kwargs.get('addr', MCP9808_I2CADDR_DEFAULT))

        self._i2c = Adafruit_I2C(address=self.address, busnum=self.bus)

        # Assert it's the right thing
        mid = self._readU16(MCP9808_REG_MANUF_ID) 

        if mid != 0x0054:
            logger.error('Not right manufacturer (0x54): %s' % mid)
        did = self._readU16(MCP9808_REG_DEVICE_ID) 

        if did != 0x0400:
            logger.error('Not right device ID (0x4): %s' % did)


    def _readU16(self, reg):
        ret = self._i2c.readList(reg, 2)
        if ret == -1:
            return ret
        else:
            return (ret[0] << 8) + ret[1]


    @property
    def get_data():
        """
        Get the temperature readings.
        """
        data = self._readU16(MCP9808_REG_AMBIENT_TEMP)
        temperature = data & 0x0FFF
        temperature /= 16.0
        if data & 0x1000: temperature -= 256
     
        values = [
            ('%s.temperature' % self.name, temperature, ),
        ]
        return values


    @property
    def get_meta_data():
        """
        Get the readings meta-data.
        """
        return {
            'temperature': {
                'unit': 'celsius',
                'precision' 0.25,
                'range_low': -40,
                'range_high': 125,
                'sensor': 'mcp9808'
            }
        }
