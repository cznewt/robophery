
===============================
RoboPhery: Robotic Peripehrials
===============================

Python library for interfacing low level hardware sensors and actuators with
MQTT and Statsd bindings.


Standards
=========

* SenML https://tools.ietf.org/html/draft-jennings-senml-08


GPIO modules
============


Generic GPIO switch sensor
--------------------------

* https://github.com/adafruit/Adafruit_Python_GPIO


Generic GPIO relay actuator
---------------------------

* https://github.com/adafruit/Adafruit_Python_GPIO


L293D - GPIO DC motor actuator
------------------------------

* http://www.instructables.com/id/Controlling-Direction-and-Speed-of-DC-Motor-Using-/
* https://github.com/jamesevickery/l293d


DS18B20 - 1-wire temperature sensor
-----------------------------------

* https://github.com/timofurrer/w1thermsensor
* https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing?view=all
* http://www.bonebrews.com/temperature-monitoring-with-the-ds18b20-on-a-beaglebone-black/
* http://interactingobjects.com/ds18b20-temperature-sensor-on-a-beaglebone-black-running-ubuntu/


DHT11/DHT22 - GPIO humidity/temperature sensors
-----------------------------------------------

* https://github.com/adafruit/Adafruit_Python_DHT
* https://cdn-shop.adafruit.com/datasheets/DHT22.pdf
* https://cdn-shop.adafruit.com/datasheets/DHT11-chinese.pdf


I2C modules
===========


BH1750 - I2C luminosity sensor
------------------------------

* http://www.instructables.com/id/BH1750-Digital-Light-Sensor/


BMP085/BMP180 - I2C humidity/pressure sensor
--------------------------------------------

* https://github.com/eddienigma/rpi-python-bmp180
* https://github.com/adafruit/Adafruit_Python_BMP
* https://raw.githubusercontent.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/master/Adafruit_I2C/Adafruit_I2C.py


HTU21D - I2C humidity/temperature sensor
----------------------------------------

* http://randymxj.com/?p=550 - Python Library for HTU21D Humidity Sensor on Beaglebone Black and Raspberry Pi with Adafruit_I2C
* https://github.com/randymxj/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_HTU21D - This library is used as source, requires Adafruit_I2C python library to work
* https://learn.adafruit.com/adafruit-htu21d-f-temperature-humidity-sensor?view=all


MCP9808 - I2C temperature sensor
--------------------------------

* https://learn.adafruit.com/adafruit-mcp9808-precision-i2c-temperature-sensor-guide/overview
* https://github.com/philipcristiano/beagleboneblack/blob/master/mcp9808.py


TSL2591 - I2C luminosity sensor
-------------------------------

* https://github.com/maxlklaxl/python-tsl2591


AtlasScientific sensors
-----------------------

* https://github.com/AtlasScientific/Raspberry-Pi-sample-code
* https://www.atlas-scientific.com/_files/code/pi_sample_code.pdf

BLE modules
===========


CC2541 SensorTag - multiple sensors
-----------------------------------

* https://github.com/mvartani76/RPi-Ble-Sensor-Tag-Python


Parrot Flower Power - BLE gardening sensors
-------------------------------------------

* http://www.parrot.com/usa/products/flower-power/
* http://developer.parrot.com/docs/flowerpower/FlowerPower-BLE.pdf
* http://global.parrot.com/media/porticus/ressources/files/BAT5_Datasheet_FlowerPower_UK_05nov13.pdf
* http://www.jaredwolff.com/blog/get-started-with-bluetooth-low-energy/
