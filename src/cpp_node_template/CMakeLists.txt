cmake_minimum_required(VERSION 3.22)
project(cpp_node_template)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(cpp_node src/main.cpp)
target_link_libraries(cpp_node PRIVATE rclcpp::rclcpp ${std_msgs_TARGETS})

install(TARGETS cpp_node DESTINATION lib/${PROJECT_NAME})

ament_package()
