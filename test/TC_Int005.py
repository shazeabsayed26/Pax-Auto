import pytest
import rclpy
import time
import threading

from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor

from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Bool, Int32
from ackermann_msgs.msg import AckermannDrive


class TC_Int005(Node):
    """
    TC_Int005
    Passive system integration test for Lat-Lon Control.

    - Uses ONLY real data from Model City
    - Supports manual triggers via rqt
    - Order-independent
    - Long-running (mission-based)
    """

    def __init__(self):
        super().__init__('tc_int005_lat_lon_all_io')

        # ---------------- INPUT FLAGS ----------------
        self.inputs = {
            "odom": False,                  # continuous
            "state": False,                 # continuous
            "planned_path": False,          # one-shot
            "obstacle": False,              # rqt / scenario
            "traffic_light": False,         # rqt / scenario
            "ackermann_feedback": False,    # optional
        }

        # ---------------- OUTPUT FLAGS ----------------
        self.outputs = {
            "ackermann_drive": False,        # mandatory output
            "destination_reached": False,    # scenario dependent
        }

        self.last_cmd = None

        # ---------------- INPUT SUBSCRIBERS ----------------
        self.create_subscription(Odometry, '/odom', self.cb_odom, 10)
        self.create_subscription(Int32, '/state', self.cb_state, 10)
        self.create_subscription(PoseStamped, '/planned_path', self.cb_planned_path, 10)
        self.create_subscription(Bool, '/obstacle_ahead', self.cb_obstacle, 10)
        self.create_subscription(Int32, '/traffic_light_status', self.cb_traffic_light, 10)
        self.create_subscription(
            AckermannDrive,
            '/ackermann_drive_feedback',
            self.cb_ackermann_feedback,
            10
        )

        # ---------------- OUTPUT SUBSCRIBERS ----------------
        self.create_subscription(
            AckermannDrive,
            '/ackermann_drive',
            self.cb_ackermann_drive,
            10
        )

        self.create_subscription(
            Bool,
            '/destination_reached',
            self.cb_destination_reached,
            10
        )

    # ================= CALLBACKS =================

    def cb_odom(self, msg):
        self.inputs["odom"] = True

    def cb_state(self, msg):
        self.inputs["state"] = True

    def cb_planned_path(self, msg):
        self.inputs["planned_path"] = True

    def cb_obstacle(self, msg):
        self.inputs["obstacle"] = True

    def cb_traffic_light(self, msg):
        self.inputs["traffic_light"] = True

    def cb_ackermann_feedback(self, msg):
        self.inputs["ackermann_feedback"] = True

    def cb_ackermann_drive(self, msg):
        self.outputs["ackermann_drive"] = True
        self.last_cmd = msg

    def cb_destination_reached(self, msg):
        self.outputs["destination_reached"] = True


# ================= PYTEST FIXTURE =================

@pytest.fixture(scope="module")
def tc_int005_node():
    rclpy.init()
    node = TC_Int005()

    executor = SingleThreadedExecutor()
    executor.add_node(node)

    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()

    yield node

    executor.shutdown()
    node.destroy_node()
    rclpy.shutdown()


# ================= INTEGRATION TEST =================

def test_TC_Int005(tc_int005_node):
    """
    Integration Test Logic:

    - Run full system (all packages)
    - Observe interfaces for up to 6 minutes
    - Mandatory topics MUST appear
    - Event-based topics are OPTIONAL
    """

    MAX_DURATION = 360   # 6 minutes
    start_time = time.time()

    # -------- OBSERVATION PHASE --------
    while time.time() - start_time < MAX_DURATION:
        time.sleep(0.2)

    # -------- ASSERT INPUTS --------

    MANDATORY_INPUTS = ["odom", "state"]
    OPTIONAL_INPUTS = [
        "planned_path",
        "obstacle",
        "traffic_light",
        "ackermann_feedback",
    ]

    for key in MANDATORY_INPUTS:
        assert tc_int005_node.inputs[key], f"Mandatory input not received: {key}"
        print(f"Mandatory Input OK: {key}")

    for key in OPTIONAL_INPUTS:
        if tc_int005_node.inputs[key]:
            print(f"Optional Input observed: {key}")
        else:
            print(f"Optional Input NOT observed (acceptable): {key}")

    print("Expected Result 1: PASSED (mandatory inputs received)")

    # -------- ASSERT OUTPUTS --------

    assert tc_int005_node.outputs["ackermann_drive"], \
        "AckermannDrive output was never published"
    print("Expected Result 2: PASSED (ackermann_drive published)")

    if tc_int005_node.outputs["destination_reached"]:
        print("Optional Output observed: destination_reached")
    else:
        print("Optional Output NOT observed (acceptable)")

    print("TC_Int005: PASSED")
