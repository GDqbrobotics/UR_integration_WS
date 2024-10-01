**Overview**

*control_loop.py* runs the main script, it uses a RTDE socket connection to send waypoints to the UR. It also subscribes to a mqtt topic. 
The project aim to create an interface between Vision (who pubs wp through mqtt) and UR (who listen to socket).

**Prerequisites**
- Python version at least 3.10.
- Paho lib for mqtt, you can install with ```pip3 install paho-mqtt```.
- An mqtt broker: for example mosquitto (```sudo apt install mosquitto```).

**Usage**

To test this project:

1) Powerup and release breaks of the UR.
2) TCP/IP connect PC to UR.
3) In script directory, run ```python control_loop.py```.
4) Run on UR the program **rtde_control_loop.urp**.
5) To fake vision commands, run ```python publisher.py```. It will send the pick targets read from *targets.txt*.

The integration of the vision system, other than calibration, needs to have a part of code that sends targets through mqtt as *publisher.py* does.