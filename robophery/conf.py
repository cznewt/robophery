
# Platform configurations

FT232H_PLATFORM = {
    'interface': {
        'ft232h_gpio': {
            'class': 'robophery.platform.ft232h.gpio.Ft232hGpioInterface',
            'engine': 'gpio',
        },
        'ft232h_i2c': {
            'class': 'robophery.platform.ft232h.i2c.Ft232hI2cInterface',
            'engine': 'i2c',
        }
    }
}

NODEMCU_PLATFORM = {
    'interface': {
        'local_gpio': {
            'class': 'robophery.platform.nodemcu.gpio.NodeMcuGpioInterface',
            'engine': 'gpio',
        },
        'local_i2c': {
            'class': 'robophery.platform.nodemcu.i2c.NodeMcuI2cInterface',
            'engine': 'i2c',
            'data': {
                'iface': 'local_gpio',
                'pin': 4,
            },
            'clock': {
                'iface': 'local_gpio',
                'pin': 5,
            },
        },
        'local_w1': {
            'class': 'robophery.platform.nodemcu.w1.NodeMcuW1Interface',
            'engine': 'w1',
            'data': {
                'iface': 'local_gpio',
                'pin': 3,
            }
        },
    }
}

BBB_PLATFORM = {
    'interface': {
        'local_gpio': {
            'class': 'robophery.platform.bbb.gpio.BeagleboneGpioInterface',
            'engine': 'gpio',
        },
        'local_pwm': {
            'class': 'robophery.platform.bbb.pwm.BeaglebonePwmInterface',
            'engine': 'pwm',
        },
        'local_i2c': {
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'engine': 'i2c',
            'bus_number': 2
        },
        'local_w1': {
            'class': 'robophery.platform.linux.w1.LinuxW1Interface',
            'engine': 'w1',
            'data': {
                'iface': 'local_gpio',
                'pin': 4,
            }
        },
    },
}

RPI_PLATFORM = {
    'interface': {
        'local_gpio': {
            'class': 'robophery.platform.rpi.gpio.RaspberryPiGpioInterface',
            'engine': 'gpio',
        },
        'local_i2c': {
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'engine': 'i2c',
            'bus_number': 1
        },
    },
}

RPI_W1_PLATFORM = {
    'interface': {
        'local_gpio': {
            'class': 'robophery.platform.rpi.gpio.RaspberryPiGpioInterface',
            'engine': 'gpio',
        },
        'local_i2c': {
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'engine': 'i2c',
            'bus_number': 1
        },
        'local_w1': {
            'class': 'robophery.platform.linux.w1.LinuxW1Interface',
            'engine': 'w1',
            'data': {
                'iface': 'local_gpio',
                'pin': 4,
            }
        },
    },
}

RPI_PCA_PLATFORM = {
    'interface': {
        'local_gpio': {
            'class': 'robophery.platform.rpi.gpio.RaspberryPiGpioInterface',
            'engine': 'gpio',
        },
        'local_i2c': {
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'engine': 'i2c',
            'bus_number': 1
        },
        'pca_pwm': {
            'class': 'robophery.platform.pca9685.pwm.Pca9685PwmInterface',
            'engine': 'pwm',
            'data': {
                'iface': 'local_i2c',
                'addr': 0x40,
            }
        },
    },
}


RPI_PCF_PLATFORM = {
    'interface': {
        'local_gpio': {
            'class': 'robophery.platform.rpi.gpio.RaspberryPiGpioInterface',
            'engine': 'gpio',
        },
        'local_i2c': {
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'engine': 'i2c',
            'bus_number': 1
        },
        'pcf_gpio': {
            'class': 'robophery.platform.pcf8574.gpio.Pcf8574GpioInterface',
            'engine': 'gpio',
            'data': {
                'iface': 'local_i2c',
                'addr': 0x3f,
            }
        },
    },
}

# Communication configurations

LINUX_MQTT_COMM = {
    'class': 'robophery.comm.linux.mqtt.PahoMqttComm',
    'host': 'localhost',
    'port': 1883,
}

LINUX_STATSD_COMM = {
    'class': 'robophery.comm.linux.statsd.GenericStatsdComm',
    'host': 'localhost',
    'port': 8125,
}

# Physical module configurations


AM2320_MODULE = {
    'class': 'robophery.module.i2c.am2320.Am2320Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x5c,
    },
}


BH1750_MODULE = {
    'class': 'robophery.module.i2c.bh1750.Bh1750Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x23,
    },
}

BME280_MODULE = {
    'class': 'robophery.module.i2c.bme280.Bme280Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x77,
    },
}

BMP085_MODULE = {
    'class': 'robophery.module.i2c.bmp085.Bmp085Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x77,
    },
}

