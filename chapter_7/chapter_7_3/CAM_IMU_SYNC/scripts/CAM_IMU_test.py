#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import cv2
import numpy as np
import message_filters
import os
from os.path import join
from sensor_msgs.msg import Image
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge, CvBridgeError

#初始化参数
frame_id = 0
gps_id=0
#设置保存路径，nuaa-frl为本机用户名，读者需自行修改
path = "/home/nuaa-frl/Dataset/"    
img_path = "/home/nuaa-frl/Dataset/imgs"
bridge = CvBridge()
flag=True
global path_file
path_file = '/home/nuaa-frl/temp'
#定义同步回调函数
def callback(angle, image):
	if flag==True:
		rospy.loginfo("data recieved!")
	global frame_id
	global bridge
	imu_yaw = angle.pose.position.z

	#创建data.txt，保存imu角度数据
	data = "{} {}\n".format(frame_id, imu_yaw)
	pose_file = open(join(path, 'data.txt'), 'a')
	pose_file.writelines(data)
	pose_file.close()
	#保存图片
	down_img = bridge.imgmsg_to_cv2(image)
	image_name = join(img_path, str(frame_id)+".jpg")
	cv2.imwrite(image_name, down_img)
	frame_id += 1
	rospy.loginfo("data recorded!")

def listener():
	#初始化节点
	rospy.init_node('listener', anonymous=True)
	time = rospy.Time().now()
	#订阅/imu/angle话题
	angle_sub = message_filters.Subscriber('/imu/angle', PoseStamped)
	#订阅/usb_cam/image_raw话题
	image_sub = message_filters.Subscriber('/usb_cam/image_raw', Image)
	#如果两个话题的时间戳相差在0.1s之内则认为时间戳已经对齐
	ts = message_filters.ApproximateTimeSynchronizer([angle_sub,image_sub], 1000, 0.1)
	ts.registerCallback(callback)
	rospy.loginfo("successfully initialized!")
	rospy.spin()

if __name__ == '__main__':
	global path_file
	#清空存放图片的文件夹
	for i in os.listdir(img_path):  # os.listdir()返回一个列表，包含有指定路径下的目录和文件的名称
		path_file = os.path.join(img_path,i)  # os.path.join() 用于路径拼接文件路径
	if os.path.isfile(path_file):   # os.path.isfile ()判断某一对象(需提供绝对路径)是否为文件
		os.remove(path_file)   # os.remove()删除指定路径的文件
	else:
		for f in os.listdir(path_file):
			path_file2 =os.path.join(path_file,f)
			if os.path.isfile(path_file2):
				os.remove(path_file2)
				#清空（创建）txt
	with open(join(path, 'data.txt'), 'a') as f:   #打开data.txt，如果该文件已存在，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入
		f.seek(0)    #从文件开头读取文件
		f.truncate()  #截断文件
	listener()
	rospy.loginfo("data successfully saved!")

