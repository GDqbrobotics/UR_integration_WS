## Overview

This repo contains 2 ways to remotely control an Universal Robot E-series with low computational effort and just a TCP/IP connection:
- RTDE waypoint
- Interpreter Commands 

**Prerequisites**
- Python version at least 3.10.
- Paho lib for mqtt, you can install with ```pip3 install paho-mqtt```.
- An mqtt broker: for example mosquitto (```sudo apt install mosquitto```).

## RTDE waypoint 

With this method the task runs on an *.urp* script on Polyscope, while the PC just gives the target waypoint and some flags to syncronize. On PC side *control_loop.py* runs the main script, it uses a RTDE socket connection to send data to the UR. It also subscribes to a mqtt topic. 
The project aim to create an interface between Vision (who pubs wp through mqtt) and UR (who listen to socket).

**Usage**

To test this project:

1) Powerup and release breaks of the UR.
2) TCP/IP connect PC to UR.
3) In script directory, run ```python control_loop.py```.
4) Run on UR the program **rtde_control_loop.urp**.
5) To fake vision commands, run ```python publisher.py```. It will send the pick targets read from *targets.txt*.

The integration of the vision system, other than calibration, needs to have a part of code that sends targets through mqtt as *publisher.py* does.

## Interpreter Commands 

With this method the PC sends the commands to Polyscope, while on the UR runs an *.urp* script that makes it ready to receive commands. On PC side *commanding_Interp.py* runs the main script, it reads the commands of the task in a txt file and it can execute trajectories of several points (at the moment it just reads them from another txt file). It also subscribes to a mqtt topic. 
This way could be more suited for integration scenarios where the tool has to follow some external calculated trajectory...

**Usage**

To test this project:

1) Powerup the UR (you should have the **interpreter.urp** script inside */programs/RemoteOperation/* dir).
2) TCP/IP connect PC to UR.
3) In script directory, run ```python commanding_Interp.py```.
4) Enter commands from keyboards (or read them from commands.txt, depends on the code...)
5) To fake vision commands, run ```python publisher.py```. It will send the pick targets read from *targets.txt*.

The integration of the vision system, other than calibration, needs to have a part of code that sends targets through mqtt as *publisher.py* does.

