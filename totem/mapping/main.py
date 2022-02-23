from mapping import *
from Zone import *
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray, MultiArrayDimension

msg.data.reshape()

class Mapping(Node):
    def __init__(self,map):
        super().__init__("mapping")
        self.camera_history = 1
        self.display = False
        self.map = map
        self.__log_name="logger.csv"
        self.init_log_file()
        camera_qos_policy = rclpy.qos.QoSProfile(reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
                                                 history=rclpy.qos.HistoryPolicy.KEEP_LAST,
                                                 depth=self.camera_history)

        self.next_point_publisher = self.create_publisher(Float32MultiArray, "next_point", 10)
        self.img_subscriber = self.create_subscription(Image, "/zenith_camera/image_raw", self.img_callback,
                                                       camera_qos_policy)
        self.ball_subscriber = self.create_subscription(Float32MultiArray, "balls_position", self.balls_callback,10)
        self.robot_subscriber = self.create_subscription(Float32MultiArray, "robot_position", self.traitement,10)

    def img_callback(self, msg):
        img = np.array(msg.data, dtype=np.uint8).reshape((msg.height, msg.width, 3))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        scale_percent=80
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        img = cv2.resize(img, dim)
        self.map.img=img
        self.map.hell_and_heaven()
        if self.display == True:
            self.map.__str__(True)

    def balls_callback(self, msg):
        i=1
        self.LbA, self.LbB = [], []
        for b in msg.data.reshape():
            Tennisball=Ball(b[:2], "balle{}".format(i))
            Tennisball.assigne_partie()
            Tennisball.display(self.map)
            i += 1
            if Tennisball.partie()=="A":
                self.LbA.append(Tennisball)
            else: self.LbB.append(Tennisball)

    def robot_callback(self, msg):
        bot_data=msg.data.reshape()
        Rob=Robot(bot_data[:2],"Robot")
        Rob.assigne_partie()
        Rob.display(self.map)
        if Rob.partie()=="A"
            if len(self.LbA)==0:
                if len(self.LbB) > 0: Rob.passage()
                else: Rob.final_destination()
                cX_pdp,cY_pdp=Rob.next_point[0],Rob.next_point[1]
                msg = Float32MultiArray()
                msg.data = [float(cX_pdp), float(cY_pdp)]
                self.next_point_publisher.publish(msg)
            else:
                msg = Float32MultiArray()
                msg.data = [val for val in self.LbA]
                self.next_point_publisher.publish(msg)
        else:
            if len(self.LbB)==0:
                if len(self.LbA) > 0: Rob.passage()
                else: Rob.final_destination()
                cX_pdp, cY_pdp = Rob.next_point[0], Rob.next_point[1]
                msg = Float32MultiArray()
                msg.data = [float(cX_pdp), float(cY_pdp)]
                self.next_point_publisher.publish(msg)
            else:
                msg = Float32MultiArray()
                msg.data = [val for val in self.LbB]
                self.next_point_publisher.publish(msg)




        try:
            line = [u'{}'.format(bot_data[2]),u'{}'.format(bot_data[0]),u'{}'.format(bot_data[1])]
            f = open(self.__log_name, 'a')
            ligne = ",".join(line) + "\n"
            f.write(ligne)
            f.close()
        except:
            print("Error with the logger edition")
            pass



    def init_log_file(self):
        # Done: Créer le fichier log. Ajouter un header décrivant les éléments sauvegardés en .csv
        try:
            headers = [u'Time', u'Position X',u'Position Y']
            f = open(self.__log_name, 'w')
            ligneEntete = ",".join(headers) + "\n"
            f.write(ligneEntete)
            f.close()
        except:
            print("Error with the logger creation")
            pass



def main():
    nl="Tennis_camera_plafond.png"
    M=Map(nl)
    M.hell_and_heaven()
    rclpy.init()
    mapping_node = Mapping(M)
    signal.signal(signal.SIGINT, zen_cam_node.shutdown)
    rclpy.spin(zen_cam_node)