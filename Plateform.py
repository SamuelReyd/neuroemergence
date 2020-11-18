from Constants import *

class Plateform:
    
    length = 30
    width = 2
    limit_speed = 5
    color = (0,0,255)
    
    def __init__(self):
        self.speed = 0
        self.pos = 0
        
    def update(self):
        self.pos += self.speed
        self.pos = min(self.pos, WINDOW_WIDTH - self.length)
        self.pos = max(self.pos, 0)
    
    def action_performed(self, dir: int):
        self.speed += dir
        self.speed = min(self.speed, self.limit_speed)
        self.speed = max(self.speed, -self.limit_speed)
        
    