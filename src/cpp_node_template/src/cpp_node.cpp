#include "cpp_node_template/cpp_node.hpp"

#include <functional>

namespace cpp_node_template
{

CppNode::CppNode()
: rclcpp::Node("cpp_node")
{
  publisher_ = create_publisher<std_msgs::msg::String>("cpp_to_py", 10);
  subscription_ = create_subscription<std_msgs::msg::String>(
    "py_to_cpp", 10, std::bind(&CppNode::on_message, this, std::placeholders::_1));
}

void CppNode::on_message(const std_msgs::msg::String::SharedPtr msg)
{
  // TODO: fill in
  RCLCPP_INFO(get_logger(), "received: '%s'", msg->data.c_str());
}

}  // namespace cpp_node_template
