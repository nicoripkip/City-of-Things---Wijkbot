#!/bin/bash

source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash

# If $DISPLAY is not set, start a tmux session for each node
tmux new-session -d -s hoverboard_session "source ~/catkin_ws/devel/setup.sh; roslaunch hoverboard_driver hoverboard.launch"

