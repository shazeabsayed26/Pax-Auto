from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import LogInfo
import sys
 
 
def generate_launch_description():
    # task_arg = DeclareLaunchArgument( #LaunchArgument declaration is required to provide default value for 'task'.
    #     'task',  
    #     default_value='a',
    #     description='Task parameter to set the task'
    # )
    #colcon build --packages-select lane_detection_all localization path_planning user_authorization obstacle_detection custom_msgs etsi_its_cam_msgs v2x_transmitter pax_auto_main
    package_names = ["lane_detection_all","localization","path_planning","user_authorization","obstacle_detection", "v2x_transmitter", "lat_lon_control", "traffic_light_monitor", "firestore_bridge", "decision_core", "decoder", "ad_infrastructure_services", "ad_infrastructure_services"] 
    node_names = ["detection_node","localization_node","path_planner_node","user_authorization","obstacle_detection", "v2x_transmitter", "lat_lon_control", "traffic_light_monitor", "server", "decision_core", "decoder_node", "spatem_pubsub", "mqtt_override"]
 
    if len(package_names) != len(node_names):
        print("Error: The lengths of package_names and node_names are not the same!")
        sys.exit(1)
    ld =LaunchDescription()
    for i in range(len(package_names)):
 
        node_action = Node(
            package=package_names[i],
            executable=node_names[i],
            name=node_names[i],
            output='screen'
        )
        ld.add_action(node_action)
 
    LogInfo(msg="All nodes loaded successfully!")
 
    return ld
