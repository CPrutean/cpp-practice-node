#include <memory>

#include "rclcpp/rclcpp.hpp"

#include "cpp_node_template/cpp_node.hpp"

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<cpp_node_template::CppNode>());
  rclcpp::shutdown();
  return 0;
}
