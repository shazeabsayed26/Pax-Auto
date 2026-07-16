#!/usr/bin/env python3
import time
import pytest
import rclpy
import threading

from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import Int32, Bool


# =========================================================
# OBSERVER NODE (Decision Core Outputs Only)
# =========================================================
class TC_Int_DecisionCore(Node):

    def __init__(self):
        super().__init__('tc_int_decision_core_observer')

        self.state_received = False
        self.shuttle_conf_received = False

        self.last_state = None
        self.last_shuttle_conf = None

        # Observe ONLY Decision Core outputs
        self.create_subscription(
            Int32,
            '/state',
            self.state_callback,
            10
        )

        self.create_subscription(
            Bool,
            '/shuttle_confirmation',
            self.shuttle_conf_callback,
            10
        )

    def state_callback(self, msg):
        self.state_received = True
        self.last_state = msg.data
        self.get_logger().info(f"[TEST] /state received: {msg.data}")

    def shuttle_conf_callback(self, msg):
        self.shuttle_conf_received = True
        self.last_shuttle_conf = msg.data
        self.get_logger().info(f"[TEST] /shuttle_confirmation received: {msg.data}")


# =========================================================
# HELPER
# =========================================================
def wait_for(condition_fn, timeout=60.0, interval=0.1):
    start = time.time()
    while time.time() - start < timeout:
        if condition_fn():
            return True
        time.sleep(interval)
    return False


# =========================================================
# PYTEST FIXTURE
# =========================================================
@pytest.fixture(scope="module")
def test_node():
    rclpy.init()

    node = TC_Int_DecisionCore()
    executor = SingleThreadedExecutor()
    executor.add_node(node)

    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()

    yield node

    executor.shutdown()
    thread.join(timeout=1.0)
    node.destroy_node()
    rclpy.shutdown()


# =========================================================
# TEST CASE 1 — BOOKING REQUEST → DRIVING & PLANNING
# =========================================================
def test_TC_Int_DC_01_booking_request(test_node):
    """
    TC_Int_DC_01

    Preconditions:
    - booking_request = True
    - select_shuttle = 4

    Expected:
    - /state == 1 (DRIVING_AND_PLANNING)
    - /shuttle_confirmation == True
    """

    test_node.state_received = False
    test_node.shuttle_conf_received = False

    assert wait_for(
        lambda: test_node.state_received and test_node.last_state == 1,
        timeout=60.0
    ), "FAILED: Decision Core did not enter DRIVING_AND_PLANNING state"

    assert wait_for(
        lambda: test_node.shuttle_conf_received and test_node.last_shuttle_conf is True,
        timeout=60.0
    ), "FAILED: Shuttle confirmation not published after booking"


# =========================================================
# TEST CASE 2 — DESTINATION REACHED → BOARDING
# =========================================================
def test_TC_Int_DC_02_destination_reached_boarding(test_node):
    """
    TC_Int_DC_02

    Preconditions:
    - destination_reached = True
    - user_inside = False

    Expected:
    - /state == 2 (BOARDING)
    """

    test_node.state_received = False

    assert wait_for(
        lambda: test_node.state_received and test_node.last_state == 2,
        timeout=60.0
    ), "FAILED: Decision Core did not enter BOARDING state"


# =========================================================
# TEST CASE 3 — EMERGENCY BUTTON → DROP OFF
# =========================================================
def test_TC_Int_DC_03_emergency_transition(test_node):
    """
    TC_Int_DC_03

    Preconditions:
    - emergency_button = True
    - state == DRIVING_AND_PLANNING

    Expected:
    - /state == 3 (DROP_OFF_AND_DEBOARDING)
    """

    test_node.state_received = False

    assert wait_for(
        lambda: test_node.state_received and test_node.last_state == 3,
        timeout=60.0
    ), "FAILED: Decision Core did not enter emergency DROP_OFF state"
