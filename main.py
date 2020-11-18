import pygame
from pygame.locals import *
from Ball import Ball
from Plateform import Plateform
from Constants import *
from Rendering import render
from GeneticAlgorithm import GeneticAlgorithm
import time
import matplotlib.pyplot as plt
import numpy as np

pygame.display.init()
run = True

popSize = 100


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
population = GeneticAlgorithm((6,8,1), popSize, 0.1, 2, 0.5)
balls = [Ball() for _ in range(popSize)]
plateforms = [Plateform() for _ in range(popSize)]
scores = np.zeros(popSize)
t0 = time.time()

bestScores = list()
averageScores = list()




clock = pygame.time.Clock()
while run:
    clock.tick(30)
    render(window, balls, plateforms)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            
        # if event.type == KEYDOWN:
        #     if event.key == K_LEFT:
        #         plateform.action_performed(-1)
        #     elif event.key == K_RIGHT:
        #         plateform.action_performed(1)
                
    still_any = False
    for i in range(popSize):
        if not balls[i].alive:
            scores[i] = time.time() - t0
        else:
            still_any = True
            
            input = [
            balls[i].speedDir[0], 
            balls[i].speedDir[1], 
            balls[i].pos[0]/WINDOW_WIDTH, 
            balls[i].pos[1]/WINDOW_HEIGHT,
            plateforms[i].pos/WINDOW_WIDTH,
            plateforms[i].speed/Plateform.limit_speed]
            
            output = population.population[i].feed_forward(input)
            if output < 0.4:
                plateforms[i].action_performed(-1)
            elif output > 0.6:
                plateforms[i].action_performed(1)
            plateforms[i].update()
            balls[i].update(plateforms[i])
    if not still_any:
        population.update(scores)
        balls = [Ball() for _ in range(popSize)]
        platforms = [Plateform() for _ in range(popSize)]
        bestScores.append(max(scores))
        averageScores.append(sum(scores)/len(scores))
        scores = np.zeros(popSize)
        t0 = time.time()

plt.plot(range(len(bestScores)), bestScores)
plt.plot(range(len(averageScores)), averageScores)
plt.show()
    
    
                
