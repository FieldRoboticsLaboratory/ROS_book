#include <cstdlib>
#include "ros/ros.h"
#include "hello_world/MultiplyTwoInts.h"

int main(int argc, char **argv)
{
    //ROS节点初始化
    ros::init(argc, argv, "multiply_two_ints_client");
    //从终端命令行获取两个加数,if(argc ！= 3)的意思是引导用户输入不超过三个参数，即输入两个参数
    if(argc != 3)
    {
        ROS_INFO("usage: multiply_two_ints_client X and Y");
        return 1;
    }
    //创建节点句柄
    ros::NodeHandle n;
    //功能：创建一个multiply_two_ints的Client实例，指定服务类型为learning_sun::MultiplyTwoInts
    ros::ServiceClient client = n.serviceClient<hello_world::MultiplyTwoInts>("multiply_two_ints");
    //功能：实例化一个服务类型数据的变量，该变量包含两个成员：request与response，
// 将节点运行时输入的两个参数作为需要相加的两个整数型存储到变量中
    hello_world::MultiplyTwoInts srv;
    srv.request.a = atoll(argv[1]);
    srv.request.b = atoll(argv[2]);
     //进行服务调用，如果调用过程会发生阻塞，如果调用成功则返回ture，调用失败则返回false.srv.response则不可用
    if(client.call(srv))
    {
        ROS_INFO("Multi: %1d", (long int)srv.response.multi);
    }
    else
    {
        ROS_ERROR("Failed to call service multiply_two_ints");
        return 1;
    }
    return 0;
}
