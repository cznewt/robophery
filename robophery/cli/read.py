#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from oslo_config import cfg

def _get_i2c_opts():
    common_opts = [
        cfg.Opt('bus',
                short='b',
                default="1",
                help='I2C bus'),
    ]
    CONF = cfg.CONF
    CONF.register_cli_opts(common_opts)
    CONF(sys.argv[1:])
    return CONF


def read_bh1750():

    from robophery.i2c.bh1750 import Bh1750Module
    config = _get_i2c_opts()
    module = Bh1750Module(config)
    print(module.get_data)
