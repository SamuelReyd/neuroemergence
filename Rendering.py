import pygame
from pygame.locals import *

def render(window : pygame.Surface, ball: Ball, Plateform: plateform):
    window.fill((255,255,255))
    window.draw.rect(window, plateform.color, pygame.Rect(plateform.x, WINDOW_HEIGHT-plateform.width, plateform.length, plateform.width)
    window.draw.circle(window, ball.color, (int(ball.pos[0]), int(ball.pos[1])))
    
    pygame.display.update()