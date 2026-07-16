import time
import pytest
import rclpy
import threading

from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor

from std_msgs.msg import Bool


class TC_Int_TrafficLight(Node):

    def __init__(self):
        super().__init__('tc_int_traffic_light_observer')

        self.status_received = False
        self.last_status = None

        # Observe Traffic Light output ONLY
        self.create_subscription(
            Bool,
            '/traffic_light_status',
            self.status_callback,
            10
        )

    def status_callback(self, msg):
        self.status_received = True
        self.last_status = msg.data


def wait_for(condition_fn, timeout=120.0, interval=0.1):
    start = time.time()
    while time.time() - start < timeout:
        if condition_fn():
            return True
        time.sleep(interval)
    return False


@pytest.fixture(scope="module")
def test_node():
    rclpy.init()

    node = TC_Int_TrafficLight()
    executor = SingleThreadedExecutor()
    executor.add_node(node)

    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()

    yield node

    executor.shutdown()
    thread.join(timeout=1.0)
    node.destroy_node()
    rclpy.shutdown()



# TEST CASE 1: RED LIGHT → STOP
def test_TCInt003_stopsignal(test_node):
    """
    Verifies that a RED traffic light causes STOP (traffic_light_status = True).
    Preconditions:
    - Vehicle is inside intersection
    - Decoder publishes RED signal
    """

    assert wait_for(
        lambda: test_node.status_received and test_node.last_status is True,
        timeout=120.0
    ), "FAILED: STOP was not triggered by RED traffic light"



# TEST CASE 2: GREEN LIGHT → GO
def test_TCInt003_gosignal(test_node):
    """
    Verifies that a GREEN traffic light causes GO (traffic_light_status = False).
    Preconditions:
    - Vehicle is inside intersection
    - Decoder publishes GREEN signal
    """

    # Reset observation
    test_node.status_received = False
    test_node.last_status = None

    assert wait_for(
        lambda: test_node.status_received and test_node.last_status is False,
        timeout=120.0
    ), "FAILED: GO was not triggered by GREEN traffic light"

