# Procedure to do interface test
1. Follow the installation and usage procedure from component repository to launch the ROS2 package
2. Execute the commands for feeding input in new terminal
    ```bash
    source ~/paxauto_ws/install/setup.bash
    ros2 topic pub /obstacle_warning std_msgs/Bool '{data: true}'
    ```
3. Execute the commands for feeding input in new terminal
    ```bash
   source ~/paxauto_ws/install/setup.bash
    ros2 topic pub /planned_path nav_msgs/msg/Path "
    header:
      frame_id: 'map'
    poses:
    - header:
        frame_id: 'map'
      pose:
        position: {x: 1.0, y: 2.0, z: 0.0}
        orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
    " 
    ```
4. Execute the commands for feeding input in new terminal
    ```bash
    source ~/paxauto_ws/install/setup.bash
    ros2 topic pub /ackermann_drive_feedback ackermann_msgs/msg/AckermannDrive "
    steering_angle: 0.1
    steering_angle_velocity: 0.05
    speed: 2.0
    acceleration: 1.0
    jerk: 0.2
    "
    ```
5. Execute the commands for feeding input in new terminal
    ```bash
    source ~/paxauto_ws/install/setup.bash
    ros2 topic pub /lane_obstacle_traffic_signal_info custom_msgs/msg/LaneObstacleTrafficSignalArray "
    lane:
    - left_lane:
        points:
        - {x: 0.0, y: 0.0}
        - {x: 1.0, y: 1.0}
      right_lane:
        points:
        - {x: 2.0, y: 0.0}
        - {x: 3.0, y: 1.0}
      center_line:
        points:
        - {x: 1.0, y: 0.0}
        - {x: 2.0, y: 1.0}
      lane_width: 3.5
      confidence: 0.9
      stamp: {sec: 0, nanosec: 0}
      lane_markings: [1.0, 2.0]
      lane_type: 'solid'
      lane_confidence: 0.8
      lane_angle: 0.2
      curvature_radius: 15.0

    obstacles:
    - obstacle_id: 101
      distance: 5.5
      x: 2.0
      y: 3.0
    - obstacle_id: 102
      distance: 6.2
      x: 4.0
      y: 5.0

    traffic_signal_location: ['loc1', 'loc2']
    traffic_signal_status: ['RED', 'GREEN']
    "
    
    ```
6. Execute the commands for feeding Output in new terminal
    ```bash
    source ~/paxauto_ws/install/setup.bash
    ros2 topic echo /ackermann_drive
    ```
7. Open RQT in new terminal
    ```bash
    source ~/paxauto_ws/install/setup.bash
    rqt
    ```
8. Configure RQT

    Plugins -> Introspection -> Node Graph

    Plugins -> Topics -> Topic Monitor

9. Output in rqt should look like this: 
    
    ![rqt](assets/rqt1.jpeg)

    ![rqt](assets/rqt2.jpeg)

    ![rqt](assets/rqt3.jpeg)
