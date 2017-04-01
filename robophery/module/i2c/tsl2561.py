# Copyright 2014 IIJ Innovation Institute Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY IIJ INNOVATION INSTITUTE INC. ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL IIJ INNOVATION INSTITUTE INC. OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Copyright 2014 Keiichi Shima. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import time
from robophery.interface.i2c import I2cModule


class Tsl2561Module(I2cModule):
    """
    Module for TSL2561 based light-to-digital convertor.
    """
    DEVICE_NAME = 'tsl2561'
    # TSL2561 default address
    DEVICE_ADDR = 0x39

    # Commands
    CMD = 0x80
    CMD_CLEAR = 0x40
    CMD_WORD = 0x20
    CMD_BLOCK = 0x10

    # Registers
    REG_CONTROL = 0x00
    REG_TIMING = 0x01
    REG_ID = 0x0A
    REG_BLOCKREAD = 0x0B
    REG_DATA0 = 0x0C
    REG_DATA1 = 0x0E

    # Control parameters
    POWER_UP = 0x03
    POWER_DOWN = 0x00

    # Timing parameters
    GAIN_LOW = 0b00000000
    GAIN_HIGH = 0b00010000
    INTEGRATION_START = 0b00001000
    INTEGRATION_STOP = 0b00000000
    INTEGRATE_13 = 0b00000000
    INTEGRATE_101 = 0b00000001
    INTEGRATE_402 = 0b00000010
    INTEGRATE_DEFAULT = 0b00000010  # INTEGRATE_402
    INTEGRATE_NA = 0b00000011

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', self.DEVICE_ADDR)
        super(Tsl2561Module, self).__init__(*args, **kwargs)

        self._gain = self.GAIN_LOW
        self._manual = self.INTEGRATION_STOP
        self._integ = self.INTEGRATE_DEFAULT

        self._channel0 = None
        self._channel1 = None

        self._control(self.POWER_UP)
        self._reconfigure()

    def _control(self, params):
        cmd = self.CMD | self.REG_CONTROL
        self._bus.write_byte_data(cmd, params)

        # Wait for 400ms to be power up.
        time.sleep(0.4)

    def _reconfigure(self):
        cmd = self.CMD | self.REG_TIMING
        timing = (self._gain | self._manual | self._integ)
        self._bus.write_byte_data(cmd, timing)

        # Wait for 400ms to complete initial A/D conversion.
        time.sleep(0.4)

    def read_luminosity(self):
        cmd = self.CMD | self.CMD_WORD | self.REG_DATA0
        vals = self.read_i2c_block_data(cmd, 2)
        self._channel0 = vals[1] << 8 | vals[0]

        cmd = self.CMD | self.CMD_WORD | self.REG_DATA1
        vals = self.read_i2c_block_data(cmd, 2)
        self._channel1 = vals[1] << 8 | vals[0]

        # If either sensor is satulated, no acculate lux value
        # can be achieved.
        if (self._channel0 == 0xffff or self._channel1 == 0xffff):
            lux = None
            return lux

        # The following lux value calculation code is taken from
        # the SparkFun's example code.
        #
        # https://github.com/sparkfun/
        #         TSL2561_Luminosity_Sensor_BOB/blob/master/
        #         Libraries/SFE_TSL2561/SFE_TSL2561.cpp
        d0 = float(self._channel0)
        d1 = float(self._channel1)
        if (d0 == 0):
            # Sometimes, the channel0 returns 0 when dark...
            lux = 0.0
            return lux
        ratio = d1 / d0

        integ_scale = 1
        if (self._integ == self.INTEGRATE_13):
            integ_scale = 402.0 / 13.7
        elif (self._integ == self.INTEGRATE_101):
            integ_scale = 402.0 / 101.0
        elif (self._integ == self.INTEGRATE_NA):
            integ_scale = 402.0 / self._integration_time
        d0 = d0 * integ_scale
        d1 = d1 * integ_scale

        if (self._gain == self.GAIN_HIGH):
            d0 = d0 / 16
            d1 = d1 / 16

        if (ratio < 0.5):
            return 0.0304 * d0 - 0.062 * d0 * (ratio ** 1.4)
        elif (ratio < 0.61):
            return 0.0224 * d0 - 0.031 * d1
        elif (ratio < 0.80):
            return 0.0128 * d0 - 0.0153 * d1
        elif (ratio < 1.30):
            return 0.00146 * d0 - 0.00112 * d1
        else:
            return 0.0

    def read_data(self):
        """
        Get all sensor readings.
        """
        lumin_time_start = time.time()
        lumin = self.read_luminosity()
        lumin_time_stop = time.time()
        lumin_time_delta = lumin_time_stop - lumin_time_start

        data = [
            (self._name, 'luminosity', lumin, lumin_time_delta),
        ]
        self._log_data(data)
        return data
