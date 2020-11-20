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
import pickle
import os

SHOW_RENDER = True
SAVE_BEST_PLAYER = True
SET_FPS = 500





pygame.display.init()
run = True

popSize = POPULATION_SIZE
mutationRate = MUTATION_RATE
crossoverNb = CROSSOVER_NUMBER
mutationScale = MUTATION_SCALE

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
population = GeneticAlgorithm(LAYERS_SIZES, popSize, mutationRate, crossoverNb, mutationScale)
teta = np.random.uniform(np.pi/4, 3*np.pi/4)
balls = [Ball(teta) for _ in range(popSize)]
plateforms = [Plateform() for _ in range(popSize)]
scores = np.zeros(popSize)

generation = 0
bestScores = list()
averageScores = list()
averageBounces = list()
maxBounces = list()
bestPlayer = None
bestPlayerBounces = 0

clock = pygame.time.Clock()
while run:
    if (SHOW_RENDER) :
        clock.tick(SET_FPS)
        render(window, balls, plateforms)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
                
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

            if balls[i].bounceNb > 20 : #On cappe le nombre de jongle max
                balls[i].calculeScore(plateforms[i])
                balls[i].alive = False

    if not still_any:
        for i in range(popSize) :
            scores[i] += balls[i].score - WALL_PENALITY * plateforms[i].score
        
        #Update bestPlayer :
        for i in range(popSize) :
            if balls[i].bounceNb > bestPlayerBounces :
                bestPlayer = population.population[i]
                bestPlayerBounces = balls[i].bounceNb
        
        #scores = 100/(np.amax(scores) - np.amin(scores)) * (scores - np.amin(scores))
        #scores[scores <= 0] = 0
        #population.update(scores + 0.01) #Pour eviter d'avoir tous les scores à 0 et diviser par 0
        population.update(100/(np.amax(scores) - np.amin(scores)) * (scores - np.amin(scores)) + 0.01)

        meanBounce = sum([balls[i].bounceNb for i in range(len(scores))])/len(scores)
        maxBounce = max([balls[i].bounceNb for i in range(len(scores))])
        if (generation % 5 == 0) : #Affiche de la meilleur matrice
            print("--- Generation : ", generation, " ---")
            for i in range(len(population.population[0].layers)) :
                print(population.population[np.argmax(scores)].layers[i])
            print("Nb rebond du score max : ", balls[np.argmax(scores)].bounceNb)
            print("Nb rebond max : ", maxBounce)
            print("Moyenne rebond : ", meanBounce)
            print("Record : ", bestPlayerBounces)
        averageBounces.append(meanBounce)
        maxBounces.append(maxBounce)
        bestScores.append(max(scores))
        averageScores.append(sum(scores)/len(scores))

        generation = generation + 1
        teta = np.random.uniform(np.pi/4, 3*np.pi/4)
        balls = [Ball(teta) for _ in range(popSize)]
        plateforms = [Plateform() for _ in range(popSize)]
        scores = np.zeros(popSize)

pathToFolder = PATH_TO_CONFIG[:-9]
resultNb = len(os.listdir(pathToFolder))
newFolderResult = pathToFolder + "/result" + str(resultNb)
os.mkdir(newFolderResult)

if SAVE_BEST_PLAYER :
    pickle.dump(bestPlayer, open(newFolderResult + "/bestPlayer", "wb"))

plt.plot(range(len(bestScores)), bestScores, label = "Best Scores")
plt.plot(range(len(averageScores)), averageScores, label = "Average Scores")
plt.plot(range(len(averageBounces)), averageBounces, label = "Average Bounces")
plt.plot(range(len(maxBounces)), maxBounces, label = "Max Bounces")
plt.legend()
plt.title('Results')
plt.savefig(newFolderResult + "/figure.png")
plt.show()