#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

#import Adafruit_BMP.BMP085 as BMP085
import sys
import time
sys.path.append('/root/sdcard/git/robophery-dev/')

from robophery.i2c.bmp085 import Bmp085Module

def main():
    bmp180sensor = Bmp085Module(name = 'BMP180', address = Bmp085Module.DEVICE_ADDR, busnum = 2, mode = Bmp085Module.BMP085_ULTRAHIGHRES)

    while True:
        print('Temp = {0:0.2f} *C'.format(bmp180sensor.read_temperature()))
        print('Pressure = {0:0.2f} Pa'.format(bmp180sensor.read_pressure()))
        print('Altitude = {0:0.2f} m'.format(bmp180sensor.read_altitude()))
        print('Sealevel Pressure = {0:0.2f} Pa'.format(bmp180sensor.read_sealevel_pressure()))
        time.sleep(1)

if __name__=="__main__":
    main()
