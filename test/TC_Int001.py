import rclpy
import pytest
import time
 
from rclpy.node import Node
from nav_msgs.msg import Odometry
from custom_msgs.msg import DetectedObjectsPositionArray
from etsi_its_cpm_ts_msgs.msg import CollectivePerceptionMessage as CPM
from etsi_its_cam_ts_msgs.msg import CAM
 
TEST_TIMEOUT = 10.0  # seconds
 
 
class IntegrationTestNode(Node):
 
    def __init__(self):
        super().__init__('integration_test_node')
 
        self.detected_objects_msg = None
        self.cpm_msg = None
        self.odom_msg = None
        self.cam_msg = None
 
        self.sub_detected_objects = self.create_subscription(
            DetectedObjectsPositionArray,
            '/detected_objects_pos',
            self.detected_objects_callback,
            10
        )
 
        self.sub_cpm = self.create_subscription(
            CPM,
            '/cpm',
            self.cpm_callback,
            10
        )
        
        self.sub_cam = self.create_subscription(
            CAM,
            '/cam',
            self.cam_callback,
            10
        )
        
        self.sub_odom = self.create_subscription(
            Odometry, 
            '/odom', 
            self.odom_callback, 
            10
        )
 
    def detected_objects_callback(self, msg):
        self.detected_objects_msg = msg
        self.get_logger().info('Received DetectedObjectsPositionArray')
 
    def cpm_callback(self, msg):
        self.cpm_msg = msg
        self.get_logger().info('Received CPM message')
        
    def cam_callback(self, msg):
        self.cam_msg = msg
        self.get_logger().info('Received CAM message')
    
    def odom_callback(self, msg):
        self.odom_msg = msg
        self.get_logger().info('Received odom message')
 
 
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
 
 
def test_TC_Int001(rclpy_context):
    """
    Integration test:
    Environment Model & Localization  -> V2XTransmitter
    """
 
    node = IntegrationTestNode()
 
    # 1. Wait for detected objects
    assert spin_until(
        node,
        lambda: node.detected_objects_msg is not None
    ), " No DetectedObjectsPositionArray received"
 
    dop = node.detected_objects_msg
    assert len(dop.array) == 1, " Length of detected objects position is not 1"
 
    first_obj = dop.array[0]
    assert first_obj.id == 1
    assert first_obj.class_id == '\x01'
    print("Expected Result 1a: PASSED")
    
    # 2. Wait for odom
    assert spin_until(
        node,
        lambda: node.odom_msg is not None
    ), " No odom message received"
 
    odom = node.odom_msg
    print("Expected Result 1b: PASSED")
    
    # 3. Wait for CPM
    assert spin_until(
        node,
        lambda: node.cpm_msg is not None
    ), " No CPM message received"
 
    cpm = node.cpm_msg
 
    # Validate CPM header
    assert cpm.header.protocol_version.value == 2
    assert cpm.header.message_id.value == 14
    assert cpm.header.station_id.value == 4
 
    # Validate CPM payload
    containers = cpm.payload.cpm_containers.value.array
    assert len(containers) == 1, " CPM contains no containers"
 
    perceived_container = containers[0]
    perceived_objects = (
        perceived_container
        .container_data_perceived_object_container
        .perceived_objects
        .array
    )

    assert len(perceived_objects) == 1, " CPM contains no perceived objects"
    print("Expected Result 1c: PASSED")
    
    # 4. Wait for CAM
    assert spin_until(
        node,
        lambda: node.cam_msg is not None
    ), " No CAM message received"
 
    cam = node.cam_msg
 
    # Validate CAM header
    assert cam.header.protocol_version.value == 2
    assert cam.header.message_id.value == 2
    assert cam.header.station_id.value == 4
    print("Expected Result 1d: PASSED")
    
    node.destroy_node()