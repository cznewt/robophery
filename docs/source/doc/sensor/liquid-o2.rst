
=====================================
Measuring Oxygen Saturation of Liquid
=====================================

Oxygen saturation (symbol SO2) is a relative measure of the amount of oxygen
that is dissolved or carried in a given medium. It can be measured with a
dissolved oxygen probe such as an oxygen sensor or an optode in liquid media,
usually water. The standard unit of oxygen saturation is percent (%).

Dissolved oxygen is expressed in mg/L. There are many factors that must be taken
into account when reading dissolved oxygen, such as salinity and temperature.
Therefore, there is no simple linear equation that will derive the dissolved oxygen
from the probes output voltage.

* https://en.wikipedia.org/wiki/Oxygen_saturation


Atlas Scientific DO Kit - I²C Liquid Oxygen Saturation Sensor
=============================================================

This galvanic dissolved oxygen probe is a passive device that generates a small voltage
from 0mv to 47mv depending on the oxygen saturation of the HDPE sensing membrane.
This voltage can easily be read by a multimeter or an analog to digital converter.

Determining the dissolved oxygen percentage as compaired to atmospheric
oxygen. (non scientific measurement)

% saturation= (mv in water / mv in air) x 100

Determining the dissolved oxygen in mg/L from the probes output voltage is
very complex, and the responsibility of the embedded systems engineer.

The Atlas Scientific Dissolved Oxygen Circuit will perform the calculations
for you, to derive oxygen saturation in mg/L.

.. image :: /_static/img/module/as_do.png
   :width: 50 %
   :align: center

More information
----------------

* https://www.atlas-scientific.com/_files/_app_notes/do-app-note.pdf

Where to buy
------------

* 260 USD - https://www.atlas-scientific.com/product_pages/kits/do_kit.html
