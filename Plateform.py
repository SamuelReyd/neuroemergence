from Constants import *

class Plateform:
    
    length = 60
    width = 2
    limit_speed = 5
    color = (0,0,255)
    
    def __init__(self):
        self.speed = 10
        self.pos = WINDOW_WIDTH/2
        self.score = 0 #compte quand colle bord
        
    def update(self):
        #self.pos += self.speed
        if (self.pos + self.length >= WINDOW_WIDTH) :
            self.pos = WINDOW_WIDTH - self.length
            self.score += 1
        elif (self.pos <= 0) :
            self.pos = 0
            self.score += 1
    
    def action_performed(self, dir: int):
        #self.speed += dir
        #self.speed = min(self.speed, self.limit_speed)
        #self.speed = max(self.speed, -self.limit_speed)
        self.pos += self.speed*dir
        
    