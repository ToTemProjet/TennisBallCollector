import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray, MultiArrayDimension
import cv2
import numpy as np
import signal
import sys


class zenithalCameraNode(Node):
	def __init__(self, display=False):
		super().__init__("zenithal_camera")
		self.camera_history = 1
		self.display = display
		self.img = None

		camera_qos_policy = rclpy.qos.QoSProfile(reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
														  history=rclpy.qos.HistoryPolicy.KEEP_LAST,
														  depth=self.camera_history)
		
		self.img_subscriber = self.create_subscription(Image, "/zenith_camera/image_raw", self.img_callback, camera_qos_policy)
		self.ball_publisher = self.create_publisher(Float32MultiArray, "balls_position", 10)
		self.robot_publisher = self.create_publisher(Float32MultiArray, "robot_position", 10)

		self.create_timer(0.1, self.search_balls_and_robot)

		self.balls_thresh = [30, 40]
		self.bot_thresh = [(0, 120, 0),(10, 255, 255)]

	def img_callback(self, msg):
		self.img = np.array(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
		self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
		if self.display == True:
			cv2.imshow("Camera zenitale", self.img)
			cv2.waitKey(1)

	def search_balls_and_robot(self):
		"""Returns array of [X, Y, T] for each ball detected,T is the time since ball has spawned"""
		if self.img is not None:
			hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
			
			# Balls detection
			thresholded_balls = cv2.inRange(hsv[:,:,0], (self.balls_thresh[0]), (self.balls_thresh[1]))

			output = cv2.connectedComponentsWithStats(thresholded_balls)
			(numLabels, labels, stats, centroids_balls) = output

			# Robot detection
			thresholded_bot = cv2.inRange(hsv, (self.bot_thresh[0]), (self.bot_thresh[1]))

			contours, hierarchy = cv2.findContours(thresholded_bot, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

			M = cv2.moments(contours[1])
			cX_bot = int(M["m10"] / M["m00"])
			cY_bot = int(M["m01"] / M["m00"])

			# Affichage
			if self.display == True:
				thresholded_balls = cv2.cvtColor(thresholded_balls, cv2.COLOR_GRAY2BGR)
				for centroid in centroids_balls[1:]:
					cv2.circle(thresholded_balls, (int(centroid[0]), int(centroid[1])), 2, (0, 0, 255), -1)

				thresholded_bot = cv2.cvtColor(thresholded_bot, cv2.COLOR_GRAY2BGR)

				cv2.drawContours(thresholded_bot, contours, 1, (0,255,0), 2)
				colors = [(0, 0, 255), (0, 255, 0)]
				for i in range(len(contours)):
					M = cv2.moments(contours[i])
					cX = int(M["m10"] / M["m00"])
					cY = int(M["m01"] / M["m00"])

					cv2.circle(thresholded_bot, (cX, cY), 3, colors[i%2], -1)
				cv2.imshow("thresholded_balls", thresholded_balls)
				cv2.imshow("thresholded_bot", thresholded_bot)
				# cv2.imshow("edges", im2)
				cv2.waitKey(1)

			# Msg balle
			msg = Float32MultiArray()
			msg.data = [val for val in centroids_balls[1:].flatten()]
			self.ball_publisher.publish(msg)

			# Msg bot
			msg = Float32MultiArray()
			msg.data = [float(cX_bot), float(cY_bot)]
			self.robot_publisher.publish(msg)



	def shutdown(self, sig, frame):
		sys.exit(0)

def main():
	rclpy.init()
	zen_cam_node = zenithalCameraNode(False)
	signal.signal(signal.SIGINT, zen_cam_node.shutdown)
	rclpy.spin(zen_cam_node)