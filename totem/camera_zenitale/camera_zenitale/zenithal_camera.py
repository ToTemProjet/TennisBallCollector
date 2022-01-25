import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
import numpy as np
import signal
import sys
from matplotlib import pyplot as plt


def plot3d(img, name, fig=None):
	# y, x = np.where(img>=0)
	# values = img[y, x]
	x, y = np.meshgrid(np.linspace(0, img.shape[1], img.shape[1]), np.linspace(0, img.shape[0], img.shape[0]))
	values = img
	print(y)
	print(y.shape)
	print(x.shape)
	print(img.shape)

	if fig == None:
		fig = plt.figure()
		ax = fig.gca(projection='3d')
	else:
		ax = fig.gca(projection='3d')
		ax.clear()
	ax.set_xlim3d(src.shape[1], 0)
	ax.set_ylim3d(0, src.shape[0])
	ax.plot_surface(x, y, values, cmap='viridis', edgecolor='none')

	ax.set_title(name)

	return fig

def plot3dchans(img, name, fig=None):
	img = np.where((np.sum(img, axis=2).reshape((img.shape[0], img.shape[1], 1))>0), img, np.nan)
	if fig == None:
		fig = plt.figure()
		ax = fig.gca(projection='3d')
	else:
		ax = fig.gca(projection='3d')
		ax.clear()
	ax.set_xlim3d(0, 255)
	ax.set_ylim3d(0, 255)
	ax.set_zlim3d(0, 255)
	ax.scatter(img[:,:,0], img[:,:,1], img[:,:,2], cmap='viridis', edgecolor='none')
	ax.set_title(name)
	return fig

def plot3dlabeled(img, name, labels, fig=None):
	colors = cm.viridis(np.linspace(0, 1, labels.max()+1))


	img = np.where((np.sum(img, axis=2).reshape((img.shape[0], img.shape[1], 1))>0), img, np.nan)
	if fig == None:
		fig = plt.figure()
		ax = fig.gca(projection='3d')
	else:
		ax = fig.gca(projection='3d')
		ax.clear()

	ax.set_xlim3d(0, 255)
	ax.set_ylim3d(0, 255)
	ax.set_zlim3d(0, 255)
	for i in range(0,labels.max()+1):
		subimage = img[np.where(labels==i)]
		ax.scatter(subimage[:,0], subimage[:,1], subimage[:,2], label= str(i))

	ax.set_title(name)
	ax.legend()

	return fig

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

		self.create_timer(0.1, self.search_balls_and_robot)

	def img_callback(self, msg):
		self.img = np.array(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
		self.img = cv2.cvtColor(self.img, cv2.COLOR_RGB2BGR)
		if self.display == True:
			cv2.imshow("Camera zenitale", self.img)
			cv2.waitKey(1)

	def search_balls_and_robot(self):
		"""Returns array of [X, Y, T] for each ball detected,T is the time since ball has spawned"""
		try:
			# yuv = cv2.cvtColor(self.img, cv2.COLOR_BGR2YUV)
			# cielab = cv2.cvtColor(self.img, cv2.COLOR_BGR2Lab)
			hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

			cv2.imshow("hsv", hsv)
			cv2.imshow("h", hsv[:, :, 0])
			cv2.imshow("s", hsv[:, :, 1]) #
			cv2.imshow("v2", hsv[:, :, 2])
			cv2.waitKey(1)

			# self.fig = plot3dchans(hsv, "hsv", self.fig)
		except:
			pass



	def shutdown(self, sig, frame):
		sys.exit(0)

def main():
	rclpy.init()
	zen_cam_node = zenithalCameraNode()
	signal.signal(signal.SIGINT, zen_cam_node.shutdown)
	rclpy.spin(zen_cam_node)