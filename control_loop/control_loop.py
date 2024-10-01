#!/usr/bin/env python

# Software License Agreement: BSD 3-Clause License
#
# Copyright (c) 2016-2024, qbrobotics®
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the
#   following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#   products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys
sys.path.append('..')
import logging

import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
import threading
import time

import mqtt.subscriber as mqtt_sub
#logging.basicConfig(level=logging.INFO)

ROBOT_HOST = '192.168.1.96'
ROBOT_PORT = 30004
config_filename = 'control_loop_configuration.xml'

keep_running = True

logging.getLogger().setLevel(logging.INFO)

conf = rtde_config.ConfigFile(config_filename)
state_names, state_types = conf.get_recipe('state')
setp_names, setp_types = conf.get_recipe('setp')
watchdog_names, watchdog_types = conf.get_recipe('watchdog')
new_target_found_names, new_target_found_types = conf.get_recipe('new_target_found')


con = rtde.RTDE(ROBOT_HOST, ROBOT_PORT)
con.connect()

# get controller version
con.get_controller_version()

# setup recipes
con.send_output_setup(state_names, state_types)
setp = con.send_input_setup(setp_names, setp_types)
watchdog = con.send_input_setup(watchdog_names, watchdog_types)
new_target_found = con.send_input_setup(new_target_found_names, new_target_found_types)

# Setpoint to move the robot to
new_setp = [0, -0.3, 0.3, 0, 3.14, 0] #a quite safe position vector, this should never be used but who knows...

setp.input_double_register_0 = 0
setp.input_double_register_1 = 0
setp.input_double_register_2 = 0
setp.input_double_register_3 = 0
setp.input_double_register_4 = 0
setp.input_double_register_5 = 0

sub = mqtt_sub.MQTT_SUB()

# The function "rtde_set_watchdog" in the "rtde_control_loop.urp" creates a 1 Hz watchdog
watchdog.input_int_register_0 = 0

def watchdog_thread(con_,watchdog_):
    while True:
        time.sleep(0.3)
        # kick watchdog
        try:
            con_.send(watchdog_)
        except:
            print("handshake lost...")

def subscriber_thread(sub_):
    sub.run()

def setp_to_list(setp):
    list = []
    for i in range(0,6):
        list.append(setp.__dict__["input_double_register_%i" % i])
    return list

def list_to_setp(setp, list):
    for i in range (0,6):
        setp.__dict__["input_double_register_%i" % i] = list[i]
    return setp

#start data synchronization
if not con.send_start():
    sys.exit()

#Starting threads
th1 = threading.Thread(target=watchdog_thread, args=(con,watchdog),daemon = True )
th1.start()

th2 = threading.Thread(target=subscriber_thread, args=(sub,),daemon = True )
th2.start()

# control loop
while keep_running:
    # receive the current state
    state = con.receive()
    time.sleep(0.3)

    new_target_found.input_int_register_1 = 0
    con.send(new_target_found)
    
    if state is None:
        break

    # Sends to UR the position received by mqtt publisher
    if state.output_int_register_0 != 0 and sub.received_msg:
        new_setp = sub.stored_position
        list_to_setp(setp, new_setp)
        print('Sending Pose '+ str(new_setp))
        con.send(setp)

        new_target_found.input_int_register_1 = 1   
        con.send(new_target_found)

        sub.reset_received_msg()

con.send_pause()

con.disconnect()
