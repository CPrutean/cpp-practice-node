#ifndef CPP_NODE_TEMPLATE__CPP_NODE_HPP_
#define CPP_NODE_TEMPLATE__CPP_NODE_HPP_

#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

namespace cpp_node_template
{

// Talks to py_node_template over these topics (std_msgs/msg/String):
//   subscribe: py_to_cpp   (the Python node publishes "ping <n>" at 1 Hz)
//   publish:   cpp_to_py   (the Python node logs whatever arrives here)
class CppNode : public rclcpp::Node
{
public:
  CppNode();

private:
  void on_message(const std_msgs::msg::String::SharedPtr msg);

  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_;
  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
};

}  // namespace cpp_node_template

#endif  // CPP_NODE_TEMPLATE__CPP_NODE_HPP_
