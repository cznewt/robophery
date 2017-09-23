
=================
Salt installation
=================

You can use `salt-formula-robophery <https://github.com/salt-formulas/salt-
formula-robophery>`_ to automate both installation and configuration.

Following configuration sets up multiple sensors over multiple interfaces.

.. code-block:: yaml

    robophery:
      server:
        name: garden
        platform: raspberrypi
        log_level: debug
        log_handlers:
        - console
        read_interval: 3000
        publish_interval: 6000
        interface:
          local_gpio:
            class: robophery.platform.rpi.gpio.RaspberryPiGpioInterface
            engine: gpio
          local_i2c:
            class: robophery.platform.linux.i2c.SMBusI2cInterface
            engine: i2c
            bus_number: 1
          local_w1:
            class: robophery.platform.linux.w1.LinuxW1Interface
            engine: w1
            data:
              iface: local_gpio
              pin: 4
        module:
          air_temp_humid:
            class: robophery.module.i2c.sht3x.Sht3xModule
            data:
              addr: 0x44
              iface: local_i2c
          light_luminosity:
            class: robophery.module.i2c.bh1750.Bh1750Module
            data:
              addr: 0x23
              iface: local_i2c
          light_switch:
            class: robophery.module.gpio.relay.RelayModule
            invert_logic: true
            data:
              iface: local_gpio
              pin: 36
          air_fan_switch:
            class: robophery.module.gpio.relay.RelayModule
            invert_logic: true
            data:
              iface: local_gpio
              pin: 38
          nutrient_pump_switch:
            class: robophery.module.gpio.relay.RelayModule
            invert_logic: true
            data:
              iface: local_gpio
              pin: 40 
          water_pump_switch:
            class: robophery.module.gpio.relay.RelayModule
            invert_logic: true
            data:
              iface: local_gpio
              pin: 12
          water_level:
            class: robophery.module.gpio.switch.SwitchModule
            data:
              iface: local_gpio
              pin: 13
              pull_up_down: down
          water_ph:
            class: robophery.module.i2c.ezoph.EzoPhModule
            data:
              addr: 0x68
              iface: local_i2c
          water_ec:
            class: robophery.module.i2c.ezoec.EzoEcModule
            data:
              addr: 0x69
              iface: local_i2c
          water_temp:
            class: robophery.module.w1.ds18.Ds18Module
            data:
              iface: local_w1
              addr: 00145071daff
            type: DS18B20
