# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme:
    long_description = ''.join(readme.readlines())

setup(
    name='robophery',
    version='0.1',
    description='Python library for interfacing low level hardware sensors and actuators with MQTT bindings.',
    long_description=long_description,
    author='Aleš Komárek',
    author_email='ales.komarek@newt.cz',
    license='Apache Software License',
    url='http://www.github.cz/cznewt/robophery',
    modules=['robophery'],
    classifiers=[
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'rp_discover_ft232h = robophery.utils.ft232h:discover_devices',
            'rp_read_bh1750 = robophery.cli.read:read_bh1750',
            'rp_read_dht22 = robophery.cli.read:read_dht22',
            'rp_read_ds18 = robophery.cli.read:read_ds18',
            'rp_read_flower_power = robophery.cli.read:read_flower_power',
            'rp_read_l293d = robophery.cli.read:read_l293d',
            'rp_read_mcp9808 = robophery.cli.read:read_mcp9808',
            'rp_read_switch = robophery.cli.read:read_switch',
        ],
    },
)