DHT11_MODULE = {
    'class': 'robophery.module.gpio.dht11.Dht11Module',
    'data': {
        'iface': 'local_gpio',
        'pin': None,
    },
}

DHT22_MODULE = {
    'class': 'robophery.module.gpio.dht22.Dht22Module',
    'data': {
        'iface': 'local_gpio',
        'pin': None,
    },
}

DS18_MODULE = {
    'class': 'robophery.module.w1.ds18.Ds18Module',
    'data': {
        'iface': 'local_w1',
        'addr': '00145071daff',
    },
}

HCSR04_MODULE = {
    'class': 'robophery.module.gpio.hcsr04.Hcsr04Module',
    'echo': {
        'iface': 'local_gpio',
        'pin': None,
    },
    'trigger': {
        'iface': 'local_gpio',
        'pin': None,
    },
}

HD44780_PFC_MODULE = {
    'class': 'robophery.module.gpio.hd44780.Hd44780Module',
    'rs': {
        'iface': 'pcf_gpio',
        'pin': 0,
    },
    'rw': {
        'iface': 'pcf_gpio',
        'pin': 1,
    },
    'en': {
        'iface': 'pcf_gpio',
        'pin': 2,
    },
    'bl': {
        'iface': 'pcf_gpio',
        'pin': 3,
    },
    'd4': {
        'iface': 'pcf_gpio',
        'pin': 4,
    },
    'd5': {
        'iface': 'pcf_gpio',
        'pin': 5,
    },
    'd6': {
        'iface': 'pcf_gpio',
        'pin': 6,
    },
    'd7': {
        'iface': 'pcf_gpio',
        'pin': 7,
    },
    'cols': 20,
    'rows': 4,
    'linebreaks': False,
    'backlight': True
}

HTU21D_MODULE = {
    'class': 'robophery.module.i2c.htu21d.Htu21dModule',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x40,
    },
}

INA219_MODULE = {
    'class': 'robophery.module.i2c.ina219.Ina219Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x40,
    },
}

L293D_MODULE = {
    'class': 'robophery.module.gpio.l293d.L293dModule',
    'power': {
        'iface': 'local_gpio',
        'pin': None,
    },
    'forward': {
        'iface': 'local_gpio',
        'pin': None,
    },
    'backward': {
        'iface': 'local_gpio',
        'pin': None,
    },
}

L293D_PWM_MODULE = {
    'class': 'robophery.module.pwm.l293d.L293dModule',
    'power': {
        'iface': 'local_pwm',
        'pin': None,
    },
    'forward': {
        'iface': 'local_gpio',
        'pin': None,
    },
    'backward': {
        'iface': 'local_gpio',
        'pin': None,
    },
}

MCP9808_MODULE = {
    'class': 'robophery.module.i2c.mcp9808.Mcp9808Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x18,
    },
}

MPU6050_MODULE = {
    'class': 'robophery.module.i2c.mpu6050.Mpu6050Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x68,
    },
}

PFP_MODULE = {
    'class': 'robophery.module.ble.pfp.ParrotFlowerPowerModule',
    'data': {
        'iface': 'local_ble',
        'addr': None,
    },
}

RELAY_MODULE = {
    'class': 'robophery.module.gpio.relay.RelayModule',
    'data': {
        'iface': 'local_gpio',
        'pin': None,
    },
}

SI7021_MODULE = {
    'class': 'robophery.module.i2c.si7021.Si7021Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x40,
    },
}

SERVO_MODULE = {
    'class': 'robophery.module.pwm.servo.ServoModule',
    'data': {
        'iface': 'pca_pwm',
        'pin': None,
    },
}

SSD1306_MODULE = {
    'class': 'robophery.module.i2c.ssd1306.Ssd1306Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x3c,
    },
    'reset': {
        'iface': 'local_gpio',
        'pin': None,
    },
}

SWITCH_MODULE = {
    'class': 'robophery.module.gpio.switch.SwitchModule',
    'data': {
        'iface': 'local_gpio',
        'pin': None,
    },
}

T6713_MODULE = {
    'class': 'robophery.module.i2c.tsl2561.T6713Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x15,
    },
}

TCS34725_MODULE = {
    'class': 'robophery.module.i2c.tcs34725.Tcs34725Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x29,
    },
}

TSL2561_MODULE = {
    'class': 'robophery.module.i2c.tsl2561.Tsl2561Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x39,
    },
}

TSL2591_MODULE = {
    'class': 'robophery.module.i2c.tsl2591.Tsl2591Module',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x29,
    },
}

VL53L0X_MODULE = {
    'class': 'robophery.module.i2c.vl53l0x.Vl53L0XModule',
    'data': {
        'iface': 'local_i2c',
        'addr': 0x29,
    },
}

# Virtual module configurations

