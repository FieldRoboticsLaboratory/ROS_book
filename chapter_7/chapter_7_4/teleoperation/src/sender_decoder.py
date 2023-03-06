#!/usr/bin/env python
# coding=utf-8 -*-
import serial
import rospy
import struct
import math
from geometry_msgs.msg import Twist
#from geometry_msgs.msg import Twist
#from std_msgs.msg import String


class Sender(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        rospy.loginfo("[%s] Initializing " %(self.node_name))

        #setup serial 初始化串口
        self.baud_rate = rospy.get_param("baud_rate",9600)    #115200
        self.port_name = rospy.get_param("port_name","/dev/ttyUSB0")   #lora_arduino
        self.ser = serial.Serial(self.port_name,self.baud_rate)

        # Subscriptions 订阅话题，获取转向信息
        self.sub_cmd_drive = rospy.Subscriber("/remote/cmd_vel",Twist,self.cb_twist,queue_size=1)
        

    #callback函数， 数据打包
    def cb_twist(self,msg):

        cmd = self.twist_to_str(msg)        
        self.ser.write(cmd)	
        
    def twist_to_str(self,twist):  
	
        pub_linear = int(100*twist.linear.x)
        pub_angular = int(25*twist.angular.z)

      
        
        cmd = bytearray(struct.pack("5b",0x48,
                                         0x47,
                                         pub_linear,
                                         pub_angular,
                                         0x55))
        for i in range(5):
          if i == 4:
	   print '%x'%cmd[i]
          else:
           print '%x'%cmd[i],

        #rospy.loginfo("data:%x" %(cmd.decode('hex')))
	cmd.append("\r")
        cmd.append("\n")
        return cmd

    def on_shutdown(self):
        
        rospy.loginfo("shutting down [%s]" %(self.node_name))


if __name__ == "__main__":
    rospy.init_node("lora_sender",anonymous=False)
    transmission = Sender()
    rospy.on_shutdown(transmission.on_shutdown)
    rospy.spin()
