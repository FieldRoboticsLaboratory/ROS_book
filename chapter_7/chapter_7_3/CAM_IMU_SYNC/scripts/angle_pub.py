#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from geometry_msgs.msg import PoseStamped
data_z = 0.0

def angle_publisher():
	# ROS节点初始化
	rospy.init_node('angle_publisher', anonymous=True)
	#发布话题，话题名为/imu/angle，类型为PoseStamped，队列长度为10
	angle_pub = rospy.Publisher('/imu/angle', PoseStamped, queue_size=10)
	#设置循环的频率
	rate = rospy.Rate(100) 

	while not rospy.is_shutdown(): 
		global data_z
		angle = PoseStamped()
		angle.header.frame_id="angle"  
		angle.header.stamp=rospy.Time.now() 
		data_z += 0.01       
		angle.pose.position.z = data_z
		# 发布消息
		angle_pub.publish(angle)
		rospy.loginfo("Publsh angle %0.2f deg", angle.pose.position.z)
		# 按照循环频率延时
		rate.sleep()

if __name__ == '__main__':
	try:
		angle_publisher()
	except rospy.ROSInterruptException:
	        pass
