import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PyNode(Node):
    """Publishes "<message_prefix> <n>" on `publish_topic` at `publish_rate_hz` and
    logs anything received on `subscribe_topic`.

    The defaults pair with the C++ node: it should subscribe to `py_to_cpp` and
    publish on `cpp_to_py`.
    """

    def __init__(self):
        super().__init__("py_node")
        publish_topic = self.declare_parameter("publish_topic", "py_to_cpp").value
        subscribe_topic = self.declare_parameter("subscribe_topic", "cpp_to_py").value
        self.message_prefix = self.declare_parameter("message_prefix", "ping").value
        rate_hz = self.declare_parameter("publish_rate_hz", 1.0).value

        if rate_hz <= 0.0:
            raise ValueError("publish_rate_hz must be > 0")

        self.count = 0
        self.received = []
        self.publisher = self.create_publisher(String, publish_topic, 10)
        self.subscription = self.create_subscription(
            String, subscribe_topic, self.on_message, 10
        )
        self.timer = self.create_timer(1.0 / rate_hz, self.on_timer)

        self.get_logger().info(
            f"Publishing on '{publish_topic}' at {rate_hz:.1f} Hz, "
            f"listening on '{subscribe_topic}'"
        )

    def on_timer(self):
        msg = String()
        msg.data = f"{self.message_prefix} {self.count}"
        self.count += 1
        self.publisher.publish(msg)

    def on_message(self, msg):
        self.received.append(msg.data)
        self.get_logger().info(f"Received: '{msg.data}'")


def main(args=None):
    rclpy.init(args=args)
    node = PyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
