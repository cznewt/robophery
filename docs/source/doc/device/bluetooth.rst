
=================
BlueTooth Devices
=================

Bluetooth uses the same 2.4Ghz unlicensed band as most Wi-Fi routers.
Bluetooth Low Energy (BLE) is also known as Bluetooth 4.0 and Bluetooth Smart.
It's called low-energy because it basically is. BLE devices can run for more
than 2 years with a single coin battery depending on the signal strenth and
how frequently they broadcast information.

Apple iBeacon uses Bluetooth Low Energy to create 'beacon' around regions so
apps can be alerted when users enter them. The hardware beacons are a small
wireless sensors placed inside any physical space that transmit data to your
iPhone using Bluetooth Low Energy. iOS devices can also be iBeacons. Whilst
Google have focussed on Near Field Communication (NFC), Android V4.3 has
native support for Bluetooth Low Energy.


More information
================

* http://www.dreamgreenhouse.com/projects/2014/ibeacon/index.php
* http://www.intorobotics.com/pick-right-bluetooth-module-diy-arduino-project/


CC2541 SensorTag Kit
====================

The SensorTag is fitted with six sensors and all sensors are chosen to be
small, energy efficient and low cost surface mount devices. The sensors use
I2C interface and are connected to the same interface bus with separate enable
signals. To minimize current consumption all sensors are by default disabled
and they are in sleep mode between measurements. Each sensor can be enabled
and read individually. The SensorTag includes the following sensors:

* IR Temperature Sensor (TMP006) from Texas Instruments, http://www.ti.com/product/tmp006
* Humidity Sensor (SHT21) from Sensirion, http://www.sensirion.com/en/products/humidity-temperature/humidity-sensor-sht21/
* Pressure Sensor (T5400) from Epcos, http://www.epcos.com/inf/57/ds/T5400.pdf
* Accelerometer (KXTJ9) from Kionix, http://www.kionix.com/accelerometers/kxtj9
* Gyroscope (IMU-3000) from InvenSense, http://www.invensense.com/mems/gyro/imu3000.html
* Magnetometer (MAG3110) from Freescale, http://www.freescale.com/webapp/sps/site/prod_summary.jsp?code=MAG3110

.. figure:: /_static/img/module/cc2541.jpg
   :scale: 30 %
   :align: center

More information
----------------

* http://www.ti.com/tool/cc2541dk-sensor#descriptionArea
* https://github.com/msaunby/ble-sensor-pi
* http://mike.saunby.net/2013/04/raspberry-pi-and-ti-cc2541-sensortag.html
* https://github.com/mvartani76/RPi-Ble-Sensor-Tag-Python

Where to buy
------------

* https://store.ti.com/CC2541DK-SENSOR-CC2541-SensorTag-Development-Kit-P3192.aspx


CC2650 SensorTag Kit
====================

The new TI SensorTag is based on the CC2650 ultra-low power wireless MCU,
offering a high-performance ARM® Cortex®-M3 and a fraction of the power
consumption compared to previous Bluetooth® Smart products. It also includes
cloud support, letting you move your sensor data from the smartphone app to
the cloud with a simple touch on the screen.

.. figure:: /_static/img/module/cc2650.jpg
   :scale: 30 %
   :align: center


Where to buy
------------

* 800 CZK - http://cz.farnell.com/texas-instruments/cc2650stk/sensortag-iot-kit/dp/2470181
