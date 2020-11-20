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

PATH_TO_PLAYER = "config/conf3/result1/bestPlayer"



pygame.display.init()
run = True

neuralNetwork = pickle.load(open(PATH_TO_PLAYER, "rb"))
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
teta = np.random.uniform(np.pi/4, 3*np.pi/4)
ball = Ball(teta)
bouncesScores = list()
plateform = Plateform()

clock = pygame.time.Clock()
while run:
    clock.tick(240)
    render(window, [ball], [plateform])
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    if ball.alive :
        input = [
        ball.speedDir[0], 
        ball.speedDir[1], 
        ball.pos[0]/WINDOW_WIDTH, 
        ball.pos[1]/WINDOW_HEIGHT,
        (plateform.pos + plateform.length/2)/WINDOW_WIDTH]
        
        output = neuralNetwork.feed_forward(input)
        if output < 0.49:
            plateform.action_performed(-1)
        elif output > 0.51:
            plateform.action_performed(1)
        plateform.update()
        ball.update(plateform)
    else :
        bouncesScores.append(ball.bounceNb)
        teta = np.random.uniform(np.pi/4, 3*np.pi/4)
        ball = Ball(teta)

plt.plot(range(len(bouncesScores)), bouncesScores, label = "Bounces")
plt.legend()
plt.title('Results')
plt.show()  