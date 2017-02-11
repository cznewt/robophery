#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from oslo_config import cfg

_gpio_opts = [
    cfg.Opt('name',
        short='n',
        default="sensor",
        help='Sensor name'),
    cfg.Opt('pin',
        short='p',
        help='GPIO pin of sensor'),
]

_i2c_opts = [
    cfg.Opt('name',
        short='n',
        default="sensor",
        help='Sensor name'),
    cfg.Opt('bus',
        short='b',
        default="1",
        help='I2C bus'),
]


def _config(opts):
    CONF = cfg.CONF
    CONF.register_cli_opts(opts)
    CONF(sys.argv[1:])
    return CONF

# I2C modules

def read_bh1750():
    from robophery.i2c.bh1750 import Bh1750Module
    config = _config(_i2c_opts)
    module = Bh1750Module(**config)
    print(module.get_data)


def read_mcp9808():
    from robophery.i2c.mcp9808 import Mcp9808Module
    config = _config(_i2c_opts)
    module = Mcp9808Module(**config)
    print(module.get_data)

# GPIO modules

def read_dht22():
    from robophery.gpio.dht22 import Dht22Module
    config = _config(_gpio_opts)
    module = Dht22Module(**config)
    print(module.get_data)


def read_l293d():
    from robophery.gpio.l293d import L293dModule
    opts = [
        cfg.Opt('name',
            short='n',
            default="l293d",
            help='L293D driver name'),
        cfg.Opt('power_pin',
            short='a',
            help='L293D pin 1 or pin 9: On or off'),
        cfg.Opt('forward_pin',
            short='b',
            help='L293D pin 2 or pin 10: Anticlockwise positive'),
        cfg.Opt('backward_pin',
            short='c',
            help='L293D pin 7 or pin 15: Clockwise positive'),
    ]
    config = _config(opts)
    module = L293dModule(**config)
    print(module.get_data)


def read_switch():
    from robophery.gpio.switch import SwitchModule
    config = _config(_gpio_opts)
    module = SwitchModule(**config)
    print(module.get_data)
