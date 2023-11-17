#include "ros/ros.h"
#include <wiringPi.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>


#define LED 4


void controllerCallback(const std_msgs::String::ConstPtr& msg)
{
	ROS_INFO("Received rom topic: %s", msg->data.c_str());

}



/*
 * Main function
 **/
int main(int argc, char **argv)
{
	// Setup ROS stuff
	ros::init(argc, argv, "ti_project56_lidar_sensor");
	ROS_INFO_STREAM("[info]\tInit ROS");
	ros::NodeHandle node;

	// Setup WiringPi
	ROS_INFO_STREAM("[info]\tInit gpio");
	wiringPiSetupGpio();
	pinMode(LED, OUTPUT);

	// ros::spin();

	ROS_INFO_STREAM("[info]\tReady to run code");

	ros::Publisher pub = node.advertise<geometry_msgs::Twist>("/hoverboard_velocity_controller/cmd_vel", 10);
	
	ros::Rate loop_rate(10);


	while (ros::ok()) {
		geometry_msgs::Twist twist_cmd;
		twist_cmd.linear.x = 0.35;
		twist_cmd.linear.y = 0;
		twist_cmd.linear.z = 0;

		twist_cmd.angular.z = 0;

		pub.publish(twist_cmd);

	/*
	for  (int i = 0; i < 10; i++) {
		ROS_INFO_STREAM("yo mama 2");
		digitalWrite(LED, HIGH);
		delay(500);
		digitalWrite(LED, LOW);
		delay(500);
	}*/

	
	}
	return 0;
}
