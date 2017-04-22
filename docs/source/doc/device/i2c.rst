
====================
I²C Extension Boards
====================


MCP23008 - I²C to GPIO Extension Board
======================================

Add another 8 pins to your microcontroller using a MCP23008 port expander. The
MCP23008 uses two I²C pins (these can be shared with other I²C devices), and
in exchange gives you 8 general purpose pins. You can set each of 8 pins to be
input, output, or input with a pullup. There's even the ability to get an
interrupt via an external pin when any of the inputs change so you don't have
to keep polling the chip.

Use this chip from 2.7-5.5V (good for any 3.3V or 5V setup), and you can
sink/source up to 20mA from any of the I/O pins so this will work for LEDs and
such. Team it up with a high-power MOSFET if you need more juice. DIP package
means it will plug into any breadboard or perfboard.

You can set the I²C address by tying the ADDR0-2 pins to power or ground, for
up to 8 unique addresses. That means 8 chips can share a single I²C bus -
that's 64 I/O pins,

.. image:: /_static/img/device/mcp23008.jpg
   :width: 50 %
   :align: center

Where to buy
------------

* 2 USD - https://www.adafruit.com/product/593


PCF8574 - I²C to GPIO Extension Board
=====================================

.. image:: /_static/img/device/pcf8574.jpg
   :width: 50 %
   :align: center


More infromation
----------------

* http://www.ti.com/lit/ds/symlink/pcf8574.pdf

Where to buy
------------

* 100 CZK - http://www.santy.cz/moduly-c22/arduino-lcd-1602-16x2-modul-shield-mega-nano-i2c-redukce-seriovy-serial-2560-i52/


PCA9685 - I²C to PWM Extension Board
====================================

It's an i2c-controlled PWM driver with a built in clock. That means that,
unlike the TLC5940 family, you do not need to continuously send it signal
tying up your microcontroller. It is 5V compliant, which means you can control
it from a 3.3V microcontroller and still safely drive up to 6V outputs (this
is good for when you want to control white or blue LEDs with 3.4+ forward
voltages). 6 address select pins so you can wire up to 62 of these on a single
i2c bus, a total of 992 outputs - that's a lot of servos or LEDs.

.. image:: /_static/img/device/pca9685.jpg
   :width: 50 %
   :align: center

Where to buy
------------

* 15 USD - https://www.adafruit.com/product/815
