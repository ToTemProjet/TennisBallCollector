import rclpy
import time
import numpy as np
import os
from bot.roblib import*
import cv2
import argparse
import imutils
from rclpy.node import Node
from geometry_msgs.msg import  Twist, Vector3
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import LaserScan
from rclpy.qos import ReliabilityPolicy, QoSProfile
from cv_bridge import CvBridge, CvBridgeError
from gazebo_msgs.msg import ModelStates



class MyNode(Node):
    def __init__(self):
        super().__init__("robot_control")
        #self.lidar_sub =self.create_subscription(LaserScan,"/gpu_ray/laserScan",self.laser_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.camera_zen =self.create_subscription(Float32MultiArray,"/camera/balls_position",self.zen_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.robot_pos =self.create_subscription(Float32MultiArray,"/camera/robot_position",self.rb_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.cmd_pub_publisher=self.create_publisher(Twist,"cmd_vel",10)
        # self.poseSub = self.create_subscription(ModelStates,'/model_states',self.rb1_callback,QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT))
        self.x=0
        self.y=0
        self.dt=0.01
        self.dist=[]
        self.X=array([[0],[0],[1]])
        self.C=zeros((2,2))
        

    def zen_callback(self,scan):
        self.list_ball=array(scan.data).reshape(len(scan.data)//2,2)
        #print(self.list_ball)
        self.control(self.list_ball)

    def rb_callback(self,scan):
        self.X[0:2]=array(scan.data).reshape(2,1)


    def shutdown(self):
        rospy.loginfo("Stop Moving")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

    def f(self,x,u):
        θ=x[2,0]
        return array([[cos(θ)], [sin(θ)],[u]])


    def control(self,list_ball):

        m=self.X[0:2].flatten()
        move_cmd = Twist()
        self.dist=[]
        for i in list_ball:
            i=i.flatten()
            x_=self.X.flatten()
            d=sqrt((i[1]-x_[1])**2 + (i[0]-x_[0])**2)
            self.dist.append(d)

        if self.dist==[]:
            pass
        else:
            indice_min=self.dist.index(min(self.dist))
            obj=list_ball[indice_min]
            print("ball", obj)
            print("indice_min", indice_min)
            time.sleep(0.2)
            phi=arctan2(obj[1]-m[1],obj[0]-m[0])
            self.C[:,0]=(obj-m).T[0]
            self.C[:,1] = (m-m).T[0]
            e=det(self.C)/norm(obj-m)
            thetabar=phi-arctan(e)
            u=-arctan(tan((thetabar-self.X[2,0])/2))
            move_cmd.angular.z = u
            move_cmd.linear.x = cos(u)
            move_cmd.linear.y = sin(u)
            self.X[2,0]   += self.dt*move_cmd.linear.x
            self.X[2,0]   += self.dt*move_cmd.linear.y
            print(move_cmd.angular.z)
            self.cmd_pub_publisher.publish(move_cmd)
            # # if abs(obj[0]-m[0])<0.3:
            # #     pass

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    # node.control()
    rclpy.spin(node)