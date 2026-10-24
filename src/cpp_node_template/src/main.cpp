#include <memory>

#include "rclcpp/rclcpp.hpp"

// Talks to py_node_template over these topics (std_msgs/msg/String):
//   subscribe: py_to_cpp   (the Python node publishes "ping <n>" at 1 Hz)
//   publish:   cpp_to_py   (the Python node logs whatever arrives here)

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<rclcpp::Node>("cpp_node"));
  rclcpp::shutdown();
  return 0;
}
