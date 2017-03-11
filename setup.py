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
            'rp_ft232h_discovery = robophery.utils.ft232h:discover_devices',
            'rp_bh1750 = robophery.cli:module_bh1750',
            'rp_bmp085 = robophery.cli:module_bmp085',
            'rp_htu21d = robophery.cli:module_htu21d',
            'rp_mcp9808 = robophery.cli:module_mcp9808',
            'rp_dht11 = robophery.cli:module_dht11',
            'rp_dht22 = robophery.cli:module_dht22',
            'rp_ds18 = robophery.cli:module_ds18',
            'rp_pfp = robophery.cli:module_pfp',
            'rp_l293d = robophery.cli:module_l293d',
            'rp_relay = robophery.cli:module_relay',
            'rp_switch = robophery.cli:module_switch',
        ],
    },
)
