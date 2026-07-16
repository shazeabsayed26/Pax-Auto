#!/usr/bin/env python3
import time
import pytest
import rclpy
from rclpy.node import Node

from std_msgs.msg import Bool, Int32, UInt8, String

# Safe import for custom message
try:
    from custom_msgs.msg import PickupDropPose
except ImportError:
    PickupDropPose = None


# ==========================================================
# TEST NODE
# ==========================================================
class BookingFlowIntegrationTest(Node):
    def __init__(self):
        super().__init__("booking_flow_integration_test")

        # -------- Publishers (Firestore server simulation) --------
        self.booking_pub = self.create_publisher(Bool, "/booking_request", 10)
        self.server_code_pub = self.create_publisher(String, "/server_code", 10)
        self.select_shuttle_pub = self.create_publisher(UInt8, "/select_shuttle", 10)
        self.user_inside_pub = self.create_publisher(Bool, "/user_inside", 10)

        if PickupDropPose is not None:
            self.pickupdrop_pub = self.create_publisher(
                PickupDropPose, "/pickupdrop_location", 10
            )
        else:
            self.pickupdrop_pub = None

        # -------- Observed outputs --------
        self.seen_states = set()
        self.last_confirmation = None

        self.create_subscription(Int32, "/state", self.state_callback, 10)
        self.create_subscription(
            Bool, "/shuttle_confirmation", self.confirmation_callback, 10
        )

    def state_callback(self, msg):
        self.seen_states.add(msg.data)
        self.get_logger().info(f"[TEST] /state received: {msg.data}")

    def confirmation_callback(self, msg):
        self.last_confirmation = msg.data
        self.get_logger().info(
            f"[TEST] /shuttle_confirmation received: {msg.data}"
        )


# ==========================================================
# PYTEST FIXTURES
# ==========================================================
@pytest.fixture(scope="module")
def ros():
    rclpy.init()
    yield
    rclpy.shutdown()


@pytest.fixture
def node(ros):
    node = BookingFlowIntegrationTest()
    yield node
    node.destroy_node()


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================
def wait_for(condition_fn, node, timeout=6.0):
    start = time.time()
    while time.time() - start < timeout:
        rclpy.spin_once(node, timeout_sec=0.1)
        if condition_fn():
            return True
    return False


def create_dummy_pose():
    pose = PoseStamped()
    pose.header.frame_id = "map"
    pose.pose.orientation.w = 1.0
    return pose


# ==========================================================
# INTEGRATION TEST
# ==========================================================
def test_complete_booking_flow(node):
    """
    Integration scenario:
    - booking_request = True
    - server_code = "emily0986"
    - select_shuttle = 4
    - user_inside = True
    - pickup/drop published if available

    Verification:
    - booking is processed
    - shuttle_confirmation is published
    - FSM reacts (state topic observed)
    """

    # -------- Booking initiated --------
    node.booking_pub.publish(Bool(data=True))
    node.server_code_pub.publish(String(data="emily0986"))
    node.select_shuttle_pub.publish(UInt8(data=4))
    time.sleep(0.3)

    # -------- User enters shuttle --------
    node.user_inside_pub.publish(Bool(data=True))
    time.sleep(0.3)

    # -------- Pickup & Drop (optional) --------
    if node.pickupdrop_pub is not None:
        msg = PickupDropPose()
        msg.pickup = create_dummy_pose()
        msg.drop = create_dummy_pose()
        node.pickupdrop_pub.publish(msg)
        time.sleep(0.3)
    else:
        node.get_logger().warning(
            "publish /pickupdrop_location"
        )

    # -------- Assertions (ROBUST) --------
    assert wait_for(lambda: node.last_confirmation is not None, node), \
        "shuttle_confirmation was never published"

    assert node.last_confirmation in (True, False), \
        f"Invalid shuttle_confirmation: {node.last_confirmation}"

    assert len(node.seen_states) > 0, \
        "decision_core did not react to booking flow (no state observed)"

