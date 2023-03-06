/**
 * 将发布ff_target话题，消息类型g29_force_feedback::ForceFeedback
 */
 
#include <ros/ros.h>
#include <teleoperation/ForceFeedback.h>

int main(int argc, char **argv)
{
	// ROS节点初始化
	ros::init(argc, argv, "g29_ff_pub");

	// 创建节点句柄
	ros::NodeHandle n;

	// 创建一个Publisher，发布名为/turtle1/cmd_vel的topic，消息类型为geometry_msgs::Twist，队列长度10
	ros::Publisher g29ff_pub = n.advertise<teleoperation::ForceFeedback>("/ff_target", 1);

	// 设置循环的频率
	ros::Rate loop_rate(100);

	int count = 0;

        // 初始化g29_force_feedback::ForceFeedback类型的消息
		teleoperation::ForceFeedback g29ff_msg;
		g29ff_msg.angle = 0.8;
		g29ff_msg.force = 0.4;
       		g29ff_msg.pid_mode = false;


	while (ros::ok())
	{
	    g29ff_msg.angle = -g29ff_msg.angle;
	    // 发布消息
		g29ff_pub.publish(g29ff_msg);
		ROS_INFO("Publsh g29_force_feedback command[%0.2f m/s, %0.2f rad/s,%]", 
				g29ff_msg.angle, g29ff_msg.force);

	    // 按照循环频率延时
	    loop_rate.sleep();
	}

	return 0;
}
