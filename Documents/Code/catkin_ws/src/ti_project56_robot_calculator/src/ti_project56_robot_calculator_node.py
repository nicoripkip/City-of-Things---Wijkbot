#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
import json
import math
import numpy as np
import re

sensor_data = ""


# defines A 3D vector
robot_start_vector = [0, 0, 0]

controller_pub = None

magneto_x = 0
magneto_y = 0
magneto_z = 0
magneto_w = 0
ref_magneto_x = 0
ref_magneto_y = 0
ref_magneto_z = 0
DECLINATION_ANGLE = 2.3

magneto_direction = ""
magneto_position = 0

# north = 348.75 - 11.25
# nne = 11.25 - 33.75
# ne  = 33.75 - 56.25
# ene = 56.25 - 78.75
# East = 78.75 - 101.25
# ese = 101.25 - 123.75
# se = 123.75 - 146.25
# sse = 146.25 - 168.75
# South = 168.75 - 191.25
# ssw = 191.25 - 213.75
# sw = 213.75 - 236.25
# wsw = 236.25 - 258.75
# West = 258.75 - 281.25
# wnw = 281.25 - 303.75
# nw = 303.75 - 326.25
# nnw = 326.25 - 348.75



class Direction:
    def __init__(self):
        pass




def imu_callback(data):
    global magneto_x, magneto_y, magneto_z, magneto_w, magneto_direction, magneto_position

    magneto_x = data.orientation.x
    magneto_y = data.orientation.y
    magneto_z = data.orientation.z
    magneto_w = data.orientation.w

    magneto_dx = ref_magneto_x - magneto_x
    magneto_dy = ref_magneto_y - magneto_y
    magneto_dz = ref_magneto_z - magneto_z

        
    magneto_radians = math.atan2(magneto_y, magneto_x)
    magneto_degrees = math.degrees(magneto_radians)

    if magneto_degrees < 0:
        magneto_degrees = magneto_degrees + 360

    magneto_degrees = magneto_degrees + DECLINATION_ANGLE

    if magneto_degrees > 348.75 and magneto_degrees < 11.25:
        magneto_direction = "N"
    elif magneto_degrees > 11.25 and magneto_degrees < 33.75:
        magneto_direction = "NNE"
    elif magneto_degrees > 33.75 and magneto_degrees < 56.25:
        magneto_direction = "NE"
    elif magneto_degrees > 56.25 and magneto_degrees < 78.75:
        magneto_direction = "ENE"
    elif magneto_degrees > 78.75 and magneto_degrees < 101.25:
        magneto_direction = "E"
    elif magneto_degrees > 101.25 and magneto_degrees < 123.75:
        magneto_direction = "ESE"
    elif magneto_degrees > 123.75 and magneto_degrees < 146.25:
        magneto_direction = "SE"
    elif magneto_degrees > 146.25 and magneto_degrees < 168.75:
        magneto_direction = "SSE"
    elif magneto_degrees > 168.75 and magneto_degrees < 191.25:
        magneto_direction = "S"
    elif magneto_degrees > 191.25 and magneto_degrees < 213.75:
        magneto_direction = "SSW"
    elif magneto_degrees > 213.75 and magneto_degrees < 236.25:
        magneto_direction = "SW"
    elif magneto_degrees > 236.25 and magneto_degrees < 258.75:
        magneto_direction = "WSW"
    elif magneto_degrees > 258.75 and magneto_degrees < 281.25:
        magneto_direction = "W"
    elif magneto_degrees > 281.25 and magneto_degrees < 303.75:
        magneto_direction = "WNW"
    elif magneto_degrees > 303.75 and magneto_degrees < 326.25:
        magneto_direction = "NW"
    elif magneto_degrees > 326.25 and magneto_degrees < 348.75:
        magneto_direction = "NNW"
    
    magneto_position = magneto_degrees

    print("\n\nMagneto data:\n")
    print(f"X: {magneto_dx}")
    print(f"Y: {magneto_dy}")
    print(f"Z: {magneto_dz}")
    print(f"Degree: {magneto_degrees}")
    print(f"Richting: {magneto_direction}")


