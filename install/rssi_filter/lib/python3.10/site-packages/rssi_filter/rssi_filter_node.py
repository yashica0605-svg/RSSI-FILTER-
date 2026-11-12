import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from collections import deque


class RSSIFilterNode(Node):

    def __init__(self):
        super().__init__('rssi_filter_node')

        self.window_size = 5
        self.rssi_values = deque(maxlen=self.window_size)

        self.subscription = self.create_subscription(
            Float32,
            '/rssi/raw',
            self.rssi_callback,
            10
        )

        self.publisher = self.create_publisher(
            Float32,
            '/rssi/filtered',
            10
        )

        self.get_logger().info('RSSI Moving Average Filter Started')

    def rssi_callback(self, msg):

        self.rssi_values.append(msg.data)

        average = sum(self.rssi_values) / len(self.rssi_values)

        filtered_msg = Float32()
        filtered_msg.data = float(average)

        self.publisher.publish(filtered_msg)

        self.get_logger().info(
            f'Raw RSSI: {msg.data:.2f} dBm | '
            f'Filtered RSSI: {average:.2f} dBm'
        )


def main(args=None):
    rclpy.init(args=args)

    node = RSSIFilterNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
