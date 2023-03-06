      #include <ros/ros.h> 
      #include <serial/serial.h>  //ROS已经内置了的串口包 
      #include <std_msgs/String.h> 
      #include <iostream>   //输入输出库
      #include<geometry_msgs/Twist.h>
      serial::Serial ser; //声明串口对象 
      uint8_t buffer[3]; //定义串口数据存放数组
      uint8_t a; 
      int main (int argc, char** argv) 
      { 
	      //初始化节点 
	      ros::init(argc, argv, "serial_remote_node"); 
	      //声明节点句柄 
	      ros::NodeHandle nh; 

	      //发布主题 
	      ros::Publisher read_pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel",1); 
	      ros::Publisher voice_pub = nh.advertise<std_msgs::String>("/voiceWords",1);
	      try 
	      { 
		      //设置串口属性，并打开串口 
		      ser.setPort("/dev/ttyUSB0"); 
		      ser.setBaudrate(9600); 
		      serial::Timeout to = serial::Timeout::simpleTimeout(1000); 
		      ser.setTimeout(to); 
		      ser.open(); 
	      } 
	      catch (serial::IOException& e) 
	      { 
		      ROS_ERROR_STREAM("Unable to open port "); 
		      return -1; 
	      } 
	      //检测串口是否已经打开，并给出提示信息 
	      if(ser.isOpen()) 
	      { 
	      	ROS_INFO_STREAM("Serial Port initialized"); 
	      } 
	      else 
	      { 
	      	return -1; 
	      } 
	      //指定循环的频率 
	      ros::Rate loop_rate(10); 
	      geometry_msgs::Twist vel;
	      std_msgs::String voice_msg;
	      while(ros::ok()) 
	      { 
	      	if(ser.available())
		{ 
	      	ROS_INFO_STREAM("Reading from serial port\n"); 
                ser.read(buffer,3);//从缓冲区中读取3位数据，存放到定义好的数组中
                for(int i =0 ;i<3;i++)  
		{
			if(buffer[i]==0x00)
			{
				if(buffer[i+1]==0xff)  //帧头
				{
					ROS_INFO_STREAM("Remote Success");
					a=buffer[i+2];
				}
			}
		}
	      	switch(a)
		{
		case 0x18:
			ROS_INFO_STREAM("straight");
			vel.linear.x=2;
			vel.angular.z=0;
			voice_msg.data="前进";
			break;
		case 0x52:
			ROS_INFO_STREAM("back");
			vel.linear.x=-2;
			vel.angular.z=0;
			voice_msg.data="后退";
			break;
		case 0x08:
			ROS_INFO_STREAM("left");
			vel.linear.x=0;
			vel.angular.z=1;
			voice_msg.data="左转";
			break;
		case 0x5a:
			ROS_INFO_STREAM("right");
			vel.linear.x=0;
			vel.angular.z=-1;
			voice_msg.data="右转";
			break;
		case 0x1c:
			ROS_INFO_STREAM("stop");
			vel.linear.x=0;
			vel.angular.z=0;
			voice_msg.data="停止";
			break;
		default:
			ROS_INFO_STREAM("invalid button");
			voice_msg.data="无效按键";
			break;
                }

	      	read_pub.publish(vel); 
		voice_pub.publish(voice_msg);
     		} 

	     	//处理ROS的信息，比如订阅消息,并调用回调函数 
	      	ros::spinOnce(); 
	      	loop_rate.sleep(); 
	      } 
      } 

