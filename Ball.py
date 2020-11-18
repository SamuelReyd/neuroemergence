import numpy as np
import random as rd

from Constants import *

class Ball:
    def __init__(self) :
        self.pos = np.array([WINDOW_WIDTH/2, WINDOW_HEIGHT/2]) #Ce sont des entiers
        teta = 2*np.pi*rd.random()
        self.speed = np.array([np.cos(teta), - np.sin(teta)]) # - cf convention axe
        self.rightAlpha = np.pi/5 #angle extremaux quand rebond sur planche
        self.leftAlpha = np.pi - self.rightAlpha
        self.alive = True
        self.color = [255, 0, 0]
    
    def bounce(self, plateform) : #update le speed en fonction si touche un mur
        if (self.pos[1] <= 0 or self.pos[1] >= WINDOW_WIDTH) : #Collisition sur le mur de gauche, on change compo horizontale de la vitesse OU #Collisition sur le mur de droite , on change compo horizontale de la vitesse
            self.speed[1] = -self.speed[1]
        elif (self.pos[0] <= 0) : #Collisition sur le mur du haut, on change compo verticale de la vitesse
            self.speed[0] = -self.speed[0]
        elif (self.pos[1] >= WINDOW_HEIGHT) : #Rebondi sur la planchette ?
            if (plateform.pos <= self.pos[0] <= plateform.pos + plateform.length) :
                xOnPlateform = self.pos[0] - plateform.pos
                teta = (self.rightAlpha - self.leftAlpha)/plateform.length * xOnPlateform + self.leftAlpha
                self.speed = [np.cos(teta), - np.sin(teta)]
            else :
                self.alive = False
    
    def update(self, plateform) :
        self.bounce(plateform) #Update speed et teste la mort
        if self.alive :
            self.pos = self.pos + self.speed
