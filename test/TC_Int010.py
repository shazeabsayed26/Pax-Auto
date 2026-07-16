#!/usr/bin/env python3

import time
import pytest
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

import launch
import launch_ros
import launch_testing
import launch_testing.actions


# ------------------------------------------------------------
# Launch all real system components
# ------------------------------------------------------------
@pytest.mark.launch_test
def generate_test_description():
    """
    Launch the real system components required for ETA computation.
    """

    eta_node = launch_ros.actions.Node(
        package='eta_component',
        executable='eta_node',
        name='eta_component',
        output='screen'
    )

    path_planner_node = launch_ros.actions.Node(
        package='path_planning',
        executable='path_planner_node',
        name='path_planner',
        output='screen'
    )

    localization_node = launch_ros.actions.Node(
        package='localization',
        executable='localization_node',
        name='localization',
        output='screen'
    )

    control_node = launch_ros.actions.Node(
        package='lat_lon_control',
        executable='lat_lon_controller',
        name='lat_lon_controller',
        output='screen'
    )

    return (
        launch.LaunchDescription([
            eta_node,
            path_planner_node,
            localization_node,
            control_node,
            launch_testing.actions.ReadyToTest(),
        ]),
        {}
    )


# ------------------------------------------------------------
# Test Node (Black-box observer)
# ------------------------------------------------------------
class TestETABasicIntegration(Node):
    """
    Test node that observes ETA output.
    """

    def __init__(self):
        super().__init__('test_eta_basic_node')

        self.eta_received = False
        self.eta_value = None

        self.get_logger().info(
            "[TEST] Listening for ETA output on topic /eta_info"
        )

        self.create_subscription(
            Int32,
            '/eta_info',
            self.eta_callback,
            10
        )

    def eta_callback(self, msg: Int32):
        self.eta_received = True
        self.eta_value = msg.data

        self.get_logger().info(
            f"[TEST] /eta_info received with value: {msg.data}"
        )


# ------------------------------------------------------------
# Basic Integration Test Case
# ------------------------------------------------------------
@launch_testing.post_shutdown_test()
class TestETABasic:
    """
    Black-box integration test for ETA component.
    """

    def test_eta_is_published(self, proc_output):
        """
        Test objective:
        Verify that ETA is published when all system components are running.
        """

        rclpy.init()
        node = TestETABasicIntegration()

        node.get_logger().info(
            "[TEST] Waiting for ETA output from ETA component..."
        )

        start_time = time.time()
        timeout = 15.0  # seconds

        while time.time() - start_time < timeout:
            rclpy.spin_once(node, timeout_sec=0.5)
            if node.eta_received:
                break

        node.destroy_node()
        rclpy.shutdown()

        # ----------------------------------------------------
        # Assertions (Black-box validation)
        # ----------------------------------------------------
        assert node.eta_received, \
            "[TEST] FAIL: ETA was not published on /eta_info"

        assert node.eta_value is not None, \
            "[TEST] FAIL: ETA value is None"

        assert node.eta_value >= 0, \
            "[TEST] FAIL: ETA value is invalid"

