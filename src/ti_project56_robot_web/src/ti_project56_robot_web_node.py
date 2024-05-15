#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from bluepy.btle import Scanner, DefaultDelegate
import math



class BeaconScannerDelegate(DefaultDelegate):

    def __init__(self, beacon_publisher):
        DefaultDelegate.__init__(self)
        self.beacon_publisher = beacon_publisher

    def handleDiscovery(self, dev, isNewDev, isNewData):
        rssi_threshold = -75
        if isNewDev or isNewData:
            beacon_data = dev.getValueText(9)  # 9 is the index for the manufacturer data
            if beacon_data and "ROBOKAST_BEACON" in beacon_data:
                print(dev)
                if dev.rssi > rssi_threshold:
                    distance = estimate_distance(dev.rssi)
                    rospy.loginfo(f"Discovered device {dev.addr} with beacon data: {beacon_data}")
                    rospy.loginfo(f"Estimated distance: {distance:.2f} meters")
                    rospy.loginfo(f"Publishing beacon data: {beacon_data}")
                    self.beacon_publisher.publish(beacon_data + str(dev.rssi))
                else:
                    rospy.loginfo(f"Signal too weak!")
                    rospy.loginfo(dev.rssi)

                  
def estimate_distance(rssi):
    # You need to calibrate this function based on your specific hardware and environment
    # This is a simple example, and you may need to adjust it based on empirical data
    transmitted_power = -10  # Replace with the actual transmitted power of your BLE device
    frequency = 2400  # Replace with the actual frequency of your BLE device in megahertz

    path_loss = (transmitted_power - rssi) / (20 * math.log10(frequency) + 20 * math.log10(3e8))
    distance = math.pow(10, path_loss / 20)

    return distance

def main():
    rospy.init_node('beacon_detector', anonymous=True)

    beacon_topic = "/beacon_data"
    beacon_publisher = rospy.Publisher(beacon_topic, String, queue_size=10)

    scanner_delegate = BeaconScannerDelegate(beacon_publisher)
    scanner = Scanner().withDelegate(scanner_delegate)

    try:
        while not rospy.is_shutdown():
            devices = scanner.scan(0.1)  # Perform a single scan without waiting

            for dev in devices:
                pass

    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":
    main()
