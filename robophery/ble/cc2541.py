#!/usr/bin/env python
# -*- coding: utf-8 -*-

from robophery.ble import BleModule


class Cc2541Module(BleModule):

    def __init__(self, kwargs):
        self.debug = kwargs.get('debug', False)
        self.addr = kwargs.get('addr')
        super(Cc2541Module, self).__init__()
