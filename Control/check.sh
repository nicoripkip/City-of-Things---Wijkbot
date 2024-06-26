#!/bin/bash

start_nodes_and_launch() {
    # Check if the communicator_session tmux session exists
    if ! tmux has-session -t communicator_session 2>/dev/null; then
        # If the session does not exist, start a new tmux session for the communicator node
        tmux new-session -d -s communicator_session "source ~/catkin_ws/devel/setup.sh;rosrun ti_project56_robot_communicator ti_project56_robot_communicator_node.py"
        echo "Started communicator_session"
    fi

    # Check if the calculator_session tmux session exists
    if ! tmux has-session -t calculator_session 2>/dev/null; then
        # If the session does not exist, start a new tmux session for the calculator node
        tmux new-session -d -s calculator_session "source ~/catkin_ws/devel/setup.sh;rosrun ti_project56_robot_calculator ti_project56_robot_calculator_node.py"
        echo "Started calculator_session"
    fi

    # Check if the controller_session tmux session exists
    if ! tmux has-session -t controller_session 2>/dev/null; then
        # If the session does not exist, start a new tmux session for the controller node
        tmux new-session -d -s controller_session "source ~/catkin_ws/devel/setup.sh; rosrun ti_project56_robot_controller ti_project56_robot_controller_node.py"
        echo "Started controller_session"
    fi

    # Check if the hoverboard_session tmux session exists
    if ! tmux has-session -t hoverboard_session 2>/dev/null; then
        # If the session does not exist, start a new tmux session for the hoverboard launch file
       	tmux kill-session -t communicator_session
	tmux kill-session -t calculator_session
	tmux kill-session -t controller_session
	tmux new-session -d -s hoverboard_session "source ~/catkin_ws/devel/setup.sh; roslaunch hoverboard_driver hoverboard.launch"
        echo "Started hoverboard_session"
    fi

    # Check if the i2c_imu_session tmux session exists
    # if ! tmux has-session -t i2c_imu_session 2>/dev/null; then
        # If the session does not exist, start a new tmux session for the i2c_imu launch file
    #    tmux new-session -d -s i2c_imu_session "roslaunch i2c_imu i2c_imu_auto.launch"
    #    echo "Started i2c_imu_session"
    # fi
}


# Run the loop every 10 seconds
while true; do
    # Start the nodes and i2c_imu launch file
    start_nodes_and_launch

    # Sleep for 10 seconds
    sleep 1

    # Check if the stop file exists
    if [ -e stop_script.txt ]; then
        echo "Stopping the script."
        break
    fi
done

# Remove the stop file if it exists
[ -e stop_script.txt ] && rm stop_script.txt

