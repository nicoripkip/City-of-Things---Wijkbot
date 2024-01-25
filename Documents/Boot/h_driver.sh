#!/bin/bash

source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash

# Check if $DISPLAY is set
if [ -n "$DISPLAY" ]; then
    # If $DISPLAY is set, open xterm for each node
    xterm -e roslaunch hoverboard_driver hoverboard.launch &
else
    # If $DISPLAY is not set, start a tmux session for each node
    tmux new-session -d -s hoverboard_session "roslaunch hoverboard_driver hoverboard.launch"
fi

