import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray, MultiArrayDimension
import cv2
import numpy as np
import signal
import sys


class zenithalCameraNode(Node):
	def __init__(self):
		super().__init__("zenithal_camera")
		self.camera_history = 1
		self.display = False
		self.img = None

		camera_qos_policy = rclpy.qos.QoSProfile(reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
														  history=rclpy.qos.HistoryPolicy.KEEP_LAST,
														  depth=self.camera_history)
		
		self.img_subscriber = self.create_subscription(Image, "/zenith_camera/image_raw", self.img_callback, camera_qos_policy)
		self.ball_publisher = self.create_publisher(Float32MultiArray, "balls_position", 10)

		self.create_timer(0.1, self.search_balls_and_robot)

		self.thresh = [30, 40]

	def img_callback(self, msg):
		self.img = np.array(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
		self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
		if self.display == True:
			cv2.imshow("Camera zenitale", self.img)
			cv2.waitKey(1)

	def search_balls_and_robot(self):
		"""Returns array of [X, Y, T] for each ball detected,T is the time since ball has spawned"""
		if self.img is not None:
			# yuv = cv2.cvtColor(self.img, cv2.COLOR_BGR2YUV)
			# cielab = cv2.cvtColor(self.img, cv2.COLOR_BGR2Lab)
			hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

			# self.fig = plot3dchans(hsv, "hsv", self.fig)
			thresholded = cv2.inRange(hsv[:,:,0], (self.thresh[0]), (self.thresh[1]))

			kernel = np.ones((9,9),np.uint8)
			closing = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)

			output = cv2.connectedComponentsWithStats(closing)
			(numLabels, labels, stats, centroids) = output


			if self.display == True:
				thresholded = cv2.cvtColor(thresholded, cv2.COLOR_GRAY2BGR)
				for centroid in centroids[1:]:
					cv2.circle(thresholded, (int(centroid[0]), int(centroid[1])), 2, (0, 0, 255), -1)

				cv2.imshow("closing", closing)
				cv2.imshow("thresholded", thresholded)
				cv2.waitKey(1)



			msg = Float32MultiArray()
			msg.layout.dim = [MultiArrayDimension(), MultiArrayDimension()]
			
			msg.data = [val for val in centroids[1:].flatten()]

			self.ball_publisher.publish(msg)

	def shutdown(self, sig, frame):
		sys.exit(0)

def main():
	rclpy.init()
	zen_cam_node = zenithalCameraNode()
	signal.signal(signal.SIGINT, zen_cam_node.shutdown)
	rclpy.spin(zen_cam_node)