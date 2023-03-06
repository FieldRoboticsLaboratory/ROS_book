cmake_minimum_required(VERSION 2.8.3)
project(DeepLearning)
 
## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages

set(OpenCV_DIR /usr/share/OpenCV) 
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  
) 
catkin_package()

install(PROGRAMS
   scripts/test.py 
   DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

