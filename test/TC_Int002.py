import time
import pytest
import rclpy
import threading

from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor

from nav_msgs.msg import Odometry, Path
from std_msgs.msg import Int32
from custom_msgs.msg import PickupDropPose

class TC_Int_PathPlanner(Node):
    def __init__(self):
        super().__init__('tc_int_path_planner_observer')

        self.odom_received = False
        self.pickdrop_received = False
        self.state_received = False
        self.path_received = False

        self.last_state = None
        self.path_state = None

        self.create_subscription(Odometry, '/odom', self.odom_cb, 10)
        self.create_subscription(
            PickupDropPose, '/pickupdrop_location', self.pickdrop_cb, 10
        )
        self.create_subscription(Int32, '/state', self.state_cb, 10)
        self.create_subscription(Path, '/planned_path', self.path_cb, 10)

    def odom_cb(self, msg):
        self.odom_received = True

    def pickdrop_cb(self, msg):
        self.pickdrop_received = True

    def state_cb(self, msg):
        self.state_received = True
        self.last_state = msg.data

    def path_cb(self, msg):
        if len(msg.poses) > 1:
            self.path_received = True
            self.path_state = self.last_state

def wait_for(condition_fn, timeout=30.0, interval=0.1):
    start = time.time()
    while time.time() - start < timeout:
        if condition_fn():
            return True
        time.sleep(interval)
    return False

@pytest.fixture(scope="module")
def test_node():
    rclpy.init()

    node = TC_Int_PathPlanner()
    executor = SingleThreadedExecutor()
    executor.add_node(node)

    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()

    yield node

    executor.shutdown()
    thread.join(timeout=1.0)
    node.destroy_node()
    rclpy.shutdown()

# TEST CASE 1: PICKUP PATH (state 0 → 1)
def test_TCInt002_pickup_path(test_node):
    """
    Verifies that a pickup path is published when the system
    transitions to state = 1 
    """

    assert wait_for(lambda: test_node.odom_received), \
        "FAILED: /odom not received"

    assert wait_for(lambda: test_node.pickdrop_received), \
        "FAILED: /pickupdrop_location not received"

    assert wait_for(lambda: test_node.state_received), \
        "FAILED: /state not received"

    assert wait_for(
        lambda: test_node.path_received and test_node.path_state == 1
    ), "FAILED: Pickup path not published"

# TEST CASE 2: DROP PATH (state 2 → 1)
def test_TCInt002_drop_path(test_node):
    """
    Verifies that a drop path is published when the system
    transitions to state = 1 after drop selection.
    """
    
    test_node.path_received = False
    test_node.path_state = None

    assert wait_for(
        lambda: test_node.path_received and test_node.path_state == 1
    ), "FAILED: Drop path not published"

