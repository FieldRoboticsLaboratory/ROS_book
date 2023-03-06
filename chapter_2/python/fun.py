#! /usr/bin/env python
# -*- coding: utf-8 -*-
def forward():
	print "Robot moving forward"
def backward():
	print "Robot moving backward"
def left():
	print "Robot moving left"
def right():
	print "Robot moving right"
def main():
	'''
		This the main function!
	'''
	robot_command = raw_input("Enter the command:> ")
	if (robot_command == "move_forward"):
		forward()
	elif (robot_command == "move_backward"):
		backward()
	elif (robot_command == "move_left"):
		left()
	elif (robot_command == "move_right"):
		right()
    	else:
		print "Invalid command"
        
if __name__ == "__main__":
	while True:
		main()
