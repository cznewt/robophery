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
import atexit
import math
from robophery.interface.gpio import GpioInterface


class Ft232hGpioInterface(GpioInterface):
    """
    Make GPIO constants that match main GPIO class for compatibility.
    """

    FT232H_VID = 0x0403   # Default FTDI FT232H vendor ID
    FT232H_PID = 0x6014   # Default FTDI FT232H product ID

    MSBFIRST = 0
    LSBFIRST = 1

    OUT = 0
    IN = 1
    HIGH = True
    LOW = False

    def __init__(self, *args, **kwargs):
        """
        Create a FT232H object. Will search for the first available FT232H
        device with the specified USB vendor ID and product ID (defaults to
        FT232H default VID & PID). Can also specify an optional serial number
        string to open an explicit FT232H device given its serial number.
        """
        self._serial = kwargs.get('serial', None)
        # Initialize FTDI device connection.
        self._bus = ftdi.new()
        if self._bus == 0:
            raise RuntimeError('ftdi_new failed! Is libftdi1 installed?')
        # Register handler to close and cleanup FTDI context on program exit.
        atexit.register(self.close)
        super(Ft232hGpioInterface, self).__init__(*args, **kwargs)
        if self._serial is None:
            # Open USB connection for specified VID and PID if no serial is
            # specified.
            self._check(ftdi.usb_open, self.FT232H_VID, self.FT232H_PID)
        else:
            # Open USB connection for VID, PID, serial.
            self._check(ftdi.usb_open_string, 's:{0}:{1}:{2}'.format(
                self.FT232H_VID, self.FT232H_PID, self._serial))
        # Reset device.
        self._check(ftdi.usb_reset)
        # Disable flow control. It is unclear if this is necessary.
        # self._check(ftdi.setflowctrl, ftdi.SIO_DISABLE_FLOW_CTRL)
        # Change read & write buffers to maximum size, 65535 bytes.
        self._check(ftdi.read_data_set_chunksize, 65535)
        self._check(ftdi.write_data_set_chunksize, 65535)
        # Clear pending read data & write buffers.
        self._check(ftdi.usb_purge_buffers)
        # Enable MPSSE and syncronize communication with device.
        self._mpsse_enable()
        self._mpsse_sync()
        # Initialize all GPIO as inputs.
        self._write('\x80\x00\x00\x82\x00\x00')
        self._direction = 0x0000
        self._level = 0x0000

    def close(self):
        """
        Close the FTDI device. Will be automatically called when the
        program ends.
        """
        if self._bus is not None:
            ftdi.free(self._bus)
        self._bus = None

    def _write(self, string):
        """
        Helper function to call write_data on the provided FTDI device and
        verify it succeeds.
        """
        # Get modem status. Useful to enable for debugging.
        # ret, status = ftdi.poll_modem_status(self._bus)
        # if ret == 0:
        #   logger.debug('Modem status {0:02X}'.format(status))
        # else:
        #   logger.debug('Modem status error {0}'.format(ret))
        length = len(string)
        ret = ftdi.write_data(self._bus, string, length)
        # Log the string that was written in a python hex string format using
        # a very ugly one-liner list comprehension for brevity.
        # logger.debug('Wrote {0}'.format(''.join(['\\x{0:02X}'.format(ord(x)) for x in string])))
        if ret < 0:
            raise RuntimeError('ftdi_write_data failed with error {0}: {1}'.format(
                ret, ftdi.get_error_string(self._bus)))
        if ret != length:
            raise RuntimeError(
                'ftdi_write_data expected to write {0} bytes but actually wrote {1}!'.format(length, ret))

    def _check(self, command, *args):
        """
        Helper function to call the provided command on the FTDI device and
        verify the response matches the expected value.
        """
        ret = command(self._bus, *args)
        self._log.debug('Called ftdi_{0} and got response {1}.'.format(
            command.__name__, ret))
        if ret != 0:
            raise RuntimeError('ftdi_{0} failed with error {1}: {2}'.format(
                command.__name__, ret, ftdi.get_error_string(self._bus)))

    def _poll_read(self, expected, timeout_s=5.0):
        """
        Helper function to continuously poll reads on the FTDI device until an
        expected number of bytes are returned. Will throw a timeout error if
        no data is received within the specified number of timeout seconds.
        Returns the read data as a string if successful, otherwise raises an
        execption.
        """
        start = self._get_time()
        # Start with an empty response buffer.
        response = bytearray(expected)
        index = 0
        # Loop calling read until the response buffer is full or a timeout
        # occurs.
        while self._get_time() - start <= timeout_s:
            ret, data = ftdi.read_data(self._bus, expected - index)
            # Fail if there was an error reading data.
            if ret < 0:
                raise RuntimeError(
                    'ftdi_read_data failed with error code {0}.'.format(ret))
            # Add returned data to the buffer.
            response[index:index + ret] = data[:ret]
            index += ret
            # Buffer is full, return the result data.
            if index >= expected:
                return str(response)
            self._msleep(10)
        raise RuntimeError(
            'Timeout while polling ftdi_read_data for {0} bytes!'.format(expected))

    def _mpsse_enable(self):
        """
        Enable MPSSE mode on the FTDI device.
        """
        # Reset MPSSE by sending mask = 0 and mode = 0
        self._check(ftdi.set_bitmode, 0, 0)
        # Enable MPSSE by sending mask = 0 and mode = 2
        self._check(ftdi.set_bitmode, 0, 2)

    def _mpsse_sync(self, max_retries=10):
        """
        Synchronize buffers with MPSSE by sending bad opcode and reading
        expected error response. Should be called once after enabling MPSSE.
        """
        # Send a bad/unknown command (0xAB), then read buffer until bad command
        # response is found.
        self._write('\xAB')
        # Keep reading until bad command response (0xFA 0xAB) is returned.
        # Fail if too many read attempts are made to prevent sticking in a
        # loop.
        tries = 0
        sync = False
        while not sync:
            data = self._poll_read(2)
            if data == '\xFA\xAB':
                sync = True
            tries += 1
            if tries >= max_retries:
                raise RuntimeError('Could not synchronize with FT232H!')

    def mpsse_set_clock(self, clock_hz, adaptive=False, three_phase=False):
        """
        Set the clock speed of the MPSSE engine. Can be any value from 450hz
        to 30mhz and will pick that speed or the closest speed below it.
        """
        # Disable clock divisor by 5 to enable faster speeds on FT232H.
        self._write('\x8A')
        # Turn on/off adaptive clocking.
        if adaptive:
            self._write('\x96')
        else:
            self._write('\x97')
        # Turn on/off three phase clock (needed for I2C).
        # Also adjust the frequency for three-phase clocking as specified in section 2.2.4
        # of this document:
        #   http://www.ftdichip.com/Support/Documents/AppNotes/AN_255_USB%20to%20I2C%20Example%20using%20the%20FT232H%20and%20FT201X%20devices.pdf
        if three_phase:
            self._write('\x8C')
        else:
            self._write('\x8D')
        # Compute divisor for requested clock.
        # Use equation from section 3.8.1 of:
        #  http://www.ftdichip.com/Support/Documents/AppNotes/AN_108_Command_Processor_for_MPSSE_and_MCU_Host_Bus_Emulation_Modes.pdf
        # Note equation is using 60mhz master clock instead of 12mhz.
        divisor = int(
            math.ceil((30000000.0 - float(clock_hz)) / float(clock_hz))) & 0xFFFF
        if three_phase:
            divisor = int(divisor * (2.0 / 3.0))
        self._log.debug(
            'Setting clockspeed with divisor value {0}'.format(divisor))
        # Send command to set divisor from low and high byte values.
        self._write(
            str(bytearray((0x86, divisor & 0xFF, (divisor >> 8) & 0xFF))))

    def mpsse_read_gpio(self):
        """
        Read both GPIO bus states and return a 16 bit value with their state.
        D0-D7 are the lower 8 bits and C0-C7 are the upper 8 bits.
        """
        # Send command to read low byte and high byte.
        self._write('\x81\x83')
        # Wait for 2 byte response.
        data = self._poll_read(2)
        # Assemble response into 16 bit value.
        low_byte = ord(data[0])
        high_byte = ord(data[1])
        self._log.debug('Read MPSSE GPIO low byte = {0:02X} and high byte = {1:02X}'.format(
            low_byte, high_byte))
        return (high_byte << 8) | low_byte

    def mpsse_gpio(self):
        """
        Return command to update the MPSSE GPIO state to the current direction
        and level.
        """
        level_low = chr(self._level & 0xFF)
        level_high = chr((self._level >> 8) & 0xFF)
        dir_low = chr(self._direction & 0xFF)
        dir_high = chr((self._direction >> 8) & 0xFF)
        return str(bytearray((0x80, level_low, dir_low, 0x82, level_high, dir_high)))

    def mpsse_write_gpio(self):
        """
        Write the current MPSSE GPIO state to the FT232H chip.
        """
        self._write(self.mpsse_gpio())

    def _setup_pin(self, pin, mode):
        if pin < 0 or pin > 15:
            raise ValueError('Pin must be between 0 and 15 (inclusive).')
        if mode not in (self.IN, self.OUT):
            raise ValueError('Mode must be GPIO.IN or GPIO.OUT.')
        if mode == self.IN:
            # Set the direction and level of the pin to 0.
            self._direction &= ~(1 << pin) & 0xFFFF
            self._level &= ~(1 << pin) & 0xFFFF
        else:
            # Set the direction of the pin to 1.
            self._direction |= (1 << pin) & 0xFFFF
        self._use_pin(pin)

    def setup_pin(self, pin, mode):
        """
        Set the input or output mode for a specified pin. Mode should be
        either OUT or IN.
        """
        self._setup_pin(pin, mode)
        self.mpsse_write_gpio()

    def setup_pins(self, pins, values={}, write=True):
        """
        Setup multiple pins as inputs or outputs at once.  Pins should be a
        dict of pin name to pin mode (IN or OUT).  Optional starting values of
        pins can be provided in the values dict (with pin name to pin value).
        """
        for pin, mode in iter(pins.items()):
            self._setup_pin(pin, mode)
        for pin, value in iter(values.items()):
            self._output_pin(pin, value)
        if write:
            self.mpsse_write_gpio()

    def _output_pin(self, pin, value):
        if value:
            self._level |= (1 << pin) & 0xFFFF
        else:
            self._level &= ~(1 << pin) & 0xFFFF

    def output(self, pin, value):
        """
        Set the specified pin the provided high/low value. Value should be
        either HIGH/LOW or a boolean (true = high).
        """
        if pin < 0 or pin > 15:
            raise ValueError('Pin must be between 0 and 15 (inclusive).')
        self._output_pin(pin, value)
        self.mpsse_write_gpio()

    def output_pins(self, pins, write=True):
        """
        Set multiple pins high or low at once. Pins should be a dict of pin
        name to pin value (HIGH/True for 1, LOW/False for 0). All provided pins
        will be set to the given values.
        """
        for pin, value in iter(pins.items()):
            self._output_pin(pin, value)
        if write:
            self.mpsse_write_gpio()

    def input(self, pin):
        """
        Read the specified pin and return HIGH/true if the pin is pulled high,
        or LOW/false if pulled low.
        """
        return self.input_pins([pin])[0]

    def input_pins(self, pins):
        """
        Read multiple pins specified in the given list and return list of pin values
        GPIO.HIGH/True if the pin is pulled high, or GPIO.LOW/False if pulled low.
        """
        if [pin for pin in pins if pin < 0 or pin > 15]:
            raise ValueError('Pin must be between 0 and 15 (inclusive).')
        _pins = self.mpsse_read_gpio()
        return [((_pins >> pin) & 0x0001) == 1 for pin in pins]
