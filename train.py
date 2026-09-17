# import the necessary libraries:
import torch
import torch.nn as nn
from snake import Snake


# create the neural network class
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()                      # inherit from nn.Module class
        self.flatten = nn.Flatten()             # this is used to turn a multidimensional tensor to a 1d tensor
        self.network_stack = nn.Sequential(     # intialize every layer and the activation functions
            nn.Linear(19, 16),
            nn.ReLU(),
            nn.Linear(16, 16),
            nn.ReLU(),
            nn.Linear(16, 4)
        )

    
    def forward(self, x):
        x = self.flatten(x)
        logits = self.network_stack(x)          # get the raw values of output layer without using any activation function on the output layer

        return logits



model = NeuralNetwork()

snake_0 = Snake()

while snake_0.running:
    print(snake_0.get_information())
