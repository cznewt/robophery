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

import ftdi1 as ftdi
from robophery.platform.i2c import I2cInterface


class FT232Interface():

    def __init__(self, *args, **kwargs):
        pass

    def writeRaw8(self, value):
        """Write an 8-bit value on the bus (without register)."""

    def write8(self, register, value):
        """Write an 8-bit value to the specified register."""

    def write16(self, register, value):
        """Write a 16-bit value to the specified register."""

    def writeList(self, register, data):
        """Write bytes to the specified register."""

    def readRaw8(self):
        """Read an 8-bit value on the bus (without register)."""
        return result

    def readU8(self, register):
        """Read an unsigned byte from the specified register."""
        return result

    def readS8(self, register):
        """Read a signed byte from the specified register."""
        return result

    def readU16(self, register, little_endian=True):
        """Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        return result

    def readS16(self, register, little_endian=True):
        """Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first)."""
        return result

    def readList(self, register, length):
        """Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray."""
        return results