def rotate_position(position, angle):
    return np.dot(position, np.array([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ])) 


def degree_to_radian(degree):
    return degree * (math.pi / 180)


def radian_to_degree(radian):
    return radian * (180 / math.pi)


def xy_to_polar(x, y):
    return (
        math.sqrt(x**2 + y**2), 
        math.atan2(y, x)
    )


def polar_to_xy(data):
    return [
        data[0]*math.cos(data[1]), 
        data[0]*mah.sin(data[1])
    ]


def construct_point_cloud():
    global robot_start_vector
    pass


def construct_motor_data():
    pass


def calculator_callback(data):
    global sensor_data, controller_pub
    
    drive_direction = ""
    turn_direction = ""
    drive_speed = 0
    turn_speed = 0
        
    try:
        # Extract the actual string data from the ROS message
        json_string = data.data

        # Parse the JSON string directly
        sensor_data = json.loads(json_string)

        # Access individual sensor values
        sv = {
            "sonar1_value": int(re.findall(r'\b\d+\b', sensor_data.get("sonar1").get("distance"))[0]),
            "sonar2_value": int(re.findall(r'\b\d+\b', sensor_data.get("sonar2").get("distance"))[0]),
            "sonar3_value": int(re.findall(r'\b\d+\b', sensor_data.get("sonar3").get("distance"))[0]),
            "sonar4_value": int(re.findall(r'\b\d+\b', sensor_data.get("sonar4").get("distance"))[0]),
            "sonar5_value": int(re.findall(r'\b\d+\b', sensor_data.get("sonar5").get("distance"))[0])
        }
       
        print(f"Values: {sv}")

        # Do something with the values (print them in this example)
        # print(f"Sonar 1 value: {sonar1_value}")
        # print(f"Sonar 2 value: {sonar2_value}")
        # print(f"Sonar 3 value: {sonar3_value}")
        # print(f"Sonar 4 value: {sonar2_value}")
        # print(f"Sonar 5 value: {sonar3_value}")

        # Set threshold values for each sensor
        thresholds = {
            "sonar2": 600,
            "sonar3": 600,
            "sonar1": 600,
            "sonar4": 400,
            "sonar5": 400
        }

        # Check sonar sensors and take appropriate action
        for sensor, threshold in thresholds.items():
            current_sensor_value = sv[f"{sensor}_value"]
            
            print(f"current sensor value from sensor: {sensor} : {current_sensor_value}")

            rospy.loginfo(f"Current sensor value in loop: {current_sensor_value}")

            if current_sensor_value < threshold:
                if sensor == "sonar2":
                    drive_direction = "backward"
                    turn_direction = "left"

                    rospy.loginfo("Rij terug")
                elif sensor == "sonar3":
                    drive_direction = "forward"
                    turn_direction = "right"

                    rospy.loginfo("Rij naar rechts")
                elif sensor == "sonar1":
                    drive_direction = "forward"
                    turn_direction = "left"

                    rospy.loginfo("Rij naar links")                
                elif sensor == "sonar4":
                    drive_direction = "forward"
                    turn_direction = "right"

                    rospy.loginfo("Rij naar rechts")                
                elif sensor == "sonar5":
                    drive_direction = "forward"
                    turn_direction = "left"

                break
            else:
                drive_direction = "forward"
                turn_direction = "none"
        
        l = json.dumps({
            "drive": drive_direction,
            "turn": turn_direction,
            "drive_speed": 0.2,
            "turn_speed": 0.75
        }, indent=2)

        controller_pub.publish(l)

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")



def main():
    global controller_pub

    rospy.init_node("ti_project56_robot_calculator_node")
    rospy.loginfo("Robot calculator module loaded")
    
    rospy.Subscriber("/hoverboard/project56/calculator", String, calculator_callback)
    rospy.Subscriber("/imu/data", Imu, imu_callback)
    
    controller_pub = rospy.Publisher("/hoverboard/project56/controller", String, queue_size=10)

    rospy.spin()


if __name__ == "__main__":
    main()
