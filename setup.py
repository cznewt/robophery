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
)
