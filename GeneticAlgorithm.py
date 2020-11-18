import numpy as np

from NeuralNetwork import NeuralNetwork

class GeneticAlgorithm :

    def __init__(self, vecSizes, popSize, mutationRate, crossoverNb, mutationScale) :
        self.popSize = popSize
        self.mutationRate = mutationRate
        self.crossoverNb = crossoverNb
        self.mutationScale = mutationScale
        self.population = [NeuralNetwork.get_random_neural_network(vecSizes) for i in popSize]
    
    def crossover(self, neuralNetwork1, neuralNetwork2) :
        newLayers = []
        for layer1, layer2 in zip(neuralNetwork1.layers, neuralNetwork2.layers) :
            flatLayer1 = np.reshape(layer1, -1)
            flatLayer2 = np.reshape(layer2, -1)
            crossoverPoints = sorted(np.random.choice(np.arange(len(flatLayer1)), self.crossoverNb))
            crossoverPoints = [0] + crossoverPoints
            crossoverPoints.append(len(flatLayer1) - 1)
            newFlatLayer = []
            for i in range(len(crossoverPoints) - 1) :
                if i % 2 == 0 :
                    newFlatLayer.extend(flatLayer1[crossoverPoints[i] : crossoverPoints[i+1]])
                else :
                    newFlatLayer.extend(flatLayer2[crossoverPoints[i] : crossoverPoints[i+1]])
            newLayers.append(np.reshape(np.array(newFlatLayer), layer1.shape))
        return NeuralNetwork(newLayers)

    def mutation(self, neuralNetwork) :
        for layer in neuralNetwork.layers :
            for pos in np.random.choice([[i, j] for i in range(layer.shape[0]) for j in range(layer.shape[1])], int(self.mutationRate*layer.shape[0]*layer.shape[1])) :
                layer[pos] = layer[pos] + self.mutationScale*np.random.uniform(-1, 1)
    
    def update(self, scores) :
        newPop = []
        for i in range(self.popSize) :
            parent1, parent2 = np.random.choice(self.population, 2, p = scores/np.sum(scores))
            newPop.append(self.crossover(parent1, parent2))
            self.mutation(newPop[i])
        self.population = newPop