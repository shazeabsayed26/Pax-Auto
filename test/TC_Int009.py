import rclpy
import pytest
import time

from rclpy.node import Node
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import PoseStamped
from custom_msgs.msg import ObstacleDetectionData, ObstacleDetectionArray
from std_msgs.msg import Bool


TEST_TIMEOUT = 10.0  # seconds


class IntegrationTestNode(Node):

    def __init__(self):
        super().__init__('integration_test_node')

        self.odom_msg = None
        self.planned_path_msg = None
        self.obstacles_msg = None
        self.obstacle_ahead = None

        self.sub_odom = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.sub_planned_path = self.create_subscription(
            Path,
            "/planned_path",
            self.path_callback,
            10
        )

        self.sub_obstacles = self.create_subscription(
            ObstacleDetectionArray,
            "/obstacles",
            self.obstacle_callback,
            10
        )

        self.sub_obstacle_ahead = self.create_subscription(
            Bool,
            "/obstacle_ahead",
            self.obstacle_ahead_callback,
            10
        )

    def odom_callback(self, msg):
        self.odom_msg = msg
        self.get_logger().info('Received odom message')

    def path_callback(self, msg):
        self.planned_path_msg = msg
        self.get_logger().info('Received planned path message')

    def obstacle_callback(self, msg):
        self.obstacles_msg = msg
        self.get_logger().info('Received obstacles message')
    
    def obstacle_ahead_callback(self, msg):
        self.obstacle_ahead = msg
        self.get_logger().info('Received obstacle ahead message')


@pytest.fixture(scope='module')
def rclpy_context():
    rclpy.init()
    yield
    rclpy.shutdown()


def spin_until(node, condition_fn, timeout=TEST_TIMEOUT):
    start_time = time.time()
    while time.time() - start_time < timeout:
        rclpy.spin_once(node, timeout_sec=0.1)
        if condition_fn():
            return True
    return False


def test_TC_Int002(rclpy_context):
    """
    Integration test:
    Obstacle detection, Path planning & Localization  -> Obstacle Avoidance
    """

    node = IntegrationTestNode()

    # 1. Wait for odom
    assert spin_until(
        node,
        lambda: node.odom_msg is not None
    ), " No odom message received"

    odom = node.odom_msg
    print("Expected Result 1a: PASSED")

    # 2. Wait for planned path
    assert spin_until(
        node,
        lambda: node.planned_path_msg is not None
    ), " No planned_path_msg received"

    planned_path = node.planned_path_msg
    assert len(planned_path.poses) > 1, "Number of poses is less than 1"
    print("Expected Result 1a: PASSED")

    # 3. Wait for obstacles
    assert spin_until(
        node,
        lambda: node.obstacles_msg is not None
    ), " No obstacle message received"

    obstacles_array = node.obstacles_msg
    assert len(obstacles_array.obstacles) == 1, "Number of obstacles is not 1"
    print("Expected Result 1c: PASSED")

    # 4. Wait for obstacle_ahead
    assert spin_until(
        node,
        lambda: node.obstacle_ahead is not None
    ), " No obstacle_ahead message received"

    obstacle_ahead_status = node.obstacle_ahead

    assert obstacle_ahead_status is True, "There is no obstacle"
    print("Expected Result 1d: PASSED")


    node.destroy_node()