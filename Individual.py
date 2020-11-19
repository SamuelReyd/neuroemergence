class Individual :
    def __init__(self, neuralNetwork, ball, plateform) :
        self.neuralNetwork = neuralNetwork
        self.ball = ball
        self.plateform = plateform
        self.score = 0