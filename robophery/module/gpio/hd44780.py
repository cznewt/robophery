# -*- coding: UTF-8 -*-
# Copyright (C) 2013-2016 Danilo Bargen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from __future__ import print_function, division, absolute_import, unicode_literals
import time
from enum import Enum
from robophery.module.gpio.base import GpioModule


# Flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00


alignment = {
    'left': LCD_ENTRYLEFT,
    'right': LCD_ENTRYRIGHT
}

shiftMode = {
    "cursor": LCD_ENTRYSHIFTDECREMENT,
    "display": LCD_ENTRYSHIFTINCREMENT
}

cursorMode = {
    "hide": LCD_CURSOROFF | LCD_BLINKOFF,
    "line": LCD_CURSORON | LCD_BLINKOFF,
    "blink": LCD_CURSOROFF | LCD_BLINKON
}

backlightMode = {
    "active_high": 1,
    "active_low": 2
}


class Hd44780Module(GpioModule):
    """
    Module for Character LCD controller with HD44780 chip.
    """
    DEVICE_NAME = 'gpio-hd44780'

    # Commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # Flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # Flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # Flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00

    # Flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # Flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    # Flags for backlight control
    LCD_BACKLIGHT = 0x08
    LCD_NOBACKLIGHT = 0x00

    # Flags for RS pin modes
    RS_INSTRUCTION = 0x00
    RS_DATA = 0x01

    # Pin bitmasks
    PIN_ENABLE = 0x4
    PIN_READ_WRITE = 0x2
    PIN_REGISTER_SELECT = 0x1

    def __init__(self, *args, **kwargs):
        self._bus_mode = self.LCD_4BITMODE
        self._dot_size = 8
        self._cols = kwargs.get('cols', 20)
        self._rows = kwargs.get('rows', 4)
        self._auto_linebreaks = kwargs.get('auto_linebreaks', True)
        self._recent_auto_linebreak = False
        self._backlight_enabled = kwargs.get('backlight_enabled', True)
        self._backlight = self.LCD_BACKLIGHT if self._backlight_enabled else self.LCD_NOBACKLIGHT
        self._rs_pin = self._normalize_pin(kwargs.get('rs_pin'))
        self._rw_pin = self._normalize_pin(kwargs.get('rw_pin'))
        self._en_pin = self._normalize_pin(kwargs.get('en_pin'))
        self._bl_pin = self._normalize_pin(kwargs.get('bl_pin'))
        self._d4_pin = self._normalize_pin(kwargs.get('d4_pin'))
        self._d5_pin = self._normalize_pin(kwargs.get('d5_pin'))
        self._d6_pin = self._normalize_pin(kwargs.get('d6_pin'))
        self._d7_pin = self._normalize_pin(kwargs.get('d7_pin'))
        super(Hd44780Module, self).__init__(*args, **kwargs)

        # Setup initial display configuration
        displayfunction = self._bus_mode | self.LCD_5x8DOTS
        if self._rows == 1:
            displayfunction |= self.LCD_1LINE
        elif self._rows in [2, 4]:
            # LCD only uses two lines on 4 row displays
            displayfunction |= self.LCD_2LINE
        if self._dot_size == 10:
            # For some 1 line displays you can select a 10px font.
            displayfunction |= self.LCD_5x10DOTS

        # Create content cache
        self._content = [[0x20] * self._cols for _ in range(self._rows)]

        # Choose 4 or 8 bit mode
        if self._bus_mode == self.LCD_4BITMODE:
            # Hitachi manual page 46
            self.command(0x03)
            self._msleep(4.5)
            self.command(0x03)
            self._msleep(4.5)
            self.command(0x03)
            self._usleep(100)
            self.command(0x02)
        elif self._bus_mode == self.LCD_8BITMODE:
            # Hitachi manual page 45
            self.command(0x30)
            self._msleep(4.5)
            self.command(0x30)
            self._usleep(100)
            self.command(0x30)
        else:
            raise ValueError('Invalid bus mode: {}'.format(self._bus_mode))

        # Write configuration to display
        self.command(self.LCD_FUNCTIONSET | displayfunction)
        self._usleep(50)

        # Configure display mode
        self._display_mode = self.LCD_DISPLAYON
        self._cursor_mode = int(self.LCD_CURSOROFF | self.LCD_BLINKOFF)
        self.command(self.LCD_DISPLAYCONTROL | self._display_mode | self._cursor_mode)
        self._usleep(50)

        # Clear display
        self.clear()

        # Configure entry mode
        self._text_align_mode = int(self.LCD_ENTRYLEFT)
        self._display_shift_mode = int(self.LCD_ENTRYSHIFTDECREMENT)
        self._cursor_pos = (0, 0)
        self.command(self.LCD_ENTRYMODESET | self._text_align_mode | self._display_shift_mode)
        self._usleep(50)


    def __str__(self):
        return "{0} (connected to {1}, RS pin {2}, size {3}x{4})".format(self._base_name(), self._interface._name, self._rs_pin, self._cols, self._rows)


    def close(self, clear=False):
        if clear:
            self.clear()
        self._close_connection()


    def _get_cursor_pos(self):
        return self._cursor_pos


    def _set_cursor_pos(self, value):
        if not hasattr(value, '__getitem__') or len(value) != 2:
            raise ValueError('Cursor position should be determined by a 2-tuple.')
        if value[0] not in range(self._rows) or value[1] not in range(self._cols):
            msg = 'Cursor position {pos!r} invalid on a {lcd._rows}x{lcd._cols} LCD.'
            raise ValueError(msg.format(pos=value, lcd=self))
        row_offsets = [0x00, 0x40, self._cols, 0x40 + self._cols]
        self._cursor_pos = value
        self.command(self.LCD_SETDDRAMADDR | row_offsets[value[0]] + value[1])
        self._usleep(50)


    cursor_pos = property(_get_cursor_pos, _set_cursor_pos,
        doc='The cursor position as a 2-tuple (row, col).')


    def _get_text_align_mode(self):
        self._text_align_mode


    def _set_text_align_mode(self, value):
        self._text_align_mode = int(value)
        self.command(self.LCD_ENTRYMODESET | self._text_align_mode | self._display_shift_mode)
        self._usleep(50)


    text_align_mode = property(_get_text_align_mode, _set_text_align_mode,
        doc='The text alignment (``Alignment.left`` or ``Alignment.right``).')


    def _get_write_shift_mode(self):
        try:
            return shiftMode[self._display_shift_mode]
        except ValueError:
            raise ValueError('Internal _display_shift_mode has invalid value.')

    def _set_write_shift_mode(self, value):
        if value not in ShiftMode:
            raise ValueError('Write shift mode must be of ``ShiftMode`` type.')
        self._display_shift_mode = int(value)
        self.command(self.LCD_ENTRYMODESET | self._text_align_mode | self._display_shift_mode)
        self._usleep(50)


    write_shift_mode = property(_get_write_shift_mode, _set_write_shift_mode,
        doc='The shift mode when writing (``ShiftMode.cursor`` or ``ShiftMode.display``).')


    def _get_display_enabled(self):
        return self._display_mode == self.LCD_DISPLAYON


    def _set_display_enabled(self, value):
        self._display_mode = self.LCD_DISPLAYON if value else self.LCD_DISPLAYOFF
        self.command(self.LCD_DISPLAYCONTROL | self._display_mode | self._cursor_mode)
        self._usleep(50)


    display_enabled = property(_get_display_enabled, _set_display_enabled,
        doc='Whether or not to display any characters.')


    def _get_cursor_mode(self):
        try:
            return cursorMode[self._cursor_mode]
        except ValueError:
            raise ValueError('Internal _cursor_mode has invalid value.')


    def _set_cursor_mode(self, value):
        self._cursor_mode = int(value)
        self.command(self.LCD_DISPLAYCONTROL | self._display_mode | self._cursor_mode)
        self._usleep(50)


    cursor_mode = property(_get_cursor_mode, _set_cursor_mode,
            doc='How the cursor should behave (``CursorMode.hide``, ' +
                                   '``CursorMode.line`` or ``CursorMode.blink``).')


    def _get_backlight_enabled(self):
        return self._backlight == LCD_BACKLIGHT


    def _set_backlight_enabled(self, value):
        self._backlight = LCD_BACKLIGHT if value else LCD_NOBACKLIGHT
        self.bus.write_byte(self.address, self._backlight)

    backlight_enabled = property(_get_backlight_enabled, _set_backlight_enabled,
        doc='Whether or not to enable the backlight. Either ``True`` or ``False``.')


    # High level commands

    def write_string(self, value):
        """
        Write the specified unicode string to the display.
        To control multiline behavior, use newline (``\\n``) and carriage
        return (``\\r``) characters.
        Lines that are too long automatically continue on next line, as long as
        ``auto_linebreaks`` has not been disabled.
        Make sure that you're only passing unicode objects to this function. If
        you're dealing with bytestrings (the default string type in Python 2),
        convert it to a unicode object using the ``.decode(encoding)`` method
        and the appropriate encoding. Example for UTF-8 encoded strings:
        .. code::
            >>> bstring = 'Temperature: 30°C'
            >>> bstring
            'Temperature: 30\xc2\xb0C'
            >>> bstring.decode('utf-8')
            u'Temperature: 30\xb0C'
        Only characters with an ``ord()`` value between 0 and 255 are currently
        supported.
        """
        ignored = None  # Used for ignoring manual linebreaks after auto linebreaks
        for char in value:
            # Write regular chars
            if char not in '\n\r':
                self.write(ord(char))
                ignored = None
                continue
            # If an auto linebreak happened recently, ignore this write.
            if self._recent_auto_linebreak is True:
                # No newline chars have been ignored yet. Do it this time.
                if ignored is None:
                    ignored = char
                    continue
                # A newline character has been ignored recently. If the current
                # character is different, ignore it again. Otherwise, reset the
                # ignored character tracking.
                if ignored != char:  # A carriage return and a newline
                    ignored = None  # Reset ignore list
                    continue
            # Handle newlines and carriage returns
            row, col = self.cursor_pos
            if char == '\n':
                if row < self._rows - 1:
                    self.cursor_pos = (row + 1, col)
                else:
                    self.cursor_pos = (0, col)
            elif char == '\r':
                if self.text_align_mode is self.LCD_ENTRYLEFT:
                    self.cursor_pos = (row, 0)
                else:
                    self.cursor_pos = (row, self._cols - 1)

    def clear(self):
        """
        Overwrite display with blank characters and reset cursor position.
        """
        self.command(self.LCD_CLEARDISPLAY)
        self._cursor_pos = (0, 0)
        self._content = [[0x20] * self._cols for _ in range(self._rows)]
        self._msleep(2)


    def home(self):
        """
        Set cursor to initial position and reset any shifting.
        """
        self.command(self.LCD_RETURNHOME)
        self._cursor_pos = (0, 0)
        self._msleep(2)


    def shift_display(self, amount):
        """
        Shift the display. Use negative amounts to shift left and positive
        amounts to shift right.
        """
        if amount == 0:
            return
        direction = self.LCD_MOVERIGHT if amount > 0 else self.LCD_MOVELEFT
        for i in range(abs(amount)):
            self.command(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | direction)
            self._usleep(50)

    def create_char(self, location, bitmap):
        """
        Create a new character.
        The HD44780 supports up to 8 custom characters (location 0-7).
        :param location: The place in memory where the character is stored.
            Values need to be integers between 0 and 7.
        :type location: int
        :param bitmap: The bitmap containing the character. This should be a
            tuple of 8 numbers, each representing a 5 pixel row.
        :type bitmap: tuple of int
        :raises AssertionError: Raised when an invalid location is passed in or
            when bitmap has an incorrect size.
        Example:
        .. sourcecode:: python
            >>> smiley = (
            ...     0b00000,
            ...     0b01010,
            ...     0b01010,
            ...     0b00000,
            ...     0b10001,
            ...     0b10001,
            ...     0b01110,
            ...     0b00000,
            ... )
            >>> lcd.create_char(0, smiley)
        """
        assert 0 <= location <= 7, 'Only locations 0-7 are valid.'
        assert len(bitmap) == 8, 'Bitmap should have exactly 8 rows.'

        # Store previous position
        pos = self.cursor_pos

        # Write character to CGRAM
        self.command(self.LCD_SETCGRAMADDR | location << 3)
        for row in bitmap:
            self._send(row, self.RS_DATA)

        # Restore cursor pos
        self.cursor_pos = pos

    # Mid level commands


    def command(self, value):
        """
        Send a raw command to the LCD.
        """
        self._send(value, self.RS_INSTRUCTION)


    def write(self, value):
        """
        Write a raw byte to the LCD.
        """

        # Get current position
        row, col = self._cursor_pos

        # Write byte if changed
        if self._content[row][col] != value:
            self._send(value, self.RS_DATA)
            # Update content cache
            self._content[row][col] = value
            unchanged = False
        else:
            unchanged = True

        # Update cursor position.
        if self.text_align_mode is self.LCD_ENTRYLEFT:
            if self._auto_linebreaks is False or col < self._cols - 1:
                # No newline, update internal pointer
                newpos = (row, col + 1)
                if unchanged:
                    self.cursor_pos = newpos
                else:
                    self._cursor_pos = newpos
                self._recent_auto_linebreak = False
            else:
                # Newline, reset pointer
                if row < self._rows - 1:
                    self.cursor_pos = (row + 1, 0)
                else:
                    self.cursor_pos = (0, 0)
                self._recent_auto_linebreak = True
        else:
            if self._auto_linebreaks is False or col > 0:
                # No newline, update internal pointer
                newpos = (row, col - 1)
                if unchanged:
                    self.cursor_pos = newpos
                else:
                    self._cursor_pos = newpos
                self._recent_auto_linebreak = False
            else:
                # Newline, reset pointer
                if row < self._rows - 1:
                    self.cursor_pos = (row + 1, self._cols - 1)
                else:
                    self.cursor_pos = (0, self._cols - 1)
                self._recent_auto_linebreak = True


    # Low level commands

    def _send(self, value, mode):
        """Send the specified value to the display with automatic 4bit / 8bit
        selection. The rs_mode is either ``RS_DATA`` or ``RS_INSTRUCTION``."""

        # Choose instruction or data mode
        self.output(self._rs_pin, mode)

        # If the RW pin is used, set it to low in order to write.
        if self._rw_pin is not None:
            self.output(self._rw_pin, 0)

        # Write data out in chunks of 4 or 8 bit
        if self._bus_mode == self.LCD_8BITMODE:
            self._write8bits(value)
        else:
            self._write4bits(value >> 4)
            self._write4bits(value)


    def _data_pins(self):
        if self._bus_mode == self.LCD_8BITMODE:
            return [
                self._d0_pin,
                self._d1_pin,
                self._d2_pin,
                self._d3_pin,
                self._d4_pin,
                self._d5_pin,
                self._d6_pin,
                self._d7_pin
            ]
        else:
            return [
                self._d4_pin,
                self._d5_pin,
                self._d6_pin,
                self._d7_pin
            ]


    def _write4bits(self, value):
        """
        Write 4 bits of data into the data bus.
        """
        for i in range(4):
            bit = (value >> i) & 0x01
            self.output(self._data_pins()[i], bit)
        self._pulse_enable()


    def _write8bits(self, value):
        """
        Write 8 bits of data into the data bus.
        """
        for i in range(8):
            bit = (value >> i) & 0x01
            self.output(self._data_pins()[i], bit)
        self._pulse_enable()


    def _pulse_enable(self):
        """
        Pulse the `enable` flag to process data.
        """
        self.set_low(self._en_pin)
        self._usleep(1)
        self.set_high(self._en_pin)
        self._usleep(1)
        self.set_low(self._en_pin)
        # commands need > 37us to settle
        self._usleep(100)


    def read_data(self):
        """
        LCD status readings.
        """
        self.write_string('dfdsfewfwef')
        if self._backlight_enabled:
            backlight = 1
        else:
            backlight = 0
        return [
            (self._name, 'backlight', backlight, 0),
        ]


    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'backlight': {
                'type': 'counter',
                'unit': '',
                'range_low': 0,
                'range_high': 1,
            }
        }
