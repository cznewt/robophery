#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from oslo_config import cfg
from robophery.base import ModuleManager
from robophery.config import *

GPIO_OPTS = [
    cfg.Opt('data_pin',
        short='p',
        help='GPIO pin of module'),
]

BLE_OPTS = [
    cfg.Opt('addr',
        short='a',
        help='MAC address of module'),
]


def _config(module_conf, opts = None):
    conf = {
        'read_interval': 2000,
        'platform': 'raspberrypi',
        'config': RPI_PLATFORM
    }
    conf['config']['module'] = {
        'module': module_conf,
    }
    if opts != None:
        CONF = cfg.CONF
        CONF.register_cli_opts(opts)
        CONF(sys.argv[1:])
        conf.update(CONF)
    print conf
    return conf

# I2C modules

def read_bh1750():
    config = _config(BH1750_MODULE)
    manager = ModuleManager(**config)
    manager.run()


def read_htu21d():
    config = _config(HTU21D_MODULE)
    manager = ModuleManager(**config)
    manager.run()

# GPIO modules

def read_dht22():
    config = _config(DHT22_MODULE, GPIO_OPTS)
    manager = ModuleManager(**config)
    manager.run()


def read_l293d():
    OPTS = [
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
    config = _config(L293D_MODULE, OPTS)
    manager = ModuleManager(**config)
    manager.run()

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
