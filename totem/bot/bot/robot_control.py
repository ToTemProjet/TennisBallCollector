import rclpy
import time
import numpy as np
import cv2
import argparse
from rclpy.node import Node
from geometry_msgs.msg import  Twist, Vector3
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import LaserScan
from rclpy.qos import ReliabilityPolicy, QoSProfile
from cv_bridge import CvBridge, CvBridgeError


class MyNode(Node):
    def __init__(self):
        super().__init__("my_node")
        #self.lidar_sub =self.create_subscription(LaserScan,"/gpu_ray/laserScan",self.laser_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.camera_zen =self.create_subscription(Float32MultiArray,"/balls_position",self.zen_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.cmd_pub_publisher=self.create_publisher(Twist,"cmd_vel",10)
        self.x=0
        self.y=0

        
    def zen_callback(self,scan):
        self.x=scan.x
        # self.y=scan.data.y

        print(self.x)



    def laser_callback(self,scan):

        self.scan_param = [scan.angle_min*(np.pi/180), scan.angle_max*(np.pi/180), scan.angle_increment*(np.pi/180), scan.time_increment,
                           scan.scan_time, scan.range_min, scan. range_max]
        self.scan = np.array(scan.ranges)
        # print(self.scan[180])
        self.control(2)

    def shutdown(self):
        rospy.loginfo("Stop Moving")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)


def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    # node.control()
    rclpy.spin(node)


    
