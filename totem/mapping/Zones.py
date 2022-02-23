import cv2
import numpy as np
from math import hypot


class Zone:
    def __init__(self, box_pix, type, name="1connu", partie="None"):
        avalaible_types=["ball","robot","wall","goal"]
        self.message=name+'\n'
        self.__name=name
        self._blocked=False
        self._partie=partie
        self.assigne_partie()
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

    def partie(self):
        return self._partie

    def __str__(self):
        print(self.__name)
        print(self.__type)
        print(self._partie)
        print(self.log())


    def log(self):
        m=self.message
        self.message=""
        return m

class Wall(Zone):
    def __init__(self,box_pix,name="Wall1connu"):
        super().__init__(box_pix=box_pix,type="wall",name=name)
        self.switch_access(True)


    def display(self,map,saved=False):
        try:
            for i in range(self._box_pix[0,0],self._box_pix[1,0]):
                for j in range(self._box_pix[0, 1], self._box_pix[1, 1]):
                    map.img[j,i]=[0]*3
            self.message += "Des murs ont été ajouté" + "\n"
            if saved:
                map.save()
                self.message += "Une nouvelle map a été sauvée" + "\n"
        except:
            self.message += "Mur non ajouté! L'objet map est peut être inadaptée!" + "\n"
        print(self.log())



class Goal(Zone):
    def __init__(self,box_pix,name="Goal1connu"):
        super().__init__(box_pix=box_pix,type="goal",name=name)
        self.center=np.array([[(box_pix[0,0]+box_pix[1,0])//2],[(box_pix[0,1]+box_pix[1,1])//2]])

    def display(self,map,saved=False):
        try:
            for i in range(self._box_pix[0,0],self._box_pix[1,0]):
                for j in range(self._box_pix[0, 1], self._box_pix[1, 1]):
                    map.img[j,i]=[255]*3
            self.message += "Un nouvel objectif a été ajouté" + "\n"
            if saved:
                map.save()
                self.message += "Une nouvelle map a été sauvée" + "\n"
        except:
            self.message += "Aucun nouvel objectif ajouté! L'objet map est peut être inadaptée!" + "\n"
        print(self.log())

class Ball(Zone):
    def __init__(self,center,name="Ball1connu"):
        self._center = center
        box_pix=np.array([[center[0]-1,center[1]-1],[center[0]+1,center[1]+1]])
        super().__init__(box_pix=box_pix,type="ball",name=name)

    def Is_ball_on_other(self,Zone):
        if self._center[0] in range(Zone._box_pix[0]) and self._center[1] in range(Zone._box_pix[1]):
            return True
        return False

    def display(self,map,saved=False):
        try:
            for i in [self._box_pix[0,0],self._box_pix[1,0]]:
                for j in range(self._box_pix[0, 1], self._box_pix[1, 1]):
                    map.img[[j,i]]=[0,255,255]
            for j in [self._box_pix[0, 1], self._box_pix[1, 1]]:
                for i in range(self._box_pix[0,0],self._box_pix[1,0]):
                    map.img[[j,i]] = [0, 255, 255]
            self.message += "Une balle a été ajouté" + "\n"
            if saved:
                map.save()
                self.message += "Une nouvelle map a été sauvée" + "\n"
        except:
            self.message += "Aucune nouvelle balle ajouté! L'objet map est peut être inadaptée!" + "\n"
        print(self.log())

class Robot(Zone):
    def __init__(self,box_pix,name="Robot1connu"):
        super().__init__(box_pix=box_pix, type="robot",name=name)
        self.pos=[(box_pix[1,0]+box_pix[0,0])//2,(box_pix[1,1]+box_pix[0,1])//2]
        self.next_point=self.pos
    def display(self,map,saved=False):
        try:
            for i in [self._box_pix[0,0],self._box_pix[1,0]]:
                for j in range(self._box_pix[0, 1], self._box_pix[1, 1]):
                    map.img[[j,i]]=[255, 255, 0]
            for j in [self._box_pix[0, 1], self._box_pix[1, 1]]:
                for i in range(self._box_pix[0,0],self._box_pix[1,0]):
                    map.img[[j,i]] = [255, 255, 0]
            map.__str__(saved)
            self.message += "Le robot a été ajouté" + "\n"
            if saved:
                map.save()
                self.message += "Une nouvelle map a été sauvée" + "\n"
        except:
            self.message += "Aucun robot ajouté! L'objet map est peut être inadaptée!" + "\n"
        print(self.log())

    # def nearest(self,list_balls,list_balls_other):#separer les balles en fonction partie A ou B
    #     if len(list_balls) > 0 :
    #         length=np.inf
    #         for lb in list_balls:
    #             lgh = hypot(lb.center[0] - pos[0], lb.center[1] - pos[1])
    #             if lgh<length:
    #                 length=lgh
    #                 self.next_point=lb
    #     else:
    #         if len(list_balls_other) > 0: self.passage()
    #         else: self.final_destination()

    def passage(self,map):
        self.next_point=crossing_point(map,self)

    def final_destination(self,map):
        for g in map.goal:
            if g._partie==self._partie:
                self.next_point=g.center.flatten()
                pass


    def go_to_point(self):
        pass

if __name__=="__main__":
    z=Zone("ball")
    print("Hye")