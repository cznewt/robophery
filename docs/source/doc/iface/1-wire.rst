
=============
Dallas 1-Wire
=============

The 1-Wire system is the invention of Dallas Semiconductors, who were acquired
by Maxim in 2001. 1-Wire and iButton are essentially two implementations of
the same technology, the former being manufactured in traditional IC packages
and the latter in a robust stainless steel package (shaped in like a button).
This section focuses on the 1-Wire devices and networks.

1-Wire is a bit of a misnomer, since the bus in fact requires two wires. One
wire is a ground wire and the the second carries both power and data. Many
1-Wire sensors are inexpensive and bus-powered, using a small capacitor to
accumulate charge while the bus is idle and then using this stored energy to
communicate with the bus master when polled. More complex sensors require a
regulated 5V supply or unregulated 12V, both of which can be supplied along
with the serial bus through a single Cat-5 cable. The power is usually
injected into each branch of the serial network by a hub.

Interference
============

If you have long 1-Wire network runs and are having problems with glitches you
should add a Schottky diode to the end of your network. Typically a 1N5817
diode reverse biased across sensors will acheive this. Solder the side with
the stripe to pin 2 and the other side to pin 1 of the DS18S20.

Usage
=====

A 1-Wire network isn't going to do everything but there are some things that
it are particularly good at and for for which there is good support, with
clever devices. Its inherent simplicity, low power consumption and fairly low
speed, mean that it is well suited to basic monitoring situations and the main
things I'm using it for are:

* Temperature sensors
* Door contact sensors
* Mains power present sensor
* Weather instruments
* Switching on/off devices/lighting 

More information
================

* Maxim Dallas 1-Wire, MicroLan, iButton: A Hobbyist's View http://www.arunet.co.uk/tkboyd/e1didx.htm
* Guidelines for Reliable Long Line 1-Wire Networks http://www.maximintegrated.com/en/app-notes/index.mvp/id/148
