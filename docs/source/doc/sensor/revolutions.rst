
====================
Measuing Revolutions
====================


3 Wire Fans - GPIO  Sensor
==========================

3 wire fans have an extra OUTPUT from the fan to tell the (generally
motherboard) what speed the fan is turning.

.. figure:: /_static/img/module/3pin-fan.jpg
   :width: 50 %
   :align: center

Wiring schemes
--------------

.. figure:: /_static/img/scheme/fan_revolutions.jpg
   :width: 50 %
   :align: center

   Measuring PC fan revolutions


4 Wire Fans - GPIO Sensor/PWM Actuator
======================================

4 wire fans have that same output as 3-wire fans, but also a PWM input pin
that you can drive with a regular old pwm output pin from an arduino (or
motherboard).

More information
----------------

* http://electronics.stackexchange.com/questions/62324/arduino-controlled-pwm-pc-fan
* http://formfactors.org/developer/specs/4_Wire_PWM_Spec.pdf
