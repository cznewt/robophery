=======================
RoboPhery Documentation
=======================

Internet of Things is growing phenomena caused by advances of speed and size
of computational hardware. It is possible to collect data from various
sensors, devices or services and react to evaluated envent and start the
predefined process. These systems are closely connected with Cloud based
services as they provide publicly accesible interface for management and
visualization, coputational and storage cababilities for forecasts and other
advanced data processing to create ambient intelligence environment. The true
ambient environments react to the presence of people and the sensors and
actuators have become part of the environment.

This article shows the design and implementation of Python library for
interfacing low level hardware sensors and actuators with MQTT and TSDB
bindings. The system architecture is designed to be so simple at hardware
level to support sigle-board microcontrollers like ESP2866, ESP32 modules as
well as sigle-board computers based on ARM or x86 architectures. The
communication among devices is handled by the standard MQTT message bus.

.. toctree::
   :maxdepth: 3
   :glob:

   doc/arch/index
   doc/install/index
   doc/device/index
   doc/interface/index
   doc/actuator/index
   doc/sensor/index
   doc/virtual/index
