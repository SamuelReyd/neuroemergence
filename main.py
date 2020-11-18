import pygame
from pygame.locals import *
from Ball import Ball
from Plateform import Plateform
from Constants import *
from Rendering import render

pygame.display.init()
run = True

plateform = Plateform()
ball = Ball()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()

while run:
    clock.tick(30)
    render(window, ball, plateform)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                plateform.action_performed(-1)
            elif event.key == K_RIGHT:
                plateform.action_performed(1)
    
    plateform.update()
    ball.update(plateform)
                
