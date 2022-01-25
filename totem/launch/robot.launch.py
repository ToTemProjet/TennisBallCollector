import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node


# ROS_DISTRO_ELOQUENT = "eloquent"
# ROS_DISTRO_FOXY = "foxy"
# ROS_DISTRO_GALACTIC = "galactic"
# ROS_DISTRO = os.environ.get("ROS_DISTRO")

def generate_launch_description():
    tennis_court_share = get_package_share_directory("tennis_court")
    gazebo_ros_share = get_package_share_directory("gazebo_ros")
    cam_zen_share = get_package_share_directory("camera_zenitale")

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

    return LaunchDescription([
        DeclareLaunchArgument(name="ROS_DISTRO", default_value="foxy"),
        tennis_court_launch,
        zen_cam
    ])