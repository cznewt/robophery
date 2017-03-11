
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
        }
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
            'class': 'robophery.platform.bbb.gpio.BeagleboneI2cInterface',
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
            'class': 'robophery.platform.linux.gpio.SMBusI2cInterface',
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

BH1750_MODULE = {
    'interface': 'local-i2c',
    'class': 'robophery.module.i2c.bh1750.Bh1750Module',
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

PFP_MODULE = {
    'interface': 'local-ble',
    'class': 'robophery.module.ble.pfp.ParrotFlowerPowerModule',
}
