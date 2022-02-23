import cv2
import numpy as np
import matplotlib.pyplot as plt
from Zones import *
from time import sleep


class Map:
    def __init__(self,camera,name="Map",scale_percent=80):
        self.message=""
        self.__name=name
        self.__path = camera
        self.reload(scale_percent)


    def __str__(self, saved=False):
        cv2.imshow('image', self.img)
        cv2.waitKey(1)
        sleep(1)
        cv2.destroyAllWindows()
        self.message += "Une image a été affichée \n"

        if saved: self.save()

        return self.log()

    def reload(self,scale_percent=80):
        try:
            self.img = cv2.imread(self.__path, cv2.IMREAD_COLOR)
            assert str(type(self.img))=="<class 'numpy.ndarray'>"
            #print(self._img)
            self._width = int(self.img.shape[1] * scale_percent / 100)
            self._height = int(self.img.shape[0] * scale_percent / 100)
            dim = (self._width, self._height)
            self.img = cv2.resize(self.img, dim)
            self.message+= self.__path+" a bien été load!\n"

        except AssertionError:
            self.img=np.zeros((100,100,3))
            self.message+=" Une image n'a pas été trouvée, image par défaut attribuée, essayez de reload! Est-ce que le chemin est bien: "+self.__path + " ?"
            print(self.log())


    def hell_and_heaven(self,heaven_boxes=[np.array([[48,49],[165,147]]),np.array([[1306,675],[1423,774]])],
                        hell_boxes=[np.array([[0,0],[48,773]]),
                                    np.array([[0,773],[1425,824]]),
                                    np.array([[1424,48],[1475,824]]),
                                    np.array([[48,0],[1475,48]]),
                                    np.array([[731,120],[740,706]]),
                                    np.array([[165,46],[169,83]]),
                                    np.array([[48,148],[83,151]]),
                                    np.array([[1388,671],[1475,675]]),
                                    np.array([[1301,737],[1308,774]])]):
        self.goals=[Goal(heaven_boxes[i], name="Goal{}".format(i+1)) for i in range(len(heaven_boxes))]
        self.walls=[Wall(hell_boxes[i], name="Wall{}".format(i+1)) for i in range(len(hell_boxes))]
        for G in self.goals:
            G.display(self)

        for W in self.walls:
            W.display(self)

        self.save("Map_with_walls_and_goals.png")


    def crossing_point(self,objet,top_point=[735,83],bottom_point=[735,740]):
        if objet.center[1]>self._height/2:
            if objet.center[0] >  self._width/2:
                bottom_point[0]=bottom_point[0]-10
                return bottom_point
            else:
                bottom_point[0]=bottom_point[0]+10
                return bottom_point
        else:
            if objet.center[0] >  self._width/2:
                top_point[0]=top_point[0]-10
                return top_point
            else:
                top_point[0]=top_point[0]+10
                return top_point

    def save(self, filename = 'savedMap.png'):
        # Using cv2.imwrite() method
        # Saving the image
        cv2.imwrite(filename, self.img)
        self.message+=" Une image a été saved sous "+filename+" \n"
        print(self.log())

    def log(self):
        m=self.message
        self.message=""
        return m


if __name__=="__main__":
    nl="Tennis_camera_plafond.png"
    M=Map(nl)
    M.hell_and_heaven()
    M.__str__()