import time
import pytest
import rclpy
import threading

from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor

from std_msgs.msg import Bool


# =========================================================
# Observer Node
# =========================================================
class TC_Int_QRAuthorization(Node):

    def __init__(self):
        super().__init__('tc_int_qr_authorization_observer')

        self.auth_received = False
        self.last_auth = None

        # Observe authorization output ONLY
        self.create_subscription(
            Bool,
            '/authorization_result',
            self.auth_callback,
            10
        )

    def auth_callback(self, msg):
        self.auth_received = True
        self.last_auth = msg.data


# =========================================================
# Helper
# =========================================================
def wait_for(condition_fn, timeout=120.0, interval=0.1):
    start = time.time()
    while time.time() - start < timeout:
        if condition_fn():
            return True
        time.sleep(interval)
    return False


# =========================================================
# Pytest Fixture
# =========================================================
@pytest.fixture(scope="module")
def test_node():
    rclpy.init()

    node = TC_Int_QRAuthorization()
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
# TEST CASE 1 — VALID QR → AUTHORIZED
# =========================================================
def TC_Int006(test_node):
    """
    TC_Int006

    Preconditions:
    - state == 2
    - server_code equals QR code shown to camera

    Expected:
    - /authorization_result == True
    """

    test_node.auth_received = False
    test_node.last_auth = None

    assert wait_for(
        lambda: test_node.auth_received and test_node.last_auth is True,
        timeout=120.0
    ), "FAILED: Authorization was not granted for valid QR code"


# =========================================================
# TEST CASE 2 — INVALID QR → NOT AUTHORIZED
# =========================================================
def TC_Int006(test_node):
    """
    TC_Int006

    Preconditions:
    - state == 2
    - server_code does NOT match QR code shown

    Expected:
    - /authorization_result == False
    """

    test_node.auth_received = False
    test_node.last_auth = None

    assert wait_for(
        lambda: test_node.auth_received and test_node.last_auth is False,
        timeout=120.0
    ), "FAILED: Authorization incorrectly granted for invalid QR code"

