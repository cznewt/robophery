
==========================
Measuring Light/Luminosity
==========================

The lux is the SI unit of illuminance and luminous emittance, measuring
luminous flux per unit area. It is equal to one lumen per square metre. In
photometry, this is used as a measure of the intensity, as perceived by the
human eye, of light that hits or passes through a surface. It is analogous to
the radiometric unit watts per square metre, but with the power at each
wavelength weighted according to the luminosity function, a standardized model
of human visual brightness perception.

* http://www.intorobotics.com/common-budgeted-arduino-light-sensors/


BH1750 - I²C Luminosity Sensor
==============================

Power supply: 3~5V; Data range: 0-65535; Sensor built-in and 16bitAD
converter; Direct digital output, bypassing the complicated calculation, omit
calibration; Do not distinguish between ambient light; Close to the visual
sensitivity of spectral characteristics; For a wide range of brightness for 1
lux high precision measurement.

.. image:: /_static/img/module/bh1750.jpg
   :width: 50 %
   :align: center

More information
----------------

* http://www.instructables.com/id/BH1750-Digital-Light-Sensor/
* http://bozontlabs.blogspot.cz/2014/09/beaglebone-black-and-bh1750-light-sensor.html

Where to buy
------------

* 150 CZK - http://www.santy.cz/senzory-c24/senzor-intenzity-svetla-digi-i181/


TSL2591 - I²C Luminosity Sensor
===============================

The TSL2591 luminosity sensor is an advanced digital light sensor, ideal for
use in a wide range of light situations. Compared to low cost CdS cells, this
sensor is more precise, allowing for exact lux calculations and can be
configured for different gain/timing ranges to detect light ranges from 188
uLux up to 88,000 Lux on the fly.

The best part of this sensor is that it contains both infrared and full
spectrum diodes! That means you can separately measure infrared, full-spectrum
or human-visible light. Most sensors can only detect one or the other, which
does not accurately represent what human eyes see (since we cannot perceive
the IR light that is detected by most photo diodes) This sensor is much like
the TSL2561 but with a wider range (and the interface code is different). This
sensor has a massive 600,000,000:1 dynamic range! Unlike the TSL2561 you
cannot change the I²C address, so keep that in mind. This board/chip uses I²C
7-bit address 0x29.

.. image:: /_static/img/module/tls2591.jpg
   :width: 50 %
   :align: center

More information
----------------

* https://github.com/maxlklaxl/python-tsl2591

Where to buy
------------

* 7 USD - http://www.adafruit.com/products/1980


TSL2561 - I²C Luminosity Sensor
===============================

The TSL2561 luminosity sensor is an advanced digital light sensor, ideal for
use in a wide range of light situations. Compared to low cost CdS cells, this
sensor is more precise, allowing for exact lux calculations and can be
configured for different gain/timing ranges to detect light ranges from up to
0.1 - 40,000+ Lux on the fly. The best part of this sensor is that it contains
both infrared and full spectrum diodes! That means you can separately measure
infrared, full-spectrum or human-visible light. Most sensors can only detect
one or the other, which does not accurately represent what human eyes see
(since we cannot perceive the IR light that is detected by most photo diodes)

The sensor has a digital (i2c) interface. You can select one of three
addresses so you can have up to three sensors on one board - each with a
different i2c address. The built in ADC means you can use this with any
microcontroller, even if it doesn't have analog inputs. The current draw is
extremely low, so its great for low power data-logging systems. about 0.5mA
when actively sensing, and less than 15 uA when in powerdown mode.

This board/chip uses I²C 7-bit addresses 0x39, 0x29, 0x49, selectable with
jumpers.

.. image :: /_static/img/module/tls2561.jpg
   :width: 50 %
   :align: center

More information
----------------

* https://learn.adafruit.com/tsl2561/
* https://github.com/adafruit/Adafruit_TSL2561

Where to buy
------------

* 6 EUR - http://www.adafruit.com/products/439
* 6 EUR - http://www.hobbyelectronica.nl/product/tsl2561-digitale-lux-licht-sensor/


CdS - AIN Luminosity Sensor
===========================

CdS cells are little light sensors. As the squiggly face is exposed to more
light, the resistance goes down. When its light, the resistance is about
5-10KΩ, when dark it goes up to 200KΩ.

To use, connect one side of the photo cell (either one, its symmetric) to
power (for example 5V) and the other side to your microcontroller's analog
input pin. Then connect a 10K pull-down resistor from that analog pin to
ground. The voltage on the pin will be 2.5V or higher when its light out and
near ground when its dark.

.. image :: /_static/img/module/cds.jpg
   :width: 50 %
   :align: center

More information
----------------

* https://learn.adafruit.com/photocells/using-a-photocell

Where to buy
------------

* 1 USD - http://www.adafruit.com/products/161
