import rclpy
import numpy as np
from rclpy.node import Node
from geometry_msgs.msg import  Twist, Vector3
from std_msgs.msg import Float32MultiArray
from rclpy.qos import ReliabilityPolicy, QoSProfile
from sensor_msgs.msg import JointState

class BoxNodeControler(Node):
    def __init__(self):
        super().__init__("my_node")

        joint_state = JointState()

        self.create_timer(0.1, self.controler)

    def controler(self):
        # update joint_state
        now = self.get_clock().now()
        joint_state.header.stamp = now.to_msg()
        joint_state.name = ['front_panel_joint']
        # joint_state.position = []

    def shutdown(self):
        rospy.loginfo("Stop Moving")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)


def main():
	rclpy.init()
	box_node_controler = BoxNodeControler(False)
	signal.signal(signal.SIGINT, box_node_controler.shutdown)
	rclpy.spin(box_node_controler)