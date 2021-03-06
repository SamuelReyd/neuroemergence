import numpy as np

from NeuralNetwork import NeuralNetwork
from Constants import *

class GeneticAlgorithm :

    def __init__(self, vecSizes, popSize, mutationRate, crossoverNb, mutationScale) :
        self.popSize = popSize
        self.mutationRate = mutationRate
        self.crossoverNb = crossoverNb
        self.mutationScale = mutationScale
        self.population = [NeuralNetwork.get_random_neural_network(vecSizes) for i in range(popSize)]
        #self.population = [NeuralNetwork([np.array([[0, 0, 1, 0, -1, 0]])]) for i in range(popSize)]
    
    def crossover(self, neuralNetwork1, neuralNetwork2) :
        newLayers = []
        for layer1, layer2 in zip(neuralNetwork1.layers, neuralNetwork2.layers) :
            flatLayer1 = np.reshape(layer1, -1)
            flatLayer2 = np.reshape(layer2, -1)
            crossoverPoints = sorted(np.random.choice(np.arange(len(flatLayer1)), self.crossoverNb, replace = False))
            crossoverPoints = [0] + crossoverPoints
            crossoverPoints.append(len(flatLayer1))
            newFlatLayer = []
            for i in range(len(crossoverPoints) - 1) :
                if i % 2 == 0 :
                    newFlatLayer.extend(flatLayer1[crossoverPoints[i] : crossoverPoints[i+1]])
                else :
                    newFlatLayer.extend(flatLayer2[crossoverPoints[i] : crossoverPoints[i+1]])
            self.mutation(newFlatLayer)
            newLayers.append(np.reshape(np.array(newFlatLayer), layer1.shape))
        return NeuralNetwork(newLayers)

    def mutation(self, flatLayer) :
        for pos in range(len(flatLayer)) :
            if (np.random.rand() < self.mutationRate) :
                if (MUTATION_SCALE >= 0) :
                    flatLayer[pos] = flatLayer[pos] + self.mutationScale*np.random.uniform(-1, 1)
                else :
                    flatLayer[pos] = np.random.uniform(-1, 1)
            
    
    def update(self, scores) :
        newPop = []
        # for i in range(self.popSize) :
        #     parent1, parent2 = np.random.choice(self.population, 2, p = scores/np.sum(scores), replace = False)
        #     newPop.append(self.crossover(parent1, parent2))
        possibleParents = sorted(self.population, key=lambda x: scores[self.population.index(x)])[-NB_OF_CHOSEN:]
        newPop.extend(possibleParents)
        for _ in range(NB_OF_CHOSEN, self.popSize):
            father, mother = np.random.choice(possibleParents, 2)
            newPop.append(self.crossover(father, mother))
        self.population = newPop