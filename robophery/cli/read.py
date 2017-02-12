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

_ble_opts = [
    cfg.Opt('name',
        short='n',
        default="sensor",
        help='Sensor name'),
    cfg.Opt('addr',
        short='a',
        help='MAC address of sensor'),
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


def read_relay():
    from robophery.gpio.relay import RelayModule
    config = _config(_gpio_opts)
    module = RelayModule(**config)
    print(module.get_data)


def read_switch():
    from robophery.gpio.switch import SwitchModule
    config = _config(_gpio_opts)
    module = SwitchModule(**config)
    print(module.get_data)

# BLE modules


def read_flower_power():
    from robophery.ble.flower_power import FlowerPowerModule
    config = _config(_ble_opts)
    module = FlowerPowerModule(**config)
    print(module.get_data)

# 1-wire modules


def read_ds18():
    from robophery.w1.ds18 import Ds18Module
    _gpio_opts.append(cfg.Opt('type',
        short='t',
        default="ds18b20",
        help='Specific type of Dallas DS18 family sensor'))
    _gpio_opts.append(cfg.Opt('id',
        short='i',
        default='0',
        help='Specific sensor address ID at 1-wire bus'))
    config = _config(_gpio_opts)
    module = Ds18Module(**config)
    print(module.get_data)
