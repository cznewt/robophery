
============
Introduction
============

This paper shows possible utilization of inexpensive Linux and MicroPython
compatible microcontrollers, hardware actuators and sensors to create fully
autonomous and isolated agent-based platform. This platform can perform wide
range automation use cases. These range from simple environmental automations,
surveillance, to complete ambient intelligence environments.

First chapter introduces global architecture of autonomous agents with
communication protocols for messages to the overlaying event driven controllers,
dashboards or any other services. These systems use scalable and modular
architecture to minimise the computational overhead which allows efficient use
of available hardware resources.

The next part covers the autonomous agents in more details. Models of hardware
interfaces and corresponding modules. It also covers description of the
virtual modules that provide the simple thresholds or fuzzy logic reasoning
for autonomous control.

The final chapter shows simple interaction with overlay control system that
can communicate with multiple autonomous systems, gather vital information and
even publish arbitrary actions on demand.

The control system contains time-series database, dashboard and reasoning
platform which can detect hardware malfunctions of autonomous agent systems
and perform necessary steps to repair it. With the usage of virtual models
that provide  high-level access to individual physical modules of individual
agents.
