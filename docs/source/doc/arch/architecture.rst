
============
Architecture
============

RoboPhery project provides software drivers for a wide variety of commonly
used sensors and actuators through both wired and wireless interfaces.
Platform is designed for multiple interfaces to be stacked (GPIO or I2C over
IQRF or BlueTooth) to provide seamless intergration with vast variery of
hardware platforms. The software drivers interact with the underlying hardware
platform (or microcontroller), as well as with the attached sensors, through
API calls to attached interfaces.

The actuators are controlled and the data is collected and this together forms
a hardware foundation for ambient intelligence environment. The event-driven
control system, data storage and data processing systems are provided in form
of external cloud services or handled by computer with more processing power.

.. Arribas-Ayllon, Michael. "Ambient Intelligence: an innovation narrative".
.. Aarts, Emile H. L.; Encarnação, José Luis (13 December 2006). "True Visions: The Emergence of Ambient Intelligence". Springer – via Google Books.
.. "The Internet of Things and Convenience (PDF Download Available)".
.. "Ambient Intelligence Knowledge Center .: SemiEngineering.com".


Ambient intelligence environments that are those that are sensitive and
responsive to the presence of people. A typical example of ambient
intelligence environment is a Home environment [1]. Term Ambient intelligence
as a vision of the future of consumer electronics and computing was originally
pointed by Eli Zelkha at Palo Alto Ventures in the late 1990s. The time frame
set for this vision was 2010–2020.[1][2][3][4]

In an ambient intelligence world, devices work together to support people in
their everyday life activities, tasks and rituals in a natural way that uses
information from physical environment collected by network connected devices
and uses cloud power to drive the intelligence that can react and learn to the
information coming from the environment.

The physical devices steadily grow smaller and are more integrated into our
environment, the technology used disappears until only the user interface
remains visible to the users.

.. (Bieliková & Krajcovic 2001)

.. Emile Aarts, Rick Harwig and Martin Schuurmans, chapter Ambient Intelligence in The Invisible Future: The Seamless Integration Of Technology Into Everyday Life, McGraw-Hill Companies, 2001

The ambient intelligence paradigm builds upon pervasive computing, ubiquitous
computing, profiling, context awareness, and human-centric computer
interaction design and is characterized by systems and technologies that are
(Zelkha et al. 1998; Aarts, Harwig & Schuurmans 2001):

Embedded
  Many networked devices are integrated into the environment

Context aware
  These devices can recognize you and your situational context

Personalized
  They can be tailored to your needs

Adaptive
  They can change in response to you

Anticipatory
  They can anticipate your desires without conscious mediation.

.. Bieliková, Mária; Krajcovic, Tibor (2001), "Ambient Intelligence within a Home Environment", ERCIM News (published October 2001) (47)

The basic architecture setup consists of time-series database, user dashboard
and event-driven control engine. This setup can be further expanded by
machine learning services. Actual RoboPhery application is writtern in Python
code compatible with MicroPython used on less expensive microcontrollers.


Ambient Inteligence System
==========================

On the following Figure, you can see components of our proposed ambient
intelligence system and their relationships. The central component is the
message bus, in our case provided by MQTT broker.

.. image :: /_static/img/arch/arch_system.png
   :width: 50 %
   :align: center

The event driven automation plays key role in controlling the behavior of the
system, the inner conditions are altered by machine-learning algorithms that
can provide better values to get the best outcome where entropy is involved.
Virtual models can provide future models for autonomous decisions based on
past conditions or predefined conditions. This mechanism is used control the
autonomous agent if communication bus is broken.


Communication Bus
-----------------

MQTT is a machine-to-machine connectivity protocol in area of "Internet of
Things". It was designed as an extremely lightweight publish/subscribe
messaging transport. It is useful for connections with remote locations where
a small code footprint is required and/or network bandwidth is low. MQTT
broker can handle thousands of messages per second, supports high-availability
setups for both high performance and stability. Individual Autonomous agents
and cloud-based Control system along with time-series databases are connected
to this common message bus.

.. http://www.redbooks.ibm.com/abstracts/sg248054.html


