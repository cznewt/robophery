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

from robophery.interface.i2c import I2cInterface


class Ft232hI2cInterface(I2cInterface):

    REPEAT_DELAY = 4

    def __init__(self, *args, **kwargs):
        """
        Create an instance of the I2C device at the specified address on the
        specified I2C bus number.
        """
        super(Ft232hI2cInterface, self).__init__(*args, **kwargs)
#        self._address = address
        self._data = self._manager._interface[kwargs.get('data').get('iface')]
        self._sda1 = int(kwargs.get('data').get('sda1_pin', 0))
        self._sda2 = int(kwargs.get('data').get('sda2_pin', 1))
        self._scl = int(kwargs.get('data').get('scl_pin', 2))
        self._clock_rate = int(kwargs.get('clock_rate', 100000))
        # Enable clock with three phases for I2C.
        self._data.mpsse_set_clock(self._clock_rate, three_phase=True)
        # Enable drive-zero mode to drive outputs low on 0 and tri-state on 1.
        # This matches the protocol for I2C communication so multiple devices
        # can share the I2C bus.
        self._data._write('\x9E\x07\x00')
        self._idle()

    def _idle(self):
        """
        Put the I2C lines into an idle state with SCL and SDA high.
        """
        self._data.setup_pins(
            {0: self._data.OUT, 1: self._data.OUT, 2: self._data.IN},
            {0: self._data.HIGH, 1: self._data.HIGH}
        )

    def _transaction_start(self):
        """
        Start I2C transaction. Clear command buffer and expected response
        bytes.
        """
        self._command = []
        self._expected = 0

    def _transaction_end(self):
        """
        End I2C transaction and get response bytes, including ACKs.
        """
        # Ask to return response bytes immediately.
        self._command.append('\x87')
        # Send the entire command to the MPSSE.
        self._data._write(''.join(self._command))
        # Read response bytes and return them.
        return bytearray(self._data._poll_read(self._expected))

    def _i2c_start(self):
        """
        Send I2C start signal. Must be called within a transaction start/end.
        """
        # Set SCL high and SDA low, repeat 4 times to stay in this state for a
        # short period of time.
        self._data.output_pins(
            {0: self._data.HIGH, 1: self._data.LOW}, write=False)
        self._command.append(self._data.mpsse_gpio() * self.REPEAT_DELAY)
        # Now drop SCL to low (again repeat 4 times for short delay).
        self._data.output_pins(
            {0: self._data.LOW, 1: self._data.LOW}, write=False)
        self._command.append(self._data.mpsse_gpio() * self.REPEAT_DELAY)

    def _i2c_idle(self):
        """Set I2C signals to idle state with SCL and SDA at a high value. Must
        be called within a transaction start/end.
        """
        self._data.output_pins(
            {0: self._data.HIGH, 1: self._data.HIGH}, write=False)
        self._command.append(self._data.mpsse_gpio() * self.REPEAT_DELAY)

    def _i2c_stop(self):
        """
        Send I2C stop signal. Must be called within a transaction start/end.
        """
        # Set SCL low and SDA low for a short period.
        self._data.output_pins(
            {0: self._data.LOW, 1: self._data.LOW}, write=False)
        self._command.append(self._data.mpsse_gpio() * self.REPEAT_DELAY)
        # Set SCL high and SDA low for a short period.
        self._data.output_pins(
            {0: self._data.HIGH, 1: self._data.LOW}, write=False)
        self._command.append(self._data.mpsse_gpio() * self.REPEAT_DELAY)
        # Finally set SCL high and SDA high for a short period.
        self._data.output_pins(
            {0: self._data.HIGH, 1: self._data.HIGH}, write=False)
        self._command.append(self._data.mpsse_gpio() * self.REPEAT_DELAY)

    def _i2c_read_bytes(self, length=1):
        """
        Read the specified number of bytes from the I2C bus. Length is the
        number of bytes to read (must be 1 or more).
        """
        for i in range(length - 1):
            # Read a byte and send ACK.
            self._command.append('\x20\x00\x00\x13\x00\x00')
            # Make sure pins are back in idle state with clock low and data
            # high.
            self._data.output_pins(
                {0: self._data.LOW, 1: self._data.HIGH}, write=False)
            self._command.append(self._data.mpsse_gpio())
        # Read last byte and send NAK.
        self._command.append('\x20\x00\x00\x13\x00\xFF')
        # Make sure pins are back in idle state with clock low and data high.
        self._data.output_pins(
            {0: self._data.LOW, 1: self._data.HIGH}, write=False)
        self._command.append(self._data.mpsse_gpio())
        # Increase expected number of bytes.
        self._expected += length

    def _i2c_write_bytes(self, data):
        """
        Write the specified number of bytes to the chip.
        """
        for byte in data:
            # Write byte.
            self._command.append(str(bytearray((0x11, 0x00, 0x00, byte))))
            # Make sure pins are back in idle state with clock low and data
            # high.
            self._data.output_pins(
                {0: self._data.LOW, 1: self._data.HIGH}, write=False)
            self._command.append(self._data.mpsse_gpio() * self.REPEAT_DELAY)
            # Read bit for ACK/NAK.
            self._command.append('\x22\x00')
        # Increase expected response bytes.
        self._expected += len(data)

    def _address_byte(self, addr, read=True):
        """
        Return the address byte with the specified R/W bit set. If read is
        True the R/W bit will be 1, otherwise the R/W bit will be 0.
        """
        if read:
            return (addr << 1) | 0x01
        else:
            return addr << 1

    def _verify_acks(self, response):
        """
        Check all the specified bytes have the ACK bit set. Throws a
        RuntimeError exception if not all the ACKs are set.
        """
        for byte in response:
            if byte & 0x01 != 0x00:
                raise RuntimeError('Failed to find expected I2C ACK!')

    def ping(self, addr):
        """
        Attempt to detect if a device at this address is present on the I2C
        bus. Will send out the device's address for writing and verify an ACK
        is received. Returns true if the ACK is received, and false if not.
        """
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, False)])
        self._i2c_stop()
        response = self._transaction_end()
        if len(response) != 1:
            raise RuntimeError(
                'Expected 1 response byte but received {0} byte(s).'.format(len(response)))
        return ((response[0] & 0x01) == 0x00)

    def writeRaw8(self, addr, value):
        """
        Write an 8-bit value on the bus (without register).
        """
        value = value & 0xFF
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, False), value])
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response)

    def write8(self, addr, register, value):
        """
        Write an 8-bit value to the specified register.
        """
        value = value & 0xFF
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, False), register, value])
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response)

    def write16(self, addr, register, value, little_endian=True):
        """
        Write a 16-bit value to the specified register.
        """
        value = value & 0xFFFF
        value_low = value & 0xFF
        value_high = (value >> 8) & 0xFF
        if not little_endian:
            value_low, value_high = value_high, value_low
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, False), register, value_low,
                               value_high])
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response)

    def writeList(self, addr, register, data):
        """
        Write bytes to the specified register.
        """
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, False), register] + data)
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response)

    def readList(self, addr, register, length):
        """
        Read a length number of bytes from the specified register.  Results
        will be returned as a bytearray.
        """
        if length <= 0:
            raise ValueError("Length must be at least 1 byte.")
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, True), register])
        self._i2c_stop()
        self._i2c_idle()
        self._i2c_start()
        self._i2c_read_bytes(length)
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response[:-length])
        return response[-length:]

    def readRaw8(self, addr):
        """
        Read an 8-bit value on the bus (without register).
        """
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, False)])
        self._i2c_stop()
        self._i2c_idle()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, True)])
        self._i2c_read_bytes(1)
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response[:-1])
        return response[-1]

    def readU8(self, addr, register):
        """
        Read an unsigned byte from the specified register.
        """
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, False), register])
        self._i2c_stop()
        self._i2c_idle()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, True)])
        self._i2c_read_bytes(1)
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response[:-1])
        return response[-1]

    def readS8(self, addr, register):
        """
        Read a signed byte from the specified register.
        """
        result = self.readU8(addr, register)
        if result > 127:
            result -= 256
        return result

    def readU16(self, addr, register, little_endian=True):
        """
        Read an unsigned 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        self._idle()
        self._transaction_start()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, False), register])
        self._i2c_stop()
        self._i2c_idle()
        self._i2c_start()
        self._i2c_write_bytes([self._address_byte(addr, True)])
        self._i2c_read_bytes(2)
        self._i2c_stop()
        response = self._transaction_end()
        self._verify_acks(response[:-2])
        if little_endian:
            return (response[-1] << 8) | response[-2]
        else:
            return (response[-2] << 8) | response[-1]

    def readS16(self, addr, register, little_endian=True):
        """
        Read a signed 16-bit value from the specified register, with the
        specified endianness (default little endian, or least significant byte
        first).
        """
        result = self.readU16(addr, register, little_endian)
        if result > 32767:
            result -= 65536
        return result

    def readU16LE(self, addr, register):
        """
        Read an unsigned 16-bit value from the specified register, in little
        endian byte order.
        """
        return self.readU16(addr, register, little_endian=True)

    def readU16BE(self, addr, register):
        """
        Read an unsigned 16-bit value from the specified register, in big
        endian byte order.
        """
        return self.readU16(addr, register, little_endian=False)

    def readS16LE(self, addr, register):
        """
        Read a signed 16-bit value from the specified register, in little
        endian byte order.
        """
        return self.readS16(addr, register, little_endian=True)

    def readS16BE(self, addr, register):
        """
        Read a signed 16-bit value from the specified register, in big
        endian byte order.
        """
        return self.readS16(addr, register, little_endian=False)
