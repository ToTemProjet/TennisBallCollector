import cv2
import numpy as np
import matplotlib.pyplot as plt
from Zones import *


class Map:
    def __init__(self,new_light,name="Map",scale_percent=80):
        self.message=""
        self.__name=name
        self.reload(new_light,scale_percent)

    def __str__(self, saved=False):
        cv2.imshow('image', self._img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.message += "Une image a été affichée \n"

        if saved: self.save()

        return self.log()

    def reload(self, path,scale_percent=80):
        try:
            self._img = cv2.imread(path, cv2.IMREAD_COLOR)
            assert str(type(self._img))=="<class 'numpy.ndarray'>"
            #print(self._img)
            width = int(self._img.shape[1] * scale_percent / 100)
            height = int(self._img.shape[0] * scale_percent / 100)
            dim = (width, height)
            self._img = cv2.resize(self._img, dim)
            self.message+= path+" a bien été load!\n"

        except AssertionError:
            self._img=np.zeros((100,100,3))
            self.message+=" Une image n'a pas été trouvée, image par défaut attribuée, essayez de reload! Est-ce que le chemin est bien: "+path + " ?"
            print(self.log())


    def hell_and_heaven(self,heaven_boxes=[np.array([[48,49],[165,147]]),np.array([[1306,675],[1423,774]])]):
        for box in heaven_boxes:

            # i=box[0,0]
            # while i<=box[1,0]:
            #     j = box[0, 1]
            #     while j<=box[1,1]:
            #         self._img[j,i]=[250]*3
            #         j+=1
            #     i+=1


    def save(self, filename = 'savedMap.png'):
        # Using cv2.imwrite() method
        # Saving the image
        cv2.imwrite(filename, self._img)
        self.message+=" Une image a été saved sous "+filename+" \n"


    def log(self):
        m=self.message
        self.message=""
        return m


if __name__=="__main__":
    nl="Tennis_camera_plafond.png"
    M=Map(nl)
    print(M)