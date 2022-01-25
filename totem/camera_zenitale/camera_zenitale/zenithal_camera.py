import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import numpy as np


class zenithalCameraNode(Node):
	def __init__(self):
		super().__init__("zenithal_camera")
		self.camera_history = 1
		self.display = False

		camera_qos_policy = rclpy.qos.QoSProfile(reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
														  history=rclpy.qos.HistoryPolicy.KEEP_LAST,
														  depth=self.camera_history)
		
		self.img_subscriber = self.create_subscription(Image, "/zenith_camera/image_raw", self.img_callback, camera_qos_policy)

	def img_callback(self, msg):
		self.img = np.array(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
		self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
		if self.display == True:
			cv2.imshow("Camera zenitale", self.img)
			cv2.waitKey(1)

	def serachBalls(self):
		"""Returns array of [X, Y, T] for each ball detected,T is the time since ball has spawned"""
		


		pass

	def shutdown(self, sig, frame):
		sys.exit(0)

def main():
	rclpy.init()
	zen_cam_node = zenithalCameraNode()
	signal.signal(signal.SIGINT, zen_cam_node.shutdown)
	rclpy.spin(zen_cam_node)