#!/usr/bin/python3

import logging
import time
import sys
sys.path.append('..')

from interpreter.interpreter import InterpreterHelper

# num of commands after which clear_interpreter() command will be invoked.
# If interpreted statements are not cleared periodically then "runtime too much behind" error may
# be shown when leaving interpreter mode
CLEARBUFFER_LIMIT = 500

# logging.basicConfig(level=logging.INFO)

def execute_line(intrp,line,command_count):
    command_id = intrp.execute_command(line)
    if command_count % CLEARBUFFER_LIMIT == 0:
        # logging.info(f"{command_count} commands sent. Waiting for all commands to be executed before clear.")
        # Wait for interpreted commands to be executed. New commands will be discarded if interpreter buffer
        # limit is exceeded.
        while intrp.get_last_executed_id() != command_id:
            # logging.info(f"Last executed id {intrp.get_last_executed_id()}/{command_id}")
            time.sleep(2)

        # Manual buffer clear is necessary when large amount of statements is sent in one interpreter mode session.
        # By default statements are cleared when leaving interpreter mode.
        # Look at CLEARBUFFER_LIMIT comment for more info.
        # logging.info("Clearing all interpreted statements")
        intrp.clear()
    command_count += 1

def send_cmd_interpreter_mode_mqtt(intrp,trajFile,commFile,sub):
    f = open(trajFile, "r")
    F = open(commFile, "r")

    trajectory_points = f.readlines()
    commandLines = F.readlines()

    command_count = 1

    points_index = 0
    file_lines_index = 0

    executing_traj = False
    executing_file = False
    line = ''

    while True:

        if(not executing_traj):
            if not executing_file:
                line = input("Enter Command to execute: ")
            else:
                line = commandLines[file_lines_index].rstrip()
                file_lines_index += 1
                if file_lines_index == len(commandLines):
                    file_lines_index = 0
                    #executing_file = False

            match str(line):
                case "EXE":
                    executing_traj = True
                    point_index = 0
                    continue

                case "CLOSE":
                    line = "qbdevice.setClawCommand(6500,0)"

                case "OPEN":
                    line = "qbdevice.setClawCommand(4200,4000)"

                case "WAIT TARGET":
                    while not sub.received_msg:
                        time.sleep(0.01)
                    sub.reset_received_msg()
                    approach_stored_position = sub.stored_position.copy()
                    approach_stored_position[2] += 0.08 #approach 7cm above the target 
                    line = "movel(p" + str(approach_stored_position) + ", a=1.2, v=0.25, r=0.0)"
                    execute_line(intrp,line,command_count)
                    line = "movel(p" + str(sub.stored_position) + ", a=0.1, v=0.1, r=0.0)"
                    execute_line(intrp,line,command_count)
                    if sub.action == 'Pick':
                        line = "qbdevice.setClawCommand(6500,0)"
                        execute_line(intrp,line,command_count)
                        line = "sleep(1.5)"
                        execute_line(intrp,line,command_count)
                    else:
                        if sub.action == 'Place':
                            line = "qbdevice.setClawCommand(4200,4000)"
                            execute_line(intrp,line,command_count)
                            line = "sleep(1.0)"
                            execute_line(intrp,line,command_count)
                            # Here we have to know the center of the jar
                            approach_stored_position[0] = 0.08 #jar x
                            approach_stored_position[1] = -0.5 #jar y
                    line = "movel(p" + str(approach_stored_position) + ", a=1.2, v=0.25, r=0.0)"

                case "RUN FILE":
                    if not executing_file:
                        file_lines_index = 0 #RUN FILE command not allowed inside file, it would create infinite loop
                    executing_file = True
                    continue

        else:
            line = "movel(" + trajectory_points[point_index].rstrip() + ", a=0.05, v=0.1, r=0.0)"
            # time.sleep(0.1)
            point_index = point_index + 1
            if point_index == len(trajectory_points):
                executing_traj = False
                point_index = 0

        execute_line(intrp,line,command_count)    
