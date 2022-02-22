import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    tennis_court_share = get_package_share_directory("tennis_court")
    gazebo_ros_share = get_package_share_directory("gazebo_ros")
    cam_zen_share = get_package_share_directory("camera_zenitale")
    desc_package = get_package_share_directory("bot")
    model_file = os.path.join(desc_package, "urdf", "bot.urdf")



    # A ne pas utiliser ici
    # os.system("ros2 service call /delete_entity 'gazebo_msgs/DeleteEntity'  '{name: totem}'")

    # Tennis court
    tennis_court_launch_file = os.path.join(tennis_court_share, "launch", "tennis_court.launch.py")
    tennis_court_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(tennis_court_launch_file)
        # launch_arguments={
        #     ROS_DISTRO
        # }.items()
    )

    # Zenital camera
    zen_cam = Node(
        package="camera_zenitale",
        output="screen",
        executable="zenithal_camera"
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher", executable="robot_state_publisher",
        parameters=[{"robot_description": Command(["xacro", " ", model_file])}]
        )

    gazebo_spawn_entity_node = Node(
        package="gazebo_ros", executable="spawn_entity.py",
        arguments=["-entity", "bot", "-topic", "/robot_description",
                    "-x", "0", "-y", "0", "-z", "0.95"],
        )

    # rqt_robot_steering_node = Node(
    #     package="rqt_robot_steering", executable="rqt_robot_steering"
    #     )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher"
        )


    return LaunchDescription([
        DeclareLaunchArgument(name="ROS_DISTRO", default_value="foxy"),
        tennis_court_launch,
        zen_cam,
        robot_state_publisher_node,
        gazebo_spawn_entity_node,
        # rqt_robot_steering_node,
        joint_state_publisher_node
    ])
