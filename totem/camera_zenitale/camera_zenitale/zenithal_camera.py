import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import numpy as np

class zenithalCameraNode(Node):
	def __init__(self):
		super().__init__("zenithal_camera")
		self.camera_history = 1

		camera_qos_policy = rclpy.qos.QoSProfile(reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
														  history=rclpy.qos.HistoryPolicy.KEEP_LAST,
														  depth=self.camera_history)
		
		self.img_subscriber = self.create_subscription(Image, "/zenith_camera/image_raw", self.img_callback, camera_qos_policy)

	def img_callback(self, msg):
		self.img = np.array(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
		self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
		cv2.imshow("test", self.img)
		cv2.waitKey(1)

def main():
	rclpy.init()
	zen_cam_node = zenithalCameraNode()
	rclpy.spin(zen_cam_node)