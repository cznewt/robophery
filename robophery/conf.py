
# Platform configs

FT232H_PLATFORM = {
    'interface': {
        'ft232h-gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.ft232h.gpio.Ft232hGpioInterface',
        },
        'ft232h-i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.ft232h.i2c.Ft232hI2cInterface',
        }
    }
}

NODEMCU_PLATFORM = {
    'interface': {
        'local-gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.nodemcu.gpio.NodeMcuGpioInterface',
        },
        'local-i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.nodemcu.i2c.NodeMcuI2cInterface',
            'uses': {
                'interface': 'local-gpio',
                'scl_pin': 5,
                'sda_pin': 4,
            }
        }
        'local-w1': {
            'engine': 'w1',
            'class': 'robophery.platform.linux.w1.LinuxW1Interface',
            'uses': {
                'interface': 'local-gpio',
                'data_pin': 3,
            }
        },
    }
}

BBB_PLATFORM = {
    'interface': {
        'local-gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.bbb.gpio.BeagleboneGpioInterface',
        },
        'local-i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'bus_number': 2
        },
        'local-w1': {
            'engine': 'w1',
            'class': 'robophery.platform.linux.w1.LinuxW1Interface',
            'uses': {
                'interface': 'local-gpio',
                'pin': 4,
            }
        },
    },
}

RPI_PLATFORM = {
    'interface': {
        'local-gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.rpi.gpio.RaspberryPiGpioInterface',
        },
        'local-i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'bus_number': 1
        },
        'local-w1': {
            'engine': 'w1',
            'class': 'robophery.platform.linux.w1.LinuxW1Interface',
            'uses': {
                'interface': 'local-gpio',
                'pin': 4,
            }
        },
    },
}

# Communication configs

LINUX_MQTT_COMM = {
    'host': 'localhost',
    'port': 1883,
    'class': 'robophery.comm.linux.mqtt.PahoMqttComm',
}

LINUX_STATSD_COMM = {
    'host': 'localhost',
    'port': 8125,
    'class': 'robophery.comm.linux.statsd.GenericStatsdComm',
}

# Module configs

BH1750_MODULE = {
    'interface': 'local-i2c',
    'class': 'robophery.module.i2c.bh1750.Bh1750Module',
}

BMP085_MODULE = {
    'interface': 'local-i2c',
    'class': 'robophery.module.i2c.bmp085.Bmp085Module',
}

DHT11_MODULE = {
    'interface': 'local-gpio',
    'class': 'robophery.module.gpio.dht11.Dht11Module',
    'data_pin': None,
}

DHT22_MODULE = {
    'interface': 'local-gpio',
    'class': 'robophery.module.gpio.dht22.Dht22Module',
    'data_pin': None,
}

DS18_MODULE = {
    'interface': 'local-w1',
    'class': 'robophery.module.w1.ds18.Ds18Module',
}

HTU21D_MODULE = {
    'interface': 'local-i2c',
    'class': 'robophery.module.i2c.htu21d.Htu21dModule',
}

INA219_MODULE = {
    'interface': 'local-i2c',
    'class': 'robophery.module.i2c.ina219.Ina219Module',
}

L293D_MODULE = {
    'interface': 'local-gpio',
    'class': 'robophery.module.gpio.l293d.L293dModule',
    'power_pin': None,
    'forward_pin': None,
    'backward_pin': None,
}

MCP9808_MODULE = {
    'interface': 'local-i2c',
    'class': 'robophery.module.i2c.mcp9808.Mcp9808Module',
}

PFP_MODULE = {
    'interface': 'local-ble',
    'class': 'robophery.module.ble.pfp.ParrotFlowerPowerModule',
}

RELAY_MODULE = {
    'interface': 'local-gpio',
    'class': 'robophery.module.gpio.relay.RelayModule',
    'data_pin': None,
}

SI7021_MODULE = {
    'interface': 'local-i2c',
    'class': 'robophery.module.i2c.si7021.Si7021Module',
}

SWITCH_MODULE = {
    'interface': 'local-gpio',
    'class': 'robophery.module.gpio.switch.SwitchModule',
    'data_pin': None,
}
