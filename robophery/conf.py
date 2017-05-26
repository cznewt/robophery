
# Platform configs

FT232H_PLATFORM = {
    'interface': {
        'ft232h_gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.ft232h.gpio.Ft232hGpioInterface',
        },
        'ft232h_i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.ft232h.i2c.Ft232hI2cInterface',
        }
    }
}

NODEMCU_PLATFORM = {
    'interface': {
        'local_gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.nodemcu.gpio.NodeMcuGpioInterface',
        },
        'local_i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.nodemcu.i2c.NodeMcuI2cInterface',
            'parent': {
                'interface': 'local_gpio',
                'scl_pin': 5,
                'sda_pin': 4,
            }
        },
        'local_w1': {
            'engine': 'w1',
            'class': 'robophery.platform.nodemcu.w1.NodeMcuW1Interface',
            'parent': {
                'interface': 'local_gpio',
                'data_pin': 3,
            }
        },
    }
}

BBB_PLATFORM = {
    'interface': {
        'local_gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.bbb.gpio.BeagleboneGpioInterface',
        },
        'local_i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'bus_number': 2
        },
        'local_w1': {
            'engine': 'w1',
            'class': 'robophery.platform.linux.w1.LinuxW1Interface',
            'parent': {
                'interface': 'local_gpio',
                'pin': 4,
            }
        },
    },
}

RPI_PLATFORM = {
    'interface': {
        'local_gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.rpi.gpio.RaspberryPiGpioInterface',
        },
        'local_i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'bus_number': 1
        },
        'local_pwm': {
            'engine': 'pwm',
            'class': 'robophery.platform.rpi.pwm.LinuxW1Interface',
            'parent': {
                'interface': 'local_gpio',
                'pins': [4, 5, 10],
            }
        },
        'local_w1': {
            'engine': 'w1',
            'class': 'robophery.platform.linux.w1.LinuxW1Interface',
            'parent': {
                'interface': 'local_gpio',
                'pin': 4,
            }
        },
    },
}

RPI_PCA_PLATFORM = {
    'interface': {
        'local_gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.rpi.gpio.RaspberryPiGpioInterface',
        },
        'local_i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'bus_number': 1
        },
        'pca_pwm': {
            'engine': 'pwm',
            'class': 'robophery.platform.pca9685.pwm.Pca9685PwmInterface',
            'parent': {
                'interface': 'local_i2c',
                'address': 0x40,
            }
        },
    },
}


RPI_PCF_PLATFORM = {
    'interface': {
        'local_gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.rpi.gpio.RaspberryPiGpioInterface',
        },
        'local_i2c': {
            'engine': 'i2c',
            'class': 'robophery.platform.linux.i2c.SMBusI2cInterface',
            'bus_number': 1
        },
        'pcf_gpio': {
            'engine': 'gpio',
            'class': 'robophery.platform.pcf8574.gpio.Pcf8574GpioInterface',
            'parent': {
                'interface': 'local_i2c',
                'address': 0x3f,
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
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.bh1750.Bh1750Module',
}

BME280_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.bme280.Bme280Module',
}

BMP085_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.bmp085.Bmp085Module',
}

DHT11_MODULE = {
    'interface': 'local_gpio',
    'class': 'robophery.module.gpio.dht11.Dht11Module',
    'data_pin': None,
}

DHT22_MODULE = {
    'interface': 'local_gpio',
    'class': 'robophery.module.gpio.dht22.Dht22Module',
    'data_pin': None,
}

DS18_MODULE = {
    'interface': 'local_w1',
    'class': 'robophery.module.w1.ds18.Ds18Module',
    'addr': '00145071daff',
}

HCSR04_MODULE = {
    'interface': 'local_gpio',
    'class': 'robophery.module.gpio.hcsr04.Hcsr04Module',
    'echo_pin': None,
    'trigger_pin': None,
}

HD44780_PFC_MODULE = {
    'interface': 'pcf_gpio',
    'class': 'robophery.module.gpio.hd44780.Hd44780Module',
    'rs_pin': 0,
    'rw_pin': 1,
    'en_pin': 2,
    'bl_pin': 3,
    'd4_pin': 4,
    'd5_pin': 5,
    'd6_pin': 6,
    'd7_pin': 7,
    'cols': 20,
    'rows': 4,
    'auto_linebreaks': True,
    'backlight_enabled': True
}

HTU21D_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.htu21d.Htu21dModule',
}

INA219_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.ina219.Ina219Module',
}

L293D_MODULE = {
    'interface': 'local_gpio',
    'class': 'robophery.module.gpio.l293d.L293dModule',
    'power_pin': None,
    'forward_pin': None,
    'backward_pin': None,
}

MCP9808_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.mcp9808.Mcp9808Module',
}

MPU6050_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.mpu6050.Mpu6050Module',
}

PFP_MODULE = {
    'interface': 'local_ble',
    'class': 'robophery.module.ble.pfp.ParrotFlowerPowerModule',
}

RELAY_MODULE = {
    'interface': 'local_gpio',
    'class': 'robophery.module.gpio.relay.RelayModule',
    'data_pin': None,
}

SI7021_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.si7021.Si7021Module',
}

SERVO_MODULE = {
    'interface': 'pca_pwm',
    'class': 'robophery.module.pwm.servo.ServoModule',
    'data_pin': None,
}

SSD1306_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.ssd1306.Ssd1306Module',
}

SWITCH_MODULE = {
    'interface': 'local_gpio',
    'class': 'robophery.module.gpio.switch.SwitchModule',
    'data_pin': None,
}

T6713_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.tsl2561.T6713Module',
}

TCS34725_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.tcs34725.Tcs34725Module',
}

TSL2561_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.tsl2561.Tsl2561Module',
}

TSL2591_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.tsl2591.Tsl2591Module',
}

VL53L0X_MODULE = {
    'interface': 'local_i2c',
    'class': 'robophery.module.i2c.vl53l0x.Vl53L0XModule',
}
