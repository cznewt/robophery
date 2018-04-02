
=====================
Measuring Temperature
=====================

A temperature is a comparative objective measure of hot and cold. It is
measured, typically by a thermometer, through the bulk behavior of a
thermometric material, detection of heat radiation, or by particle velocity or
kinetic energy. It may be calibrated in any of various temperature scales,
Celsius, Fahrenheit, Kelvin, etc.

* http://en.wikipedia.org/wiki/Temperature


MCP9808 - I²C Temperature Sensor
================================

This I²C digital temperature sensor is one of the more accurate/precise we've
ever seen, with a typical accuracy of ±0.25°C over the sensor's -40°C to
+125°C range and precision of +0.0625°C. They work great with any
microcontroller using standard i2c. There are 3 address pins so you can
connect up to 8 to a single I2C bus without address collisions. Best of all, a
wide voltage range makes is usable with 2.7V to 5.5V logic.

.. image :: /static/img/module/mcp9808.jpg
   :width: 50 %
   :align: center

More information
----------------

* https://learn.adafruit.com/adafruit-mcp9808-precision-i2c-temperature-sensor-guide/overview
* https://github.com/philipcristiano/beagleboneblack/blob/master/mcp9808.py

Where to buy
------------

* 5 USD - http://www.adafruit.com/products/1782 
* 5 EUR - http://www.hobbyelectronica.nl/product/mcp9808-precieze-i2c-temperatuur/


BMP180 - I²C Temperature and Pressure Sensor
============================================

See Air pressure chapter


DS18B20 - GPIO Temperature Sensor 
=================================

The DS18B20 is a rather useful sensor because you can read more than one of
them using the same GPIO pin. Device is able to recognise the input from each
separate sensor.

.. image :: /static/img/module/ds18b20.jpg
   :width: 50 %
   :align: center

More information
----------------

* http://datasheets.maximintegrated.com/en/ds/DS18B20.pdf 
* http://learn.adafruit.com/measuring-temperature-with-a-beaglebone-black
* http://designandmake.designspark.com/eng/projects/35/view/stage/design
* https://github.com/timofurrer/w1thermsensor
* http://www.bonebrews.com/temperature-monitoring-with-the-ds18b20-on-a-beaglebone-black/
* http://interactingobjects.com/ds18b20-temperature-sensor-on-a-beaglebone-black-running-ubuntu/

Where to buy
------------

* 55 CZK - http://www.gme.cz/teplotni-cidla-s-cislicovym-vystupem/ds18b20-p530-067/


MAX31855 - I²C Thermocouple Amplifier
=====================================

Thermocouples are very sensitive, requiring a good amplifier with a cold-
compensation reference. The MAX31855K does everything for you, and can be
easily interfaced with any microcontroller, even one without an analog input.
This breakout board has the chip itself, a 3.3V regulator with 10uF bypass
capacitors and level shifting circuitry, all assembled and tested. Comes with
a 2 pin terminal block (for connecting to the thermocouple) and pin header (to
plug into any breadboard or perfboard).

.. image :: /static/img/module/max31855.jpg
   :width: 50 %
   :align: center

More information
----------------

* http://www.picotech.com/applications/pt100.html
* http://openenergymonitor.org/emon/buildingblocks/rtd-temperature-sensing

Where to buy
------------

* 15 EUR - http://www.hobbyelectronica.nl/product/thermocouple-amplifier-max31855/
* 15 USD - http://www.adafruit.com/product/269
* additional 10 USD - Thermocouple Type-K Glass Braid Insulated - http://www.adafruit.com/products/270


TMP36 - AIN Temperature Sensor
==============================

Low cost temperature sensor.

.. image:: /static/img/module/tmp36.jpg
   :width: 50 %
   :align: center

More information
----------------

* http://www.picotech.com/applications/pt100.html
* http://openenergymonitor.org/emon/buildingblocks/rtd-temperature-sensing
* TMP36 Temperature Sensor http://learn.adafruit.com/tmp36-temperature-sensor

Where to buy
------------

* 2 USD - http://www.adafruit.com/products/165


LM335 - AIN Temperature Sensor 
==============================

The LM135 series are precision, easily-calibrated, integrated circuit
temperature sensors. Operating as a 2-terminal zener, the LM135 has a
breakdown voltage directly proportional to absolute temperature at 10 mV/°K.
With less than 1-Ω dynamic impedance, the device operates over a current range
of 400 µA to 5 mA with virtually no change in performance. When calibrated at
25°C, the LM135 has typically less than 1°C error over a 100°C temperature
range. Unlike other sensors, the LM135 has a linear output.

.. image:: /static/img/module/lm335.jpg
   :width: 50 %
   :align: center

More information
----------------

* GardenBot - The Soil Temperature Sensor http://gardenbot.org/howTo/soilTemp/
* http://www.ti.com/product/LM335

Where to buy
------------

* 17 CZK - http://www.gme.cz/teplotni-cidla-s-analogovym-vystupem/lm335-p530-003/
