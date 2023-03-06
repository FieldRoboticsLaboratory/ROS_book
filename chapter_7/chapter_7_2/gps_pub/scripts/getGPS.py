#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import cv2
import numpy as np
import message_filters
import math
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import PoseStamped,Pose,Quaternion,Point

#定义参数
frame_id = 0
RefCenterLon = 118.79232402 #lon    融合中心经度
RefCenterLat = 31.93936970  #lat    融合中心纬度
#发布话题，话题名称/gps/flat，数据类型为Point，队列长度为1
gps_pub = rospy.Publisher('/gps/flat',Point,queue_size=1)

#经纬度转换为大地坐标系下的坐标函数
def LatLonToXY(Lat, Lon):
	fi = Lat / 180 * math.pi
	la = (Lon - RefCenterLon)/180*math.pi
	zi = RefCenterLat/180*math.pi
	a = 6378137  #长半轴
	b = 6356752.3142    #短半轴
	c = 6399593.6258     #极点处子午线的曲率半径
	f = 1 / 298.257223563      #椭圆率
	E2 = 0.00669437999013      #第一偏心率的平方
	Eta2 = 0.00673949674227    #第二偏心率的平方
	V = math.sqrt(1+Eta2)
	N = c/V
	beta0 = 1.0 - 3.0 / 4.0 * E2 + 45.0 / 64.0 * E2 ** 2.0 - 175.0 / 256.0 * E2 ** 3 + 11025.0 / 16384.0 * E2 ** 4
	beta2 = beta0 - 1
	beta4 = 15.0 / 32.0 * E2 ** 2 - 175.0 / 384.0 * E2 ** 3 + 3675.0 / 8192.0 * E2 ** 4
	beta6 = -35.0 / 96.0 * E2 ** 3 + 735.0 / 2048.0 * E2 ** 4
	beta8 = 315.0 / 1024.0 * E2 ** 4
	Sz = c * (beta0 * zi + (beta2 * math.cos(zi) + beta4 * math.cos(zi) ** 3 + beta6 * math.cos(zi) ** 5 + beta8 * math.cos(zi) ** 7) * math.sin(zi))
	S = c * (beta0 * fi + (beta2 * math.cos(fi) + beta4 * math.cos(fi) ** 3 + beta6 * math.cos(fi) ** 5 + beta8 * math.cos(fi) ** 7) * math.sin(fi))
	X = S + la ** 2 * N / 2.0 * math.sin(fi) * math.cos(fi) + la ** 4 * N / 24.0 * math.sin(fi) * math.cos(fi) ** 3.0 * (5.0 - math.tan(fi) ** 2 +9.0 * Eta2 + 4 * Eta2 ** 2)+la ** 6 * N / 720.0 * math.sin(fi) * math.cos(fi) ** 5 * (61 - 58 * math.tan(fi) ** 2 + math.tan(fi) ** 4)
	Y = la * N * math.cos(fi) + la ** 3 * N / 6.0 * math.cos(fi) ** 3 * (1 - math.tan(fi) ** 2 + Eta2) + la ** 5 * N / 120.0 * math.cos(fi) ** 5 * (5 - 18 * math.tan(fi) ** 2 + math.tan(fi) ** 4)
	Z = Sz + la ** 2 * N / 2.0 * math.sin(zi) * math.cos(zi) + la ** 4 * N / 24.0 * math.sin(zi) * math.cos(zi) ** 3.0 * (5.0 - math.tan(zi) ** 2 +9.0 * Eta2 + 4 * Eta2 ** 2)+la ** 6 * N / 720.0 * math.sin(zi) * math.cos(zi) ** 5 * (61 - 58 * math.tan(zi) ** 2 + math.tan(zi) ** 4)
	X = X - Z
	return [Y,X] 

def callback(gps):
                global frame_id
    		#gps提供的经纬度数据转换为以度为单位的经纬度格式
    		gps_jingdu_1 = float(gps.longitude)/100
    		gps_weidu_1 = float(gps.latitude)/100  
    		gps_jingdu_2 = ((gps_jingdu_1 - math.floor(gps_jingdu_1))*100)/60  
    		gps_weidu_2 = ((gps_weidu_1 - math.floor(gps_weidu_1))*100)/60
    		gps_jingdu =  math.floor(gps_jingdu_1)+gps_jingdu_2
    		gps_weidu =  math.floor(gps_weidu_1)+gps_weidu_2
    		#经纬度转换为大地坐标系下的坐标
    		gps_x = LatLonToXY(gps_weidu,gps_jingdu)[1]
    		gps_y = LatLonToXY(gps_weidu,gps_jingdu)[0]
    		gps_msg=Point()
   		gps_msg.y = gps_x
    		gps_msg.x = gps_y
    		gps_pub.publish(gps_msg)

def gps_convert():
                #初始化节点
    		rospy.init_node('get_GPS', anonymous=True) 
    		#订阅话题/fix
    		gps_sub = message_filters.Subscriber('/fix',NavSatFix)  
   		ts = message_filters.ApproximateTimeSynchronizer([gps_sub], 10, 0.1)
   		ts.registerCallback(callback)
    		rospy.loginfo("gps data convert function successfully initialized!")
    		rospy.spin()

if __name__ == '__main__':
    		gps_convert()
                rospy.loginfo("data successfully saved!")
