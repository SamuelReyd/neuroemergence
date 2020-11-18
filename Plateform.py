import numpy as np

class Plateform:
    
    length = 30
    width = 2
    limit_speed = 5
    
    def __init__(self):
        self.speed = 0
        self.x = 0
        
    def update(self):
        self.pos += self.speed
        self.pos = min(self.pos, WINDOW_WIDTH)
        self.pos = max(self.pos, 0)
    
    def action_performed(dir: int):
        speed += dir
        self.speed = min(self.speed, self.limit_speed)
        self.speed = max(self.speed, -self.limit_speed)
        
    