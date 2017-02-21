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


def service_dht22():
    from robophery.gpio.dht22 import Dht22Module
    config = _config(_gpio_opts)
    module = Dht22Module(**config)
    module.start_service


def service_switch():
    from robophery.gpio.switch import SwitchModule
    config = _config(_gpio_opts)
    module = SwitchModule(**config)
    module.start_service