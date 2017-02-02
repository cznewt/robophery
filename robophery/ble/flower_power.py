#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bluetooth.ble import GATTRequester, GATTResponse
import logging
from robophery.ble import BleModule
import struct

logger = logging.getLogger("robophery.ble.flower_power")

# Device information service
DEVICE_NAME_UUID = '2a00'
MANUFACTURER_NAME_UUID = '2a29'
FIRMWARE_REVISION_UUID = '2a26'
HARDWARE_REVISION_UUID = '2a27'
# Battery service
BATTERY_LEVEL_UUID = '2a19'
# Service addresses
FRIENDLY_NAME_UUID = "00002a00-0000-1000-8000-00805f9b34fb"
LED_UUID = "39e1fa07-84a8-11e2-afba-0002a5d5c51b"
LIGHT_UUID = "39e1fa01-84a8-11e2-afba-0002a5d5c51b"
SOIL_EC_UUID = "39e1fa02-84a8-11e2-afba-0002a5d5c51b"
SOIL_TEMPERATURE_UUID = "39e1fa03-84a8-11e2-afba-0002a5d5c51b"
AIR_TEMPERATURE_UUID = "39e1fa04-84a8-11e2-afba-0002a5d5c51b"
SOIL_MOISTURE_UUID = "39e1fa05-84a8-11e2-afba-0002a5d5c51b"


class FlowerPowerModule(BleModule):

    def __init__(self, kwargs):
        self.addr = kwargs.get('addr')
        self.debug = True
        self.requester = GATTRequester(self.addr, False)

    def connect(self):
        self.requester.connect(True)
#        chars = self.requester.discover_characteristics()
#        self.characteristic = {}
#        for char in chars:
#            self.characteristic[char['uuid']] = char['value_handle']


    def __del__(self):
        self.disconnect()


    def disconnect(self):
        self.requester.disconnect()


    def _convert_luminosity(self, value):
        raw_value = struct.unpack('H', value)[0] * 1.0;
        if raw_value > 0:
            luminosity = 0.08640000000000001 * (192773.17000000001 * pow(raw_value, -1.0606619))
        else:
            luminosity = 0
        return luminosity


    def _convert_temperature(self, value):
        raw_value = struct.unpack('H', value)[0] * 1.0;
        if raw_value != 0:
            temperature = 0.00000003044 * pow(raw_value, 3) - 0.00008038 * pow(raw_value, 2) + raw_value * 0.1149 - 30.449999999999999
        else:
            temperature = 0
        if temperature < -10.0:
            temperature = -10.0
        elif temperature > 55.0:
            temperature = 55.0
        return temperature


    def _convert_moisture(self, value):
        raw_value = struct.unpack('H', value)[0] * 1.0;
        soil_moisture = 11.4293 + (0.0000000010698 * pow(raw_value, 4) - 0.00000152538 * pow(raw_value, 3) +  0.000866976 * pow(raw_value, 2) - 0.169422 * raw_value)
        soil_moisture = 100.0 * (0.0000045 * pow(soil_moisture, 3) - 0.00055 * pow(soil_moisture, 2) + 0.0292 * soil_moisture - 0.053)

        if soil_moisture < 0.0:
            soil_moisture = 0.0
        elif soil_moisture > 60.0:
            soil_moisture = 60.0
        return soil_moisture


    def _convert_conductivity(self, value):
        raw_value = struct.unpack('H', value)[0] * 1.0;
        # TODO: convert raw (0 - 1771) to 0 to 10 (mS/cm)
        conductivity = raw_value
        return conductivity


    def set_led_status(self, status):
        status_hex = struct.pack('B', status)
        self.requester.write_by_handle(self.characteristic[LED_UUID], status_hex)


    @property
    def get_led_status(self):
        data = self.requester.read_by_uuid(LED_UUID)[0]
        led_status = int("".join("%02x" % ord(c) for c in data))
        return led_status


    def set_name(self, name):
        name_hex = struct.pack('B', name)
        self.requester.write_by_handle(self.characteristic[FRIENDLY_NAME_UUID], name_hex)


    @property
    def get_name(self):
        data = self.requester.read_by_uuid(FRIENDLY_NAME_UUID)[0]
        try:
            name = data.decode("utf-8")
        except AttributeError:
            name = data
        return name


    @property
    def get_battery_level(self):
        data = self.requester.read_by_uuid(BATTERY_LEVEL_UUID)[0]
        battery_level = int(data, 16)
        return battery_level


    @property
    def get_luminosity(self):
        data = self.requester.read_by_uuid(LIGHT_UUID)[0]
        return self._convert_luminosity(data)


    @property
    def get_air_temperature(self):
        data = self.requester.read_by_uuid(AIR_TEMPERATURE_UUID)[0]
        return self._convert_temperature(data)


    @property
    def get_soil_temperature(self):
        data = self.requester.read_by_uuid(SOIL_TEMPERATURE_UUID)[0]
        return self._convert_temperature(data)


    @property
    def get_soil_moisture(self):
        data = self.requester.read_by_uuid(SOIL_MOISTURE_UUID)[0]
        return self._convert_moisture(data)


    @property
    def get_soil_conductivity(self):
        data = self.requester.read_by_uuid(SOIL_EC_UUID)[0]
        return self._convert_conductivity(data)


    @property
    def get_characteristics(self):
        return self.characteristic


    @property
    def get_data(self):

        self.connect()

        output_str = "%s.{0}" % (self.name)

        values = []

        values.append((output_str.format("air_temperature"), self.get_air_temperature))
        values.append((output_str.format("soil_temperature"), self.get_soil_temperature))
        values.append((output_str.format("luminosity"), self.get_luminosity))
        values.append((output_str.format("soil_moisture"), self.get_soil_moisture))
        values.append((output_str.format("soil_conductivity"), self.get_soil_conductivity))
        values.append((output_str.format("battery_level"), self.get_battery_level))

        self.disconnect()

        return values

    @property
    def get_meta_data():
        """
        Get the readings meta-data.
        """
        return {
            'air_temperature': {
                'type': 'gauge',
                'unit': 'C',
                'precision': 2,
                'range_low': 0,
                'range_high': 100,
                'sensor': 'flower_power',
            },
            'soil_temperature': {
                'type': 'gauge',
                'unit': 'C',
                'precision': 2,
                'range_low': 0,
                'range_high': 100,
                'sensor': 'flower_power',
            }
        }
