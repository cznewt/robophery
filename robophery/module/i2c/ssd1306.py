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

from robophery.interface.i2c import I2cModule

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Constants
SSD1306_I2C_ADDRESS = 0x3C    # 011110+SA0+RW - 0x3C or 0x3D
SSD1306_SETCONTRAST = 0x81
SSD1306_DISPLAYALLON_RESUME = 0xA4
SSD1306_DISPLAYALLON = 0xA5
SSD1306_NORMALDISPLAY = 0xA6
SSD1306_INVERTDISPLAY = 0xA7
SSD1306_DISPLAYOFF = 0xAE
SSD1306_DISPLAYON = 0xAF
SSD1306_SETDISPLAYOFFSET = 0xD3
SSD1306_SETCOMPINS = 0xDA
SSD1306_SETVCOMDETECT = 0xDB
SSD1306_SETDISPLAYCLOCKDIV = 0xD5
SSD1306_SETPRECHARGE = 0xD9
SSD1306_SETMULTIPLEX = 0xA8
SSD1306_SETLOWCOLUMN = 0x00
SSD1306_SETHIGHCOLUMN = 0x10
SSD1306_SETSTARTLINE = 0x40
SSD1306_MEMORYMODE = 0x20
SSD1306_COLUMNADDR = 0x21
SSD1306_PAGEADDR = 0x22
SSD1306_COMSCANINC = 0xC0
SSD1306_COMSCANDEC = 0xC8
SSD1306_SEGREMAP = 0xA0
SSD1306_CHARGEPUMP = 0x8D
SSD1306_EXTERNALVCC = 0x1
SSD1306_SWITCHCAPVCC = 0x2

# Scrolling constants
SSD1306_ACTIVATE_SCROLL = 0x2F
SSD1306_DEACTIVATE_SCROLL = 0x2E
SSD1306_SET_VERTICAL_SCROLL_AREA = 0xA3
SSD1306_RIGHT_HORIZONTAL_SCROLL = 0x26
SSD1306_LEFT_HORIZONTAL_SCROLL = 0x27
SSD1306_VERTICAL_AND_RIGHT_HORIZONTAL_SCROLL = 0x29
SSD1306_VERTICAL_AND_LEFT_HORIZONTAL_SCROLL = 0x2A


