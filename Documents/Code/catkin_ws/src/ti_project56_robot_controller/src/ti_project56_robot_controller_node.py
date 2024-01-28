#!/usr/bin/env python3

import rospy
import json
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import re

URL = "ws://85.215.71.71:8765"
MAX_QUEUE_SIZE = 10
DEFAULT_SPEED = 0.4
TURN_SPEED = 0.2

sonar1_value = 0
sonar2_value = 0
sonar3_value = 0
sonar4_value = 0
sonar5_value = 0

def controller_callback(data):
    global sonar1_value, sonar2_value, sonar3_value, sonar4_value, sonar5_value

    try:
        json_data = json.loads(data.data)

        # Clean up sensor names and convert to float
        drive_direction = json_data.get("drive")
        turn_direction = json_data.get("turn")

        # Check sonar sensors and take appropriate action
        if drive_direction == "forward" and turn_direction == "none":
            move_forward()
        elif drive_direction == "forward" and turn_direction == "left":
            turn_left()
        elif drive_direction == "forward" and turn_direction == "right":
            turn_right()
        elif drive_direction == "stop":
            stop_wheels()
        else:
            move_backward()
        
    except json.JSONDecodeError as e:
        rospy.logerr("Error decoding JSON data: %s", str(e))



def clean_sensor_name(sensor_name):
    # Remove non-alphanumeric characters
    cleaned_name = re.sub(r'[^a-zA-Z0-9]', '', sensor_name)
    return cleaned_name


def to_int(value):
    # Convert to float, handling potential decimal parts
    try:
        return int(value)
    except ValueError:
        rospy.logwarn("Unable to convert '%s' to float. Setting to 0.", value)
        return 0.0

def turn_left():
    rospy.loginfo("Turning left")

    move_msg.linear.x = 0
    vel_pub.publish(move_msg)

    move_msg.angular.z = TURN_SPEED  # Set angular velocity for turning left
    vel_pub.publish(move_msg)
    #rospy.sleep(turn_duration)

def turn_right():
    rospy.loginfo("Turning right")

    move_msg.linear.x = 0
    vel_pub.publish(move_msg)

    move_msg.angular.z = -TURN_SPEED  # Set angular velocity for turning right
    vel_pub.publish(move_msg)
    #rospy.sleep(turn_duration)

def move_forward():

    move_msg.angular.z = 0
    vel_pub.publish(move_msg)

    move_msg.linear.x = DEFAULT_SPEED
    vel_pub.publish(move_msg)


def move_backward():
    move_msg.linear.x = -DEFAULT_SPEED
    move_msg.angular.z = 0.4

    vel_pub.publish(move_msg)

def stop_wheels():

    move_msg.angular.z = 0
    vel_pub.publish(move_msg)

    move_msg.linear.x = 0
    vel_pub.publish(move_msg)


def main():
    global move_msg, vel_pub

    rospy.init_node("controller_node", anonymous=True)
    rospy.loginfo("Main node started")

    vel_pub = rospy.Publisher("/hoverboard_velocity_controller/cmd_vel", Twist, queue_size=MAX_QUEUE_SIZE)

    rospy.Subscriber("/hoverboard/project56/controller", String, controller_callback)
    # rospy.Subscriber("/hoverboard/project56/calculator", String, calculator_callback)

    move_msg = Twist()

    while not rospy.is_shutdown():
        rospy.sleep(0.1)  # Adjust the sleep duration if needed

    rospy.spin()


if __name__ == "__main__":
    main()
