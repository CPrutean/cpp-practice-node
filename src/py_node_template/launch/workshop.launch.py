import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    params = os.path.join(
        get_package_share_directory("py_node_template"), "config", "params.yaml"
    )
    return LaunchDescription(
        [
            Node(
                package="py_node_template",
                executable="py_node",
                name="py_node",
                output="screen",
                parameters=[params],
            ),
            Node(
                package="cpp_node_template",
                executable="cpp_node",
                name="cpp_node",
                output="screen",
            ),
        ]
    )
