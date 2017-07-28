
======================
Measuring Air Humidity
======================

Relative humidity (abbreviated RH) is the ratio of the partial pressure of
water vapor to the equilibrium vapor pressure of water at the same
temperature. Relative humidity depends on temperature and the pressure of the
system of interest.

The relative humidity  of an air-water mixture is defined as the ratio of the
partial pressure of water vapour (H2O) in the mixture to the saturated vapour
pressure of water at a given temperature. Thus the relative humidity of air is
a function of both water content and temperature.

* http://en.wikipedia.org/wiki/Relative_humidity
* https://www.kandrsmith.org/RJS/Misc/Hygrometers/calib_many.html


DHT11 - GPIO Humidity and Temperature Sensor 
============================================

The DHT11 is a basic, ultra low-cost digital temperature and humidity sensor.
It uses a capacitive humidity sensor and a thermistor to measure the
surrounding air, and spits out a digital signal on the data pin (no analog
input pins needed). Its fairly simple to use, but requires careful timing to
grab data. The only real downside of this sensor is you can only get new data
from it once every 2 seconds, so when using, sensor readings can be up to 2
seconds old.

.. image :: /_static/img/module/dht11.jpg
   :width: 50 %
   :align: center

More information
----------------

* https://github.com/adafruit/Adafruit_Python_DHT
* https://cdn-shop.adafruit.com/datasheets/DHT11-chinese.pdf

Where to buy
------------

* 5 USD - https://www.adafruit.com/products/386


DHT22 - GPIO Humidity and Temperature Sensor
============================================

The DHT22 is a basic, low-cost digital temperature and humidity sensor. It
uses a capacitive humidity sensor and a thermistor to measure the surrounding
air, and spits out a digital signal on the data pin (no analog input pins
needed). Compared to the DHT11, this sensor is more precise, more accurate and
works in a bigger range of temperature/humidity, but its larger and more
expensive.

.. image :: /_static/img/module/dht22.jpg
   :width: 50 %
   :align: center

More information
----------------

* https://github.com/adafruit/Adafruit_Python_DHT 
* https://cdn-shop.adafruit.com/datasheets/DHT22.pdf

Where to buy
------------

* 10 USD - https://www.adafruit.com/products/385


HTU21D - I²C Humidity and Temperature Sensor
============================================

This I²C digital humidity sensor is an accurate and intelligent alternative to
the much simpler Humidity and Temperature Sensor - SHT15 Breakout It has a
typical accuracy of ±2% with an operating range that's optimized from 5% to
95% RH. Operation outside this range is still possible - just the accuracy
might drop a bit. The temperature output has an accuracy of ±1°C from
-30~90°C. If you're looking to measure temperature more accurately, we
recommend the MCP9808 High Accuracy I²C Temperature Sensor Breakout Board.

.. image :: /_static/img/module/htu21d.jpg
   :width: 50 %
   :align: center

More information
----------------

* English datasheet http://www.adafruit.com/datasheets/1899_HTU21D.pdf
* http://randymxj.com/?p=550 - Python Library for HTU21D Humidity Sensor on Beaglebone Black and Raspberry Pi with Adafruit_I²C 
* https://github.com/randymxj/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_HTU21D - This library is used as source, requires Adafruit_I²C python library to work
* https://learn.adafruit.com/adafruit-htu21d-f-temperature-humidity-sensor?view=all

Where to buy
------------

* 15 USD - http://www.adafruit.com/product/1899
* 15 USD - https://www.sparkfun.com/products/12064


SI7021 - I²C Humidity and Temperature Sensor
============================================

The Si7021 is a low-cost, easy to use, highly accurate, digital temperature
and humidity sensor. All you need is two lines for I2C communication, and
you’ll have relative humidity readings and accurate temperature readings as
well! This sensor is ideal for environmental sensing and data logging, perfect
for a weather station or humidor control system.

.. image :: /_static/img/module/si7021.jpg
   :width: 50 %
   :align: center

More information
----------------

* https://github.com/ControlEverythingCommunity/SI7021/blob/master/Python/SI7021.py
* https://learn.sparkfun.com/tutorials/si7021-humidity-and-temperature-sensor-hookup-guide

Where to buy
------------

* 7 USD - https://www.sparkfun.com/products/13763


AM2320 - I²C Humidity and Temperature Sensor
============================================

The AM2320 is effectively the latest version of the AM2302 with the addition
of an option to communicate over I2C interface. It is physically a little
smaller, but with identical pin-out. The one-wire serial of the AM2302 is
retained making this a simple drop-in replacement.

.. image :: /_static/img/module/am2320.jpg
   :width: 50 %
   :align: center

More information
----------------

* http://akizukidenshi.com/download/ds/aosong/AM2320.pdf


SHT30/SHT31 - I²C Humidity and Temperature Sensor
=================================================

.. image :: /_static/img/module/sht3x.jpg
   :width: 50 %
   :align: center

Sensiron Temperature/Humidity sensors are some of the finest & highest-
accuracy devices you can get. And, finally we have some that have a true I2C
interface for easy reading.


More information
----------------

* https://cdn-shop.adafruit.com/product-files/2857/Sensirion_Humidity_SHT3x_Datasheet_digital-767294.pdf

Where to buy
------------

* 14 USD - https://www.adafruit.com/product/2857
* 5 USD - aliexpress
