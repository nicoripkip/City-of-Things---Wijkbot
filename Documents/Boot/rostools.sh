#!/bin/bash
sleep 5
source ~/Documents/Code/catkin_ws/devel/setup.sh

# Check if $DISPLAY is set
if [ -n "$DISPLAY" ]; then
    # If $DISPLAY is set, open xterm for each node
    sleep 1
    xterm -e rosrun ti_project56_robot_communicator ti_project56_robot_communicator_node.py &
    sleep 1
    xterm -e rosrun ti_project56_robot_calculator ti_project56_robot_calculator_node.py &
    sleep 1
    xterm -e rosrun ti_project56_robot_controller ti_project56_robot_controller_node.py &
else
    # If $DISPLAY is not set, start a tmux session for each node with xterm
    sleep 1
    tmux new-session -d -s communicator_session "rosrun ti_project56_robot_communicator ti_project56_robot_communicator_node.py"
    sleep 1
    tmux new-session -d -s calculator_session "rosrun ti_project56_robot_calculator ti_project56_robot_calculator_node.py"
    sleep 1
    tmux new-session -d -s controller_session "rosrun ti_project56_robot_controller ti_project56_robot_controller_node.py"
fi
sleep 5
source ~/Documents/Code/Compass/catkin_ws/devel/setup.sh

# Check if $DISPLAY is set
if [ -n "$DISPLAY" ]; then
    # If $DISPLAY is set, open xterm for the launch file
    xterm -e roslaunch i2c_imu i2c_imu_auto.launch &
else
    # If $DISPLAY is not set, start a tmux session for the launch file with xterm
    tmux new-session -d -s i2c_imu_session "roslaunch i2c_imu i2c_imu_auto.launch"
    sleep 1
    tmux new-session -d -s script "~/check.sh"
fi



