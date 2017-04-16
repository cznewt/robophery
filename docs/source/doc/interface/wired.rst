

================
Wired Interfaces
================

GPIO
====

General-purpose input/output (GPIO) is a generic pin on an integrated circuit
or computer board whose behavior—including whether it is an input or output
pin—is controllable by the user at run time.

GPIO pins have no predefined purpose, and go unused by default. The idea is
that sometimes a system integrator who is building a full system might need a
handful of additional digital control lines—and having these available from a
chip avoids having to arrange additional circuitry to provide them. For
example, the Realtek ALC260 chips (audio codec) have 8 GPIO pins, which go
unused by default. Some system integrators (Acer Inc. laptops) use the first
GPIO (GPIO0) on the ALC260 to turn on the amplifier for the laptop's internal
speakers and external headphone jack.

More information
----------------

* White, Jon, ed. (2016). Raspberry Pi - The Complete Manual (7 ed.). Imagine Publishing. p. 36. ISBN 978-1785463709.
* https://en.wikipedia.org/wiki/General-purpose_input/output
* "General Purpose Input/Output". Oracle® Java ME Embedded Developer's Guide (8 ed.). Oracle Corporation. 2014.

I²C
===

I²C (Inter-Integrated Circuit), pronounced I-squared-C, is a multi-master,
multi-slave, packet switched, single-ended, serial computer bus invented by
Philips Semiconductor (now NXP Semiconductors). It is typically used for
attaching lower-speed peripheral ICs to processors and microcontrollers in
short-distance, intra-board communication. Alternatively I²C is spelled I2C
(pronounced I-two-C) or IIC (pronounced I-I-C).

Since October 10, 2006, no licensing fees are required to implement the I²C
protocol. However, fees are still required to obtain I²C slave addresses
allocated by NXP.

Several competitors, such as Siemens AG (later Infineon Technologies AG, now
Intel mobile communications), NEC, Texas Instruments, STMicroelectronics
(formerly SGS-Thomson), Motorola (later Freescale, now merged with NXP),
Nordic Semiconductor and Intersil, have introduced compatible I²C products to
the market since the mid-1990s.

More information
----------------

* https://en.wikipedia.org/wiki/I%C2%B2C
* Official I2C Specification Version 6 - http://www.nxp.com/documents/user_manual/UM10204.pdf

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
------------

If you have long 1-Wire network runs and are having problems with glitches you
should add a Schottky diode to the end of your network. Typically a 1N5817
diode reverse biased across sensors will acheive this. Solder the side with
the stripe to pin 2 and the other side to pin 1 of the DS18S20.

Usage
-----

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
----------------

* Maxim Dallas 1-Wire, MicroLan, iButton: A Hobbyist's View http://www.arunet.co.uk/tkboyd/e1didx.htm
* Guidelines for Reliable Long Line 1-Wire Networks http://www.maximintegrated.com/en/app-notes/index.mvp/id/148


Powerline
=========

Powerline technologies utilises the existing mains wiring in your home and use
it to send communications messages. There are a few downsides with this
technology. The first one is that it won't work in the event of a power cut.
The second one is that your mains power network has all sorts of devices
plugged into it that generate interference and can reduce the reliability of
communications sent over the mains power network. A third issue is that your
mains network is electrically connected to that of you neighbours and if they
are using similar equipment, this can also interfere with your system.
Different powerline technologies can also often not co-exist happily in the
same home.

Powerline Ethernet technology allows you to network devices using adaptors
plugged into mains power sockets. Speeds of up to 200Mbps are currently
available and newer standards will enable speeds up to 380Mbps.


Structured Wiring
=================

Structured wiring is a concept where all wires and cabling run from one single
point in your home, to enable communications, entertainment and home
automation. Structured wiring is the network for all of these services and is
where you would typically install your home automation system. The approach
allows flexible use of the installed networking cables and simply
reconfiguration to support new services and requirements.

One of the main benefits of structured wiring is its inherent network
capability. The frequency which the wires are capable of transmitting is often
referred to as the bandwidth. Category 3 (Cat-3) cable is rated up to 16MHz.
Category 5 (Cat-5) cable is more common in the UK and is rated to 100MHz. In a
new build Category 6 (Cat-6) wiring is now most likely to be used, as it
supports Gigabit Ethernet and bandwidths of over 500Mhz. It is ideal for
people who wish to install large or complex home automation systems and
transmit high-definition video around their home.

If you are considering home automation in a new house build, the question is
not whether you should install structured wiring but one of how much and of
what quality. The higher the quality of the cabling you use, the more superior
your system will be and the more future-proof it will be. You may not need all
of the capabilities that advanced cables can provide right away, but they
might be just what you want in 5 years time. Because it is very expensive to
upgrade your system retrospectively, your best bet is to think about your the
future today.


Cabling & Ducting
-----------------

The biggest challenge when retro-fitting home automation technology to an
existing home is in solving the connectivity issues. For this reason alone
many people use wireless technologies but, taking the time to add ducting and
cables will make things more reliable and provide better performance in the
long run. In a new build it is essential that ducts are provided to run cables
to all the necessary devices and sockets.

In existing homes, one approach to adding new, hidden wiring is to use a
combined skirting and ducting solution.


KNX
===

KNX is a standardized (EN 50090, ISO/IEC 14543), OSI-based network
communications protocol for intelligent buildings. KNX is the successor to,
and convergence of, three previous standards: the European Home Systems
Protocol (EHS), BatiBUS, and the European Installation Bus (EIB or Instabus).
The KNX standard is administered by the KNX Association.

More information
----------------

* http://en.wikipedia.org/wiki/KNX_%28standard%29


X10
===

X10 is an international and open standard for communication between electronic
devices used for home automation. It was pretty much the first such technology
on the market and is thus widely available and at mass-market prices.

The existing household electrical wiring (mains sockets and lighting) is used
to send digital data between X10 devices. The data is encoded onto a 120kHz
carrier which is transmitted as bursts during the zero crossing points of the
50 or 60Hz alternating current waveform. One bit is transmitted at each zero
crossing and the zero crossing is used to improve signal to noise ratios.

To allow the operation of wireless keypads, remote switches, etc., a radio
protocol is also defined. This operates at a frequency of 310MHz in the U.S.
and 433MHz in Europe. The wireless devices send data packets that are very
similar to ordinary X10 power line control packets. A radio receiver provides
a bridge which translates the radio packets into ordinary X10 power line
control packets.

X10 is at the cheaper end of the market when it comes to home automation but,
it does have its uses. It's also not as reliable as some of the later and more
expensive technologies. Aside from its price, it is fairly easy to
retrospectively fit into your existing home. One of the downsides to this
technology is the relatively low number of devices (16 per house, though you
can use more than one house code) that you can install in a single home.
Another disadvantage is that you cannot interogate the status of most X10
modules.
