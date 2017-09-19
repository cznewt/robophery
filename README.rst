
======================================
RoboPhery: Robotic Peripherals Project
======================================

.. image:: https://readthedocs.org/projects/robophery/badge/?version=latest
    :target: http://robophery.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/robophery/Lobby
    :alt: Join Chat on Gitter.im

Design and implementation of Python library for interfacing low level hardware
sensors and actuators with MQTT and TSDB bindings. The system architecture is
designed to be so simple at hardware level to support sigle-board
microcontrollers like ESP2866, ESP32 modules as well as sigle-board computers
based on ARM or x86 architectures. The communication among devices is handled
by the standard MQTT message bus.

Installation
============

Virtualenv
----------

Install required dependencies

.. code-block:: bash

    apt-get install python-dev libyaml-dev git python-virtualenv

Prepare clean virtualenv

.. code-block:: bash

    virtualenv /opt/robophery

Clone this repository

.. code-block:: bash

    git clone https://github.com/cznewt/robophery.git

Install dependencies and robophery

.. code-block:: bash

    source /opt/robophery/bin/activate
    pip install -r requirements.txt
    python setup.py install

Service
-------

If you are running systemd-enabled distribution, setup systemd unit file to
start robophery automatically:

.. code-block:: bash

    cat << EOF >>/etc/systemd/system/robophery.service
    [Unit]
    Description=robophery manager
    Wants=mosquitto.service
    After=network.target mosquitto.service
    
    [Service]
    Type=simple
    User=root
    Group=root
    WorkingDirectory=/opt/robophery
    Environment=ROBOPHERY_CONF=/etc/robophery
    ExecStart=/opt/robophery/bin/rp_manager
    RestartSec=5
    Restart=on-failure
    
    [Install]
    WantedBy=multi-user.target
    EOF

Create ``/opt/robophery`` directory and config file
``/opt/robophery/robophery_conf.py`` and start the service.

.. code-block:: bash

    systemctl daemon-reload
    systemctl start robophery
    systemctl enable robophery

To check status of a service, use ``systemctl status -l robophery``.
To see logs, you can use systemd journal (eg. ``journalctl -u robophery -f``)

Configuration
=============

You can use `salt-formula-robophery
<https://github.com/salt-formulas/salt-formula-robophery>`_ to automate both installation and
configuration or you can provide config file in any other way.

Example
-------

Following example configuration will setup robophery running on Raspberry Pi
and will collect data from DHT22 sensor attached to GPIO pin 3 and publish it
to MQTT every 60 seconds.

::

  CONF = {
    'name': 'mylittleraspberry',
    'log_level': 'debug',
    'log_handlers': ['console', 'syslog'],
    'read_interval': 10000,
    'publish_interval': 60000,
    'platform': 'raspberrypi',
    'config': {
      'comm': {
        'default_mqtt': {
          'host': 'mymqttserver',
          'port': 1883,
          'class': 'robophery.comm.linux.mqtt.PahoMqttComm'
        },
      },
      'interface': {
        'local_gpio': {
          'engine': 'gpio',
          'class': 'robophery.platform.rpi.gpio.RaspberryPiGpioInterface'
        }
      },
      'module': {
        'dht22': {
          'data': {
            'pin': 3,
          },
          'class': 'robophery.module.gpio.dht22.Dht22Module'
        }
      }
    }
  }

More Information
================

* `Offical RoboPhery Documentation <http://robophery.readthedocs.io/>`_
* `Sensor Markup Language (SenML) <https://tools.ietf.org/html/draft-jennings-core-senml>`_
