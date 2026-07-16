#!/usr/bin/env python3
import time
import pytest
import rclpy
import threading

from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import Bool


# =========================================================
# OBSERVER NODE (Door Status Only)
# =========================================================
class TC_Int_DoorOperationControl(Node):

    def __init__(self):
        super().__init__('tc_int_door_operation_control_observer')

        self.door_status_received = False
        self.last_door_status = None

        # Observe ONLY the output of Door Operation Control
        self.create_subscription(
            Bool,
            '/door_status',
            self.door_status_callback,
            10
        )

    def door_status_callback(self, msg):
        self.door_status_received = True
        self.last_door_status = msg.data
        self.get_logger().info(
            f"[TEST] /door_status received: {msg.data}"
        )


# =========================================================
# HELPER
# =========================================================
def wait_for(condition_fn, timeout=30.0, interval=0.1):
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

    node = TC_Int_DoorOperationControl()
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
# TEST CASE 1 — DOOR OPENS WHEN AUTHORIZED (STATE 2)
# =========================================================
def test_TC_Int_Door_01_open_when_authorized(test_node):
    """
    TC_Int_Door_01

    Preconditions:
    - state == 2 (Boarding)
    - authorization_result == True
    - user_inside == False

    Expected:
    - /door_status == True
    """

    test_node.door_status_received = False
    test_node.last_door_status = None

    assert wait_for(
        lambda: test_node.door_status_received
                and test_node.last_door_status is True,
        timeout=30.0
    ), "FAILED: Door did not open for authorized user in boarding state"


# =========================================================
# TEST CASE 2 — DOOR REMAINS CLOSED WHEN UNAUTHORIZED
# =========================================================
def test_TC_Int_Door_02_closed_when_unauthorized(test_node):
    """
    TC_Int_Door_02

    Preconditions:
    - state == 2 (Boarding)
    - authorization_result == False
    - user_inside == False

    Expected:
    - /door_status == False
    """

    test_node.door_status_received = False
    test_node.last_door_status = None

    assert wait_for(
        lambda: test_node.door_status_received
                and test_node.last_door_status is False,
        timeout=30.0
    ), "FAILED: Door opened for unauthorized user"


# =========================================================
# TEST CASE 3 — DOOR CLOSES WHEN USER ENTERS
# =========================================================
def test_TC_Int_Door_03_close_when_user_enters(test_node):
    """
    TC_Int_Door_03

    Preconditions:
    - state == 2 (Boarding)
    - authorization_result == True
    - user_inside == True

    Expected:
    - /door_status == False
    """

    test_node.door_status_received = False
    test_node.last_door_status = None

    assert wait_for(
        lambda: test_node.door_status_received
                and test_node.last_door_status is False,
        timeout=30.0
    ), "FAILED: Door did not close after user entered"
