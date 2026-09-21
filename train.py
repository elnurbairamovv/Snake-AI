# import the necessary libraries:
import torch
import torch.nn as nn
from snake import Snake
from time import sleep


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
            nn.Linear(16, 3)
        )

    
    def forward(self, x):
        x = self.flatten(x)
        logits = self.network_stack(x)          # get the raw values of output layer without using any activation function on the output layer

        return logits



model = NeuralNetwork()

snake_0 = Snake()


def make_prediction(model: NeuralNetwork, snake: Snake) -> int:
    # pytorch requires inputs to the input layer to be a tensor so firstly turn the list object into a tensor object
    tensor = torch.tensor(snake.get_information()).unsqueeze(0)

    # out of all 3 predictions (straight, left, right) pick the prediction with the highest probability
    pred = torch.argmax(model(tensor))

# while snake_0.running:
#     print(snake_0.get_information())
#     snake_0.draw()


make_prediction(model=model, snake=snake_0)
