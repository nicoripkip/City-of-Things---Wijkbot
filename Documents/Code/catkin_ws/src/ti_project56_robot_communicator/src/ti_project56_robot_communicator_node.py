#!/usr/bin/env python3


import rospy
from std_msgs.msg import String
import smbus
import time
import json


Q_SIZE = 10
PUB_FREQ = 10
START_REG = 0x00
I2C_CHUNK_LIMIT = 32
I2C_SLAVE_FRONT = 0x04
I2C_SLAVE_BACK = 0x05


def send_data_to_i2c(bus, slave, buff: str):
    """
    Functie om data naar een slave te sturen die
    verbonden is met i2c
    """
    try:
        # Converteer de buffer naar een buffer die alleen maar ascii values bevat
        ascii_buff = [ord(char) for char in buff]
            
        for value in ascii_buff:
            bus.write_byte(slave, value)

    except Exception as e:
        print(f"error: {e}")


def receive_data_from_i2c(bus, slave):
    """
    Functie om data van de i2c lijn uit te lezen
    """
    buf = ""  # Initialize with an empty string

    try:
        bus.write_byte(slave, 0x01)
        length = bus.read_byte(slave)

        rest = length - 32

        received_bytes = bus.read_i2c_block_data(slave, START_REG, length)

        # Filter out non-printable ASCII characters
        printable_chars = [chr(value) for value in received_bytes if 32 <= value <= 126]
        buf = "".join(printable_chars)
    
        rospy.loginfo(f"Buffer data: {buf}")

    except Exception as e:
        print(f"error: {e}")
    if len(buf.split(",")) < 5:
        buf = ""

    return buf


def convert_data_to_json(data):
    d = data.split(",")
    print(len(d))
    if len(d) > 4:
        l = {
            "sonar1": {
                "distance": d[0],
                "angle": 0.00, 
            },
            "sonar2": {
                "distance": d[1],
                "angle": 0.00,
            },
            "sonar3": {
                "distance": d[2],
                "angle": 0.00,
            },
            "sonar4": {
                "distance": d[3],
                "angle": 0.00,
            },
            "sonar5": {
                "distance": d[4],
                "angle": 0.00,        
            }
        }
    return json.dumps(l, indent=2)


def publish_to_topic(pub, rate, data):
    pub.publish(data)


def main():
    rospy.init_node("ti_project56_robot_communicator_node")
    rospy.loginfo("Robot communicator module loaded")
   
    # init 
    bus = smbus.SMBus(1)
    pub = rospy.Publisher("/hoverboard/project56/calculator", String, queue_size=Q_SIZE)
    rate = rospy.Rate(PUB_FREQ)

    while not rospy.is_shutdown():
        b = receive_data_from_i2c(bus, I2C_SLAVE_FRONT)
        
        try:
            if b != "":
                rospy.loginfo(convert_data_to_json(b))
                publish_to_topic(pub, rate, convert_data_to_json(b))
                rate.sleep()

        except rospy.ROSInterruptException as e:
            print(f"error: {e}")

        # rospy.loginfo(f"Received from i2c: {b}")



if __name__ == "__main__":
    main()
