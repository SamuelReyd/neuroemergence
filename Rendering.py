import pygame
from pygame.locals import *
from Constants import *

def render(window : pygame.Surface, balls, plateforms):
    window.fill((255,255,255))
    for ball, plateform in zip(balls, plateforms) :
        if ball.alive :
            pygame.draw.rect(window, plateform.color, pygame.Rect(plateform.pos, WINDOW_HEIGHT-plateform.width, plateform.length, plateform.width))
            pygame.draw.circle(window, ball.color, (int(ball.pos[0]), int(ball.pos[1])), ball.radius)
    
    pygame.display.update()