class Ssd1306Module(I2cModule):
    """
    Base class for SSD1306-based OLED displays. Implementors should subclass
    and provide an implementation for the _initialize function.
    """
    DEVICE_NAME = 'ssd1306'

    def __init__(self, *args, **kwargs):
        self._addr = kwargs.get('addr', SSD1306_I2C_ADDRESS)
        self._contrast = kwargs.get('contrast', 255)
        self._reset_pin = kwargs.get('reset_pin').get('pin', None)
        super(Ssd1306Module, self).__init__(*args, **kwargs)
        width = kwargs.get('width', 128)
        height = kwargs.get('height', 32)
        self._width = width
        self._height = height
        self._pages = height // 8
        self._buffer = [0] * (width * self._pages)
        # Default to platform GPIO if not provided.
        if self._reset_pin is not None:
            self._gpio_interface = self._manager._interface[kwargs['reset_pin']['interface']]
            self._gpio_interface.setup_pin(self._reset_pin, self._gpio_interface.GPIO_MODE_OUT)
        self.begin()

        # Clear display.
        self.clear()
        self.display()
        self.set_contrast(self._contrast)

        self.write_text('hello world')

    def command(self, c):
        """
        Send command byte to display.
        """
        control = 0x00   # Co = 0, DC = 0
        self.write8(control, c)

    def begin(self, vccstate=SSD1306_SWITCHCAPVCC):
        """
        Initialize display.
        """
        # Save vcc state.
        self._vccstate = vccstate
        # Reset and initialize display.
        if self._reset_pin is not None:
            self.reset()
        if (self._width == 128 and self._height == 64):
            self._init_128_64()
        elif (self._width == 128 and self._height == 32):
            self._init_128_32()
        elif (self._width == 96 and self._height == 16):
            self._init_96_16()
        else:
            raise ValueError('{0}x{1} display dimensions are unknown.'
                             .format(self._width, self._height))
        # Turn on the display.
        self.command(SSD1306_DISPLAYON)

    def commit_action(self, action, arg=None):
        self._log.debug('Received action {0} with args {1})'.format(
            action, arg))
        if action == 'get_data':
            return self.read_data()
        elif action == 'clear':
            self.clear()
            self.display()
            return self.read_data()
        elif action == 'set_contrast':
            self.set_contrast(arg[0])
            return self.read_data()
        elif action == 'write_text':
            self.write_text(arg[0])
            return self.read_data()

    def reset(self):
        """
        Reset the display.
        """
        # Set reset high for a millisecond.
        self._gpio_interface.set_high(self._reset_pin)
        self._msleep(1)
        # Set reset low for 10 milliseconds.
        self._gpio_interface.set_low(self._reset_pin)
        self._msleep(10)
        # Set reset high again.
        self._gpio_interface.set_high(self._reset_pin)

    def display(self):
        """
        Write display buffer to physical display.
        """
        self.command(SSD1306_COLUMNADDR)
        self.command(0)              # Column start address. (0 = reset)
        self.command(self._width - 1)   # Column end address.
        self.command(SSD1306_PAGEADDR)
        self.command(0)              # Page start address. (0 = reset)
        self.command(self._pages - 1)  # Page end address.
        # Write buffer data.
        for i in range(0, len(self._buffer), 16):
            control = 0x40   # Co = 0, DC = 0
            self.writeList(control, self._buffer[i:i + 16])

    def image(self, image):
        """
        Set buffer to value of Python Imaging Library image. The image should
        be in 1 bit mode and a size equal to the display size.
        """
        if image.mode != '1':
            raise ValueError('Image must be in mode 1.')
        imwidth, imheight = image.size
        if imwidth != self._width or imheight != self._height:
            raise ValueError('Image must have {0}x{1} dimensions.'
                             .format(self._width, self._height))
        # Grab all the pixels from the image, faster than getpixel.
        pix = image.load()
        # Iterate through the memory pages
        index = 0
        for page in range(self._pages):
            # Iterate through all x axis columns.
            for x in range(self._width):
                # Set the bits for the column of pixels at the current
                # position.
                bits = 0
                # Don't use range here as it's a bit slow
                for bit in [0, 1, 2, 3, 4, 5, 6, 7]:
                    bits = bits << 1
                    bits |= 0 if pix[(x, page * 8 + 7 - bit)] == 0 else 1
                # Update buffer byte and increment to next byte.
                self._buffer[index] = bits
                index += 1

    def clear(self):
        """Clear contents of image buffer."""
        self._buffer = [0] * (self._width * self._pages)

    def set_contrast(self, contrast):
        """
        Sets the contrast of the display. Contrast should be a value between
        0 and 255.
        """
        if contrast < 0 or contrast > 255:
            raise ValueError(
                'Contrast must be a value from 0 to 255 (inclusive).')
        self._contrast = contrast
        self.command(SSD1306_SETCONTRAST)
        self.command(contrast)

    def dim(self, dim):
        """
        Adjusts contrast to dim the display if dim is True, otherwise sets the
        contrast to normal brightness if dim is False.
        """
        # Assume dim display.
        contrast = 0
        # Adjust contrast based on VCC if not dimming.
        if not dim:
            if self._vccstate == SSD1306_EXTERNALVCC:
                contrast = 0x9F
            else:
                contrast = 0xCF
        self.set_contrast(contrast)

    def write_text(self, text):
        image = Image.new('1', (self._width, self._height))
        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)
        # Draw a black filled box to clear the image.
        draw.rectangle((0, 0, self._width, self._height), outline=0, fill=0)

        font = ImageFont.load_default()
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        x = 0

        draw.text((x, top), str(text), font=font, fill=255)
        draw.text((x, top + 8), str(text), font=font, fill=255)
        draw.text((x, top + 16), str(text), font=font, fill=255)
        draw.text((x, top + 25), str(text), font=font, fill=255)

        # Display image.
        self.image(image)
        self.display()

    def _init_128_64(self):
        # 128x64 pixel specific initialization.
        self.command(SSD1306_DISPLAYOFF)                    # 0xAE
        self.command(SSD1306_SETDISPLAYCLOCKDIV)            # 0xD5
        # the suggested ratio 0x80
        self.command(0x80)
        self.command(SSD1306_SETMULTIPLEX)                  # 0xA8
        self.command(0x3F)
        self.command(SSD1306_SETDISPLAYOFFSET)              # 0xD3
        self.command(0x0)                                   # no offset
        self.command(SSD1306_SETSTARTLINE | 0x0)            # line #0
        self.command(SSD1306_CHARGEPUMP)                    # 0x8D
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x10)
        else:
            self.command(0x14)
        self.command(SSD1306_MEMORYMODE)                    # 0x20
        # 0x0 act like ks0108
        self.command(0x00)
        self.command(SSD1306_SEGREMAP | 0x1)
        self.command(SSD1306_COMSCANDEC)
        self.command(SSD1306_SETCOMPINS)                    # 0xDA
        self.command(0x12)
        self.command(SSD1306_SETCONTRAST)                   # 0x81
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x9F)
        else:
            self.command(0xCF)
        self.command(SSD1306_SETPRECHARGE)                  # 0xd9
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x22)
        else:
            self.command(0xF1)
        self.command(SSD1306_SETVCOMDETECT)                 # 0xDB
        self.command(0x40)
        self.command(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
        self.command(SSD1306_NORMALDISPLAY)                 # 0xA6

    def _init_128_32(self):
        # 128x32 pixel specific initialization.
        self.command(SSD1306_DISPLAYOFF)                    # 0xAE
        self.command(SSD1306_SETDISPLAYCLOCKDIV)            # 0xD5
        # the suggested ratio 0x80
        self.command(0x80)
        self.command(SSD1306_SETMULTIPLEX)                  # 0xA8
        self.command(0x1F)
        self.command(SSD1306_SETDISPLAYOFFSET)              # 0xD3
        self.command(0x0)                                   # no offset
        self.command(SSD1306_SETSTARTLINE | 0x0)            # line #0
        self.command(SSD1306_CHARGEPUMP)                    # 0x8D
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x10)
        else:
            self.command(0x14)
        self.command(SSD1306_MEMORYMODE)                    # 0x20
        # 0x0 act like ks0108
        self.command(0x00)
        self.command(SSD1306_SEGREMAP | 0x1)
        self.command(SSD1306_COMSCANDEC)
        self.command(SSD1306_SETCOMPINS)                    # 0xDA
        self.command(0x02)
        self.command(SSD1306_SETCONTRAST)                   # 0x81
        self.command(0x8F)
        self.command(SSD1306_SETPRECHARGE)                  # 0xd9
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x22)
        else:
            self.command(0xF1)
        self.command(SSD1306_SETVCOMDETECT)                 # 0xDB
        self.command(0x40)
        self.command(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
        self.command(SSD1306_NORMALDISPLAY)                 # 0xA6

    def _init_96_16(self):
        # 96x16 pixel specific initialization.
        self.command(SSD1306_DISPLAYOFF)                    # 0xAE
        self.command(SSD1306_SETDISPLAYCLOCKDIV)            # 0xD5
        # the suggested ratio 0x60
        self.command(0x60)
        self.command(SSD1306_SETMULTIPLEX)                  # 0xA8
        self.command(0x0F)
        self.command(SSD1306_SETDISPLAYOFFSET)              # 0xD3
        self.command(0x0)                                   # no offset
        self.command(SSD1306_SETSTARTLINE | 0x0)            # line #0
        self.command(SSD1306_CHARGEPUMP)                    # 0x8D
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x10)
        else:
            self.command(0x14)
        self.command(SSD1306_MEMORYMODE)                    # 0x20
        # 0x0 act like ks0108
        self.command(0x00)
        self.command(SSD1306_SEGREMAP | 0x1)
        self.command(SSD1306_COMSCANDEC)
        self.command(SSD1306_SETCOMPINS)                    # 0xDA
        self.command(0x02)
        self.command(SSD1306_SETCONTRAST)                   # 0x81
        self.command(0x8F)
        self.command(SSD1306_SETPRECHARGE)                  # 0xd9
        if self._vccstate == SSD1306_EXTERNALVCC:
            self.command(0x22)
        else:
            self.command(0xF1)
        self.command(SSD1306_SETVCOMDETECT)                 # 0xDB
        self.command(0x40)
        self.command(SSD1306_DISPLAYALLON_RESUME)           # 0xA4
        self.command(SSD1306_NORMALDISPLAY)                 # 0xA6

    def read_data(self):
        """
        Get the luminosity readings.
        """
        read_start = self._get_time()
        contrast = self._contrast
        read_time = self._get_time() - read_start
        data = [
            (self._name, 'contrast', contrast, read_time),
        ]
        self._log_data(data)
        return data

    def meta_data(self):
        """
        Get the readings meta-data.
        """
        return {
            'contrast': {
                'type': 'gauge',
                'unit': '',
                'precision': 1,
                'range_low': 0,
                'range_high': 255,
                'sensor': self.DEVICE_NAME
            },
        }
