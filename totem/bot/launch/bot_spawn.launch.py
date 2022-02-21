import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node


ROS_DISTRO_ELOQUENT = "eloquent"
ROS_DISTRO_FOXY = "foxy"
ROS_DISTRO = os.environ.get("ROS_DISTRO")