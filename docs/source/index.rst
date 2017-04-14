=======================
RoboPhery Documentation
=======================

Internet of Things is growing phenomena caused by advances of speed and size
of computational hardware. It is possible to collect data from various
sensors, devices or services and react to evaluated envent and start the
defined process. These systems are closely connected with cloud services as
the provide publicly accesible interface for management and visualization,
coputational and storage power for forecasts and other big data processing to
create ambient intelligence environment.

This article proposes the design and implementation of Python library for
interfacing low level hardware sensors and actuators with MQTT and statsd
bindings. The system architecture is designed to be so simple at device level
to support low level architectures like ESP2866 modules as well as ARM or x86
platforms. The inter-device communication is handled over standard message
bus.

.. toctree::
   :maxdepth: 3
   :glob:

   doc/arch/index.rst
   doc/device/index.rst
   doc/interface/index.rst
   doc/actuator/index.rst
   doc/sensor/index.rst
   doc/virtual/index.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
