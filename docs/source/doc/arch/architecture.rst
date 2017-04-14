
============
Architecture
============

RoboPhery consists of several objects. Communication objects handle sending
and receiving messages. Interface objects handle abstraction to hardware
communication at compute device level. Modules encapsulate individual hardware
sensors and actuators. Finally manager serves as central bus handling all
necessary communication within the service.


Autonomous Agent
================

Autonomous Agent is composed of Python daemon, which is communicating with
peripherals (mostly sensors) and sending and receiving data from external
communication sources.

The important parts of Autonomous Agent System are subsystems for Data
Persistence and Message Bus. Data Persistence subsystem is important, because
when data are collected from sensors, it is important to data will be
transfered and stored in correct state to the highest part of system, e.g. to
time-series database. Message Bus mainly take care about communication between
agent in Autonomous Agent System, because data can't be easily transfered from
sensor (agent) to database directly. Message Bus also can aggregate data to
bigger units or make some basic transformations.

Monitoring agents take care about conditions from sensors and values, which
are captured. There are predefined conditions and when captured values are
identical with same condition, monitoring agent send a message via message bus
to reacting agent, which will performs predefined action.

.. image :: /_static/img/arch/arch_unit.png
   :width: 50 %
   :align: center


System of Units
===============

On the following Figure, you can find these components and their cooperation
together. There are shown two main system - Autonomous Agent System and Cloud-
based Control System, where time-series is located database in some cloud
infrastructure.

.. image :: /_static/img/arch/arch_system.png
   :width: 50 %
   :align: center

Planning and reasoning agents are important for environment or values, where
entropy is involved. Planning agent provides future steps for autonomous
system based on past conditions or predefined conditions.

Reasoning agent examines future conditions on past conditions (captured data
in past). This agent looks for best conditions for future state of system and
for better reacting for captured data and contects in data are search for.


Sample Devices
==============

Following Figures shows simple device configurations.


RaspberryPi Device
------------------

.. image :: /_static/img/arch/detail_rpi.png
   :width: 50 %
   :align: center


ModeMCU Device
--------------

.. image :: /_static/img/arch/detail_mcu.png
   :width: 50 %
   :align: center
