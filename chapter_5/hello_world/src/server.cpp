#include "ros/ros.h"
//这里使用的头文件是hello_word/MultiplyTwoInts.h，这是我们自定义的服务数据类型的描述文件。
#include "hello_world/MultiplyTwoInts.h"
//service回调函数，输入参数req,输出参数res
bool add(hello_world::MultiplyTwoInts::Request &req,
         hello_world::MultiplyTwoInts::Response &res)
{
    //将参数中的请求数据相加，结果放入应答变量中
    res.multi = req.a * req.b;
    ROS_INFO("request: x=%1d,y=%1d" ,(long int)req.a,(long int)req.b);
    ROS_INFO("sending back response: [%1d]" ,(long int)res.multi);
    return true;
}
int main(int argc, char **argv)
{
    //ROS节点初始化，创建节点名称
    ros::init(argc, argv, "multiply_two_ints_server");
    //创建节点句柄
    ros::NodeHandle n;
    //创建一个名为add_two_ints的server,注册回调函数add()
    ros::ServiceServer service = n.advertiseService("multiply_two_ints",add);
    //循环等待回调函数
    ROS_INFO("Ready to multiply two ints!");
    ros::spin();
    return 0;
}
