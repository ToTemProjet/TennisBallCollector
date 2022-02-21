import cv2
import numpy as np
import matplotlib.pyplot as plt



class Zone:
    def __init__(self, box_pix, type, name="1connu", partie="None"):
        avalaible_types=["ball","robot","wall","goal"]
        self.message=""
        self.__name=name
        self._blocked=False
        self._partie=partie
        try:
            self.__type=type
            assert type in avalaible_types
            self._box_pix=box_pix

        except AssertionError:
            self.message+= type+" est invalide! Choisissez parmis {}".format(avalaible_types)+"\n"
            print(self.log())

    def switch_access(self,position=None):
        if position==None:
            self._blocked= not self._blocked
            self.message += "La zone {} est passée dans la position {}!".format(self.__name, self._blocked) + "\n"
        elif position in [True,False] :
            self._blocked= position
            self.message += "La zone {} est passée dans la position {}!".format(self.__name, self._blocked) + "\n"
        else : self.message+= "La zone {} est restée dans la position {}! {} n'est pas un choix possible".format(self.__name,self._blocked,position)+"\n"
        print(self.log())

    def assigne_partie(self):
        try:
            if self._box_pix[:,1]>=735:
                self._partie="B"
            else:
                self._partie="A"
            self.message += "La zone {} est passée dans la partie {}!".format(self.__name, self._partie) + "\n"

        except :
            self.message += "Error! La zone {} est restée dans la partie {}!".format(self.__name, self._partie) + "\n"

        print(self.log())

    def __str__(self,map=None):
        pass


    def log(self):
        m=self.message
        self.message=""
        return m

class Wall(Zone):
    def __init__(self,box_pix,name="Wall1connu"):
        super().__init__(box_pix=box_pix,type="wall",name=name)
        self.switch_access(True)

    def __str__(self,map):
        try:
            img=

class Goal(Zone):
    def __init__(self,box_pix,name="Goal1connu"):
        super().__init__(box_pix=box_pix,type="goal",name=name)

class Ball(Zone):
    def __init__(self,box_pix,name="Ball1connu"):
        super().__init__(box_pix=box_pix,type="ball",name=name)

class Robot(Zone):
    def __init__(self,name="Robot1connu"):
        super().__init__(type="robot",name=name)

    def best_way(self,list_balls):
        pass

if __name__=="__main__":
    z=Zone("ball")
    print("Hye")