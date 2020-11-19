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
mutationRate = 0.05
crossoverNb = 2
mutationScale = 0.08


window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
population = GeneticAlgorithm((5,1), popSize, mutationRate, crossoverNb, mutationScale)
teta = np.random.uniform(np.pi/4, 3*np.pi/4)
balls = [Ball(teta) for _ in range(popSize)]
plateforms = [Plateform() for _ in range(popSize)]
scores = np.zeros(popSize)
t0 = time.time()

generation = 0
bestScores = list()
averageScores = list()




clock = pygame.time.Clock()
while run:
    #clock.tick(120)
    render(window, balls, plateforms)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            
        # if event.type == KEYDOWN:
        #     if event.key == K_LEFT:
        #         plateform.action_performed(-1)
        #     elif event.key == K_RIGHT:
        #         plateform.action_performed(1)
                
    if (time.time() - t0 > 10) :
        for i in range(popSize):
            balls[i].calculeScore(plateforms[i])
            balls[i].alive = False

    still_any = False
    for i in range(popSize):
        if balls[i].alive:
            scores[i] += FOLLOW_BALL_BONUS*(1 - abs(balls[i].pos[0] - (plateforms[i].pos + plateforms[i].length/2))/WINDOW_WIDTH)
            still_any = True
            
            input = [
            balls[i].speedDir[0], 
            balls[i].speedDir[1], 
            balls[i].pos[0]/WINDOW_WIDTH, 
            balls[i].pos[1]/WINDOW_HEIGHT,
            (plateforms[i].pos + plateforms[i].length/2)/WINDOW_WIDTH]
            #plateforms[i].speed/Plateform.limit_speed]
            
            output = population.population[i].feed_forward(input)
            if output < 0.49:
                plateforms[i].action_performed(-1)
            elif output > 0.51:
                plateforms[i].action_performed(1)
            plateforms[i].update()
            balls[i].update(plateforms[i])

    if not still_any:
        scores[i] += balls[i].score - WALL_PENALITY * plateforms[i].score
        #scores = 100/(np.amax(scores) - np.amin(scores)) * (scores - np.amin(scores))
        scores[scores <= 0] = 0
        population.update(scores + 0.01) #Pour eviter d'avoir tous les scores à 0 et diviser par 0
        if (generation % 5 == 0) : #Affiche de la meilleur matrice
            print("--- Generation : ", generation, " ---")
            for i in range(len(population.population[0].layers)) :
                print(population.population[np.argmax(scores)].layers[i])
            print("Nb rebond du score max : ", balls[np.argmax(scores)].bounceNb)
            print("Nb rebond max : ", max([balls[i].bounceNb for i in range(len(scores))]))
            print("Moyenne rebond : ", sum([balls[i].bounceNb for i in range(len(scores))])/len(scores))
        generation = generation + 1
        teta = np.random.uniform(np.pi/4, 3*np.pi/4)
        balls = [Ball(teta) for _ in range(popSize)]
        plateforms = [Plateform() for _ in range(popSize)]
        bestScores.append(max(scores))
        averageScores.append(sum(scores)/len(scores))
        scores = np.zeros(popSize)
        t0 = time.time()


plt.plot(range(len(bestScores)), bestScores)
plt.plot(range(len(averageScores)), averageScores)
plt.show()
    
    
                
