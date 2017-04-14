
========================
Measuring Color of Light
========================

TCS34725 - I²C RGB Color Sensor 
===============================

TCS34725 has RGB and Clear light sensing elements. An IR blocking filter,
integrated on-chip and localized to the color sensing photodiodes, minimizes
the IR spectral component of the incoming light and allows color measurements
to be made accurately. The filter means you'll get much truer color than most
sensors, since humans don't see IR. The sensor also has an incredible
3,800,000:1 dynamic range with adjustable integration time and gain so it is
suited for use behind darkened glass.

You can power the breakout with 3-5VDC safely and level shifting for the I2C
pins so they can be used with 3.3V or 5V logic. Neutral 4150°K temperature LED
with a MOSFET driver onboard to illuminate what you're trying to sense. The
LED can be easily turned on or off by any logic level output.

Connect to any microcontroller with I2C and our example code will quickly get
you going with 4 channel readings. We include some example code to detect
light lux and temperature that we snagged from the eval board software.

.. image:: /_static/img/module/tcs34725.jpg
   :width: 50 %
   :align: center

More information
----------------

* https://learn.adafruit.com/adafruit-color-sensors/overview

Where to buy
------------

* 8 USD - https://www.adafruit.com/product/1334