Event-driven Controller
-----------------------

.. https://en.wikipedia.org/wiki/Event-driven_architecture

Event-driven architecture (EDA), also known as message-driven architectures,
is a software architecture pattern promoting the production, detection,
consumption of, and reaction to events.

.. K. Mani Chandy Event-Driven Applications: Costs, Benefits and Design Approaches, California Institute of Technology, 2006 [1]

An event can be defined as `a significant change in state`[1]. For example,
when a user turn's on a switch, the swith'es state changes from "off" to
"on". A car dealer's system architecture may treat this state change as an
event whose occurrence can be made known to other applications within the
architecture. From a formal perspective, what is produced, published,
propagated, detected or consumed is a (typically asynchronous) message called
the event notification, and not the event itself, which is the state change
that triggered the message emission. Events do not travel, they just occur.
However, the term event is often used metonymically to denote the notification
message itself, which may lead to some confusion.


Time-series Database
--------------------

.. https://en.wikipedia.org/wiki/Time_series_database

A time series database (TSDB) is optimized for handling time series data
storage and retrieval, arrays of numbers indexed by time (a datetime or a
datetime range). In some fields these time series are called profiles, curves,
or traces. A time series of stock prices might be called a price curve. A time
series of energy consumption might be called a load profile. A log of

Despite the disparate names, many of the same mathematical operations,
queries, or database transactions are useful for analysing all of them. The
implementation of a database that can correctly, reliably, and efficiently
implement these operations must be specialized for time-series data.

TSDBs are databases that are optimized for time series data. Software with
complex logic or business rules and high transaction volume for time series
data may not be practical with traditional relational database management
systems. Flat file databases are not a viable option either, if the data and
transaction volume reaches a maximum threshold determined by the capacity of
individual servers (processing power and storage capacity). Queries for
historical data, replete with time ranges and roll ups and arbitrary time zone
conversions are difficult in a relational database. Compositions of those
rules are even more difficult. This is a problem compounded by the free nature
of relational systems themselves. Many relational systems are often not
modelled correctly with respect to time series data. TSDBs on the other hand
impose a model and this allows them to provide more features for doing so.


Autonomous Units
================

Autonomous unit is Python service, which communicates with hardware
peripherals and sending and receiving data from external communication
sources. RoboPhery unit consists of several objects. Communication objects
handle sending and receiving messages from the upper layer services or other
autonomous units. Interface objects handle abstraction to hardware
communication at device level. Modules encapsulate individual hardware sensors
and actuators. Finally the robophery manager serves as central service that
connects all other models within the autonomous unit.

When data are collected from sensors, it is important to data will be
transfered and stored in correct state to the highest part of system, e.g. to
time-series database. 

Message Bus mainly take care about communication between agent in Autonomous
Agent System, because data can't be easily transfered from sensor (agent) to
database directly. Message Bus also can aggregate data to bigger units or make
some basic transformations.

Autonomous services take care about conditions from sensors and values, which
are captured. There are predefined conditions and when captured values are
identical with same condition, monitoring agent send a message via message bus
to reacting agent, which will performs predefined action.

.. image :: /_static/img/arch/arch_unit.png
   :width: 50 %
   :align: center


Sample Devices
==============

Following Figures shows simple device configurations.


Raspberry Pi Device
-------------------

Following figure shows RoboPhery service running on the Raspberry Pi device
with MCP23008 I2C to GPIO expander and multiple sensors connected to
individual interfaces.

.. image :: /_static/img/arch/detail_rpi.png
   :width: 50 %
   :align: center


ModeMCU Device
--------------

Following figure shows RoboPhery service running on the Mode MCU device with
multiple sensors connected to interfaces present on the device.

.. image :: /_static/img/arch/detail_mcu.png
   :width: 50 %
   :align: center


IQRF Platform
--------------

Following figure shows RoboPhery service running on the Raspberry Pi device
with IQRF coordinator with sensor interfacess connected through a mesh network
and IQRF interface.

.. image :: /_static/img/arch/detail_iqrf.png
   :width: 50 %
   :align: center
