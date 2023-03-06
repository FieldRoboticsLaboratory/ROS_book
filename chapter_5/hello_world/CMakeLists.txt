cmake_minimum_required(VERSION 3.0.2)
project(hello_world)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

add_message_files( 
FILES
gps_rtk.msg
)

add_service_files(
FILES
MultiplyTwoInts.srv
)

generate_messages( 
DEPENDENCIES
std_msgs
)

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES hello_world
  CATKIN_DEPENDS roscpp rospy std_msgs message_runtime
  DEPENDS system_lib
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)


add_executable(talker src/talker.cpp) 
target_link_libraries(talker ${catkin_LIBRARIES}) 
add_dependencies(talker ${PROJECT_NAME}_generate_messages_cpp)

add_executable(listener src/listener.cpp) 
target_link_libraries(listener ${catkin_LIBRARIES}) 
add_dependencies(listener ${PROJECT_NAME}_generate_messages_cpp)

add_executable(server src/server.cpp)
add_executable(client src/client.cpp)
add_dependencies(server ${PROJECT_NAME}_generate_messages_cpp)
add_dependencies(client ${PROJECT_NAME}_generate_messages_cpp)
target_link_libraries(server ${catkin_LIBRARIES} )
target_link_libraries(client ${catkin_LIBRARIES} )

