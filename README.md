# Neuroemergence
Project made during the course TP09 at Télécom Paris  
Teacher : Jean-Jouis Dessalles  
Team : Samuel Reyd - Thomas Poyet

## Optimization of a neural network by a genetic algorithm

The objective of this project is to teach a neural network how to play a juggling game by optimizing its weights and biaises with a genetic algorithm.

---

### How to use this project

This project runs with `python3.6` and uses `pygame`. To train the neural network, run the `main.py` file. You can set the config file in the `Constant.py` file. 
To see some previously trained player perform you can run the `showPlay.py` file and choose which one you want to see by setting the path of player pickle file in the code.

---

### The game

The game is composed of a plateform and of a ball. The player can move the plateform to the left or to the right by a certain number of pixels at each frame and the  ball bounces on the wall at a fixed speed. 
If the ball goes bellow the bottom of the screen, the game is considered lost. When the ball touches the plateform it bounces towards a direction depending on the spot where it touched the plaform.

---

### The learning algorithm

The game is played by an agent making decisions based on the output of a neural network which structure can be set in the confiuration file. The input are always 
the position and speed of the ball and the position of the plateform. The decision is to go left, if the output is lower than 0.49, to go right, if it is bigger than 0.51 and to do nothing otherwise. The neural network is initialized with random weights and biaises drawn in [-1,1] uniformly.

The learning process is performed by the genetic algorithm which is modeled by a population of brains whose genes are a flatten version of all its weights and biaises. The crossovers are performed directly on the flatten vectors. The mutation method depends on the parameter mutationScale: if less than zero then the gene is randomly reset else a quantity drawn uniformly in [-mutationSale, mutationScale] is added to the gene. 

---

### The results

The best individuals of each tested configuration is saved next to the image of the fitness curve that we obtained when we run this configuration, in a new folder within the folder of this configuration (config/confX).
