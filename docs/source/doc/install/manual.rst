
===================
Manual Installation
===================

RoboPhery is simple Python application suitable to run with minimal resources
and dependencies.

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

    cat << EOF >>/etc/systemd/system/robophery-manager.service
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
    systemctl start robophery-manager
    systemctl enable robophery-manager

To check status of a service, use ``systemctl status -l robophery-manager``.
To see logs, you can use systemd journal (eg. ``journalctl -u robophery-manager -f``)

Configuration
=============

Following example configuration will setup robophery running on Raspberry Pi
and will collect data from DHT22 sensor attached to GPIO pin 3 and publish it
to MQTT every 60 seconds.

.. code-block:: python

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
