#!/usr/bin/env python
# coding=utf-8 -*-

import rospy
import threading
import time
import math
import serial
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

cmd_pub = rospy.Publisher('/remote/cmd_vel',Twist,queue_size=1)
twist_msg = Twist()
global brake
brake = 0

global wheel_dir
wheel_dir = 1.0

global scale
scale = 1.0

##	global serial_str
##	serial_str = "0.0,0.0"

def pub_twist_thread():
    global brake
    while True:
	cmd_pub.publish(twist_msg)
        time.sleep(0.2)

'''	   	
def send_serial_thread():
    global ser
    global serial_str
    while True:
	ser.write(serial_str)
	# print(serial_str)
        time.sleep(0.1)
'''
def joy_cb(msg):
    global brake
    global wheel_dir
    global scale
 #   global serial_str

    if msg.buttons[18] == 1:
	wheel_dir = -1.0
	scale = 1.0
    else:
	wheel_dir = 1.0

    if msg.buttons[12] == 1:
	scale = 1.0
    elif msg.buttons[13] == 1:
	scale = 1.5
    elif msg.buttons[14] == 1:
	scale = 2.0
    elif msg.buttons[15] == 1:
	scale = 2.5
    elif msg.buttons[16] == 1:
	scale = 3.0
    elif msg.buttons[17] == 1:
	scale = 3.5

    if msg.buttons[12] == 0 and msg.buttons[13] == 0 and msg.buttons[14] == 0 and msg.buttons[15] == 0 and msg.buttons[16] == 0 and msg.buttons[17] == 0 and msg.buttons[18] == 0:
	scale = 0.0

    twist_msg.angular.z = msg.axes[0] * 4.0
    twist_msg.linear.x  = (msg.axes[2] + 1.0) * 0.25 * wheel_dir * scale

    if(msg.axes[3] > -0.95):
	brake = 1
    else:
	brake = 0

    if(brake == 1):
#	twist_msg.angular.z = 0.0
        twist_msg.linear.x  = 0.0

#   if(twist_msg.linear.x  == 0.0):
#	twist_msg.angular.z = 0.0

#    serial_str = str((int(twist_msg.linear.x * 1000)) / 1000.0) + "," + str((int(twist_msg.angular.z * 1000)) / 1000.0) + "\n"

def data_rev():
    rospy.init_node('joy_receiver', anonymous=True)
    joy_sub = rospy.Subscriber('/G29/joy', Joy, joy_cb)

    t_twist = threading.Thread(target=pub_twist_thread)
    t_twist.start()

    #t_serial = threading.Thread(target=send_serial_thread)
    #t_serial.start()

    rospy.spin()

if __name__ == '__main__':
    '''
    ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600)
    if not ser.isOpen():
        try:
            ser.open()
        except (OSError, serial.SerialException):
            print 'Warning: USB port is not exist!' 
    '''
    data_rev()

