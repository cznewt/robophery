
from robophery.module.i2c.base import I2cModule


class Mcp9808Module(I2cModule):
    """
    Module for MCP9808 temperature sensor.
    """
    DEVICE_NAME = 'i2c-mcp9808'
    DEVICE_ADDR = 0x18

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


    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', self.DEVICE_ADDR)
        super(Mcp9808Module, self).__init__(*args, **kwargs)
        # Assert it's the right thing
        mid = self.readU16(self.MCP9808_REG_MANUF_ID) 
        if mid != 0x0054:
            self._log.error('Not right manufacturer (0x54): %s' % mid)
        did = self.readU16(self.MCP9808_REG_DEVICE_ID) 
        if did != 0x0400:
            self._log.error('Not right device ID (0x4): %s' % did)


    def read_data(self):
        """
        Get the temperature readings.
        """
        data = self.readU16(self.MCP9808_REG_AMBIENT_TEMP)
        temperature = data & 0x0FFF
        temperature /= 16.0
        if data & 0x1000: temperature -= 256
        return [
            (self._name, 'temperature', temperature),
        ]


    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'temperature': {
                'type': 'gauge',
                'unit': 'C',
                'precision': 0.25,
                'range_low': -40,
                'range_high': 125,
                'sensor': self.DEVICE_NAME
            }
        }
