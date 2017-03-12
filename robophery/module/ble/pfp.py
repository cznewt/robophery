from robophery.module.ble.base import BleModule


class ParrotFlowerPowerModule(BleModule):
    """
    Module for Parrot Flower Power.
    """
    DEVICE_NAME = 'ble-pfp'

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


    def __init__(self, *args, **kwargs):
        super(FlowerPowerModule, self).__init__(*args, **kwargs)


    def set_led_status(self, status):
        self._write_uuid(self.FRIENDLY_NAME_UUID, status, 'string')


    @property
    def get_led_status(self):
        data = self.requester.read_by_uuid(LED_UUID)[0]
        led_status = int("".join("%02x" % ord(c) for c in data))
        return led_status


    def set_name(self, name):
        self._write_uuid(self.FRIENDLY_NAME_UUID, name, 'string')


    @property
    def get_name(self):
        return self._read_uuid(self.FRIENDLY_NAME_UUID, 'string')


    @property
    def get_battery_level(self):
        raw_value = self._read_uuid(self.BATTERY_LEVEL_UUID)
        battery_level = int(raw_value, 16)
        return battery_level


    @property
    def get_luminosity(self):
        raw_value = self._read_uuid(self.LIGHT_UUID)
        if raw_value > 0:
            luminosity = 0.08640000000000001 * (192773.17000000001 * pow(raw_value, -1.0606619))
        else:
            luminosity = 0
        return luminosity


    @property
    def get_air_temperature(self):
        raw_value = self._read_uuid(self.AIR_TEMPERATURE_UUID)
        if raw_value != 0:
            temperature = 0.00000003044 * pow(raw_value, 3) - 0.00008038 * pow(raw_value, 2) + raw_value * 0.1149 - 30.449999999999999
        else:
            temperature = 0
        if temperature < -10.0:
            temperature = -10.0
        elif temperature > 55.0:
            temperature = 55.0
        return temperature


    @property
    def get_soil_temperature(self):
        raw_value = self._read_uuid(self.SOIL_TEMPERATURE_UUID)
        if raw_value != 0:
            temperature = 0.00000003044 * pow(raw_value, 3) - 0.00008038 * pow(raw_value, 2) + raw_value * 0.1149 - 30.449999999999999
        else:
            temperature = 0
        if temperature < -10.0:
            temperature = -10.0
        elif temperature > 55.0:
            temperature = 55.0
        return temperature


    @property
    def get_soil_moisture(self):
        raw_value = self._read_uuid(self.SOIL_MOISTURE_UUID)
        soil_moisture = 11.4293 + (0.0000000010698 * pow(raw_value, 4) - 0.00000152538 * pow(raw_value, 3) +  0.000866976 * pow(raw_value, 2) - 0.169422 * raw_value)
        soil_moisture = 100.0 * (0.0000045 * pow(soil_moisture, 3) - 0.00055 * pow(soil_moisture, 2) + 0.0292 * soil_moisture - 0.053)
        if soil_moisture < 0.0:
            soil_moisture = 0.0
        elif soil_moisture > 60.0:
            soil_moisture = 60.0
        return soil_moisture


    @property
    def get_soil_conductivity(self):
        raw_value = self._read_uuid(self.SOIL_EC_UUID)
        # TODO: convert raw (0 - 1771) to 0 to 10 (mS/cm)
        conductivity = raw_value
        return conductivity


    @property
    def get_data(self):
        self._connect()
        values = [
            (self._name, "air_temperature", self.get_air_temperature),
            (self._name, "soil_temperature", self.get_soil_temperature),
            (self._name, "luminosity", self.get_luminosity),
            (self._name, "soil_moisture", self.get_soil_moisture),
            (self._name, "soil_conductivity", self.get_soil_conductivity),
            #(self._name, "battery_level", self.get_battery_level),
            (self._name, "led_status", self.get_led_status),
        ]
        self._disconnect()
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
