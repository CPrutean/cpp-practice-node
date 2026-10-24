import time

import pytest
import rclpy
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import String

from py_node_template.py_node import PyNode


def spin_until(executor, predicate, timeout=5.0):
    deadline = time.monotonic() + timeout
    while not predicate() and time.monotonic() < deadline:
        executor.spin_once(timeout_sec=0.05)
    return predicate()


def test_publishes_numbered_messages_and_logs_replies():
    rclpy.init(args=["--ros-args", "-p", "publish_rate_hz:=50.0"])
    try:
        node = PyNode()
        peer = rclpy.create_node("peer")
        got = []
        peer.create_subscription(String, "py_to_cpp", lambda m: got.append(m.data), 10)
        reply = peer.create_publisher(String, "cpp_to_py", 10)

        executor = SingleThreadedExecutor()
        executor.add_node(node)
        executor.add_node(peer)

        assert spin_until(executor, lambda: len(got) >= 3)
        assert got[:3] == ["ping 0", "ping 1", "ping 2"]

        reply.publish(String(data="pong"))
        assert spin_until(executor, lambda: node.received == ["pong"])

        node.destroy_node()
        peer.destroy_node()
    finally:
        rclpy.shutdown()


def test_rejects_non_positive_rate():
    rclpy.init(args=["--ros-args", "-p", "publish_rate_hz:=0.0"])
    try:
        with pytest.raises(ValueError):
            PyNode()
    finally:
        rclpy.shutdown()
