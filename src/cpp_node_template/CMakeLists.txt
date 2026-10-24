cmake_minimum_required(VERSION 3.22)
project(cpp_node_template)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_library(cpp_node_lib src/cpp_node.cpp)
target_include_directories(cpp_node_lib PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>)
target_link_libraries(cpp_node_lib PUBLIC rclcpp::rclcpp ${std_msgs_TARGETS})

add_executable(cpp_node src/main.cpp)
target_link_libraries(cpp_node PRIVATE cpp_node_lib)

install(DIRECTORY include/ DESTINATION include/${PROJECT_NAME})
install(TARGETS cpp_node_lib
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin)
install(TARGETS cpp_node DESTINATION lib/${PROJECT_NAME})

ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)
ament_export_dependencies(rclcpp std_msgs)

ament_package()
