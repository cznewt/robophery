
==========================
Measuring Electric Current
==========================

* http://en.wikipedia.org/wiki/Electricity_meter


INA219 - I²C DC Current Sensor
==============================

Most current-measuring devices such as our current panel meter are only good
for low side measuring. That means that unless you want to get a battery
involved, you have to stick the measurement resistor between the target ground
and true ground. This can cause problems with circuits since electronics tend
to not like it when the ground references change and move with varying current
draw. This chip is much smarter - it can handle high side current measuring,
up to +26VDC, even though it is powered with 3 or 5V. It will also report back
that high side voltage, which is great for tracking battery life or solar
panels.

A precision amplifier measures the voltage across the 0.1 ohm, 1% sense
resistor. Since the amplifier maximum input difference is ±320mV this means it
can measure up to ±3.2 Amps. With the internal 12 bit ADC, the resolution at
±3.2A range is 0.8mA. With the internal gain set at the minimum of div8, the
max current is ±400mA and the resolution is 0.1mA. Advanced hackers can remove
the 0.1 ohm current sense resistor and replace it with their own to change the
range (say a 0.01 ohm to measure up 32 Amps with a resolution of 8mA)

.. image:: /_static/img/module/ina219.jpg
   :width: 50 %
   :align: center

Where to buy
------------

* 10 USD - https://www.adafruit.com/product/904


ACS712 - ADC Electrometer
=========================

Hall Effect based linear ACS712 current sensor. The sensor gives precise
current measurement for both AC and DC signals. Thick copper conductor and
signal traces allows for survival of the device up to 5 times overcurrent
conditions.

The ACS712 outputs an analog voltage output signal that varies linearly with
sensed current. The device requires 5VDC for VCC and a couple of filter
capacitors. Please keep in mind that though the ACS712 is rated for 2.1kV
isolation, the PCB it is on is not designed for that type of voltage. Please
keep that in mind if you are using this breakout in high voltage applications.

.. image:: /_static/img/module/acs712.jpg
   :width: 50 %
   :align: center

More information
----------------

* https://www.sparkfun.com/datasheets/BreakoutBoards/0712.pdf

Where to buy
------------

* 7 EUR - http://www.hobbyelectronica.nl/product/acs712-stroommeter-20a/


HT-1PD - GPIO Digital Electrometer
==================================

Jednofázový, jednosazbový podružný elektroměr pro montáž na DIN lištu.
Impulsní výstup pro externí záznam spotřeby např. v PC (podle velikosti
oakmžitého odběru se mění frekvence blikání LED diody a frekvence pulsů
impulsního výstupu- viz. tech. parametry). Ideální pro měření spotřeby
jednotlivých nájemníků, v autokempech, chatách apod.

.. image:: /_static/img/module/ht-1pd.jpg
   :width: 50 %
   :align: center

Where to buy
------------

* 400 CZK - http://www.hutermann.com/eshop/001/produkty/elektromery-prodlu-zovaci-kabely-od-75-/elektromer-na-din-listu-jednofazovy-digitalni-1f-meric-spotreby-wattmetr-hutermann-ht-1pd


Non-Invasive Current Sensor
===========================

This non-invasive current sensor (also known as a “split core current
transformer”) can be clamped around the supply line of an electrical load to
tell you how much current is passing through it. It does this by acting as an
inductor and responding to the magnetic field around a current-carrying
conductor. By reading the amount of current being produced by the coil, you
can calculate how much current is passing through the conductor.

This particular current sensor will measure a load up to 30 Amps which makes
it great for building your own energy monitor to keep your power usage down,
or even building an over-current protection device for an AC load. This sensor
does not have a load resistor built in, so in most cases it will be necessary
to place a resistor across the output to convert the coil’s induced current to
a very small measurable voltage.

.. image:: /_static/img/module/current_sensor.jpg
   :width: 50 %
   :align: center

More information
----------------

* Datasheet http://dlnmh9ip6v2uc.cloudfront.net/datasheets/Sensors/Current/ECS1030-L72-SPEC.pdf
* http://openenergymonitor.org/emon/node/58

Where to buy
------------

* 10 USD - https://www.sparkfun.com/products/11005

