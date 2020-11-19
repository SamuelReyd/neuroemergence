import numpy as np

from Constants import *

class Ball:
    def __init__(self, teta) :
        self.pos = np.array([WINDOW_WIDTH/2, WINDOW_HEIGHT/2]) #Ce sont des entiers
        self.speedNorm = 5
        self.speedDir = np.array([np.cos(teta), - np.sin(teta)]) # - cf convention axe
        self.rightAlpha = np.pi/5 #angle extremaux quand rebond sur planche
        self.leftAlpha = np.pi - self.rightAlpha
        self.alive = True
        self.color = [255, 0, 0]
        self.radius = 5
        self.score = 0
        self.bounceNb = 0
    
    def bounce(self, plateform) : #update le speedDir en fonction si touche un mur
        if self.alive :
            if (self.pos[0] <= 0 or self.pos[0] >= WINDOW_WIDTH) : #Collisition sur le mur de gauche, on change compo horizontale de la vitesse OU #Collisition sur le mur de droite , on change compo horizontale de la vitesse
                self.speedDir[0] = -self.speedDir[0]
                if (self.pos[0] <= 0) :
                    self.pos[0] = 0
                else :
                    self.pos[0] = WINDOW_WIDTH
            elif (self.pos[1] <= 0) : #Collisition sur le mur du haut, on change compo verticale de la vitesse
                self.speedDir[1] = -self.speedDir[1]
                self.pos[1] = 0
            elif (self.pos[1] >= WINDOW_HEIGHT) : #Rebondi sur la planchette ?
                if (plateform.pos <= self.pos[0] <= plateform.pos + plateform.length) :
                    self.bounceNb = self.bounceNb + 1
                    xOnPlateform = self.pos[0] - plateform.pos
                    teta = (self.rightAlpha - self.leftAlpha)/plateform.length * xOnPlateform + self.leftAlpha
                    self.speedDir = np.array([np.cos(teta), - np.sin(teta)])
                    self.pos[1] = WINDOW_HEIGHT
                else :
                    self.alive = False
                    self.score = BOUNCE_BONUS*self.bounceNb + DEATH_DISTANCE_BONUS*(1 - abs(self.pos[0] - (plateform.pos + plateform.length/2))/WINDOW_WIDTH)
    
    def update(self, plateform) :
        self.bounce(plateform) #Update speedDir et teste la mort
        if self.alive :
            self.pos = self.pos + self.speedNorm*self.speedDir
