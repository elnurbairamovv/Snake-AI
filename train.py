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
    softmax = nn.Softmax(dim=1)                     # Softmax activation algorithm turns every prediction into a probability between 0 and 1. The sum total of the probabilities will add to 1
    logits = model(tensor)                          # raw unactivated predictions of the model
    activated_preds = softmax(logits)               # activate the predictions using softmax algorithm
    pred = torch.argmax(activated_preds)            # select the index of the prediction with the highest probability

    return int(pred)

while snake_0.running:
    snake_0.step(action=make_prediction(model=model, snake=snake_0))
    snake_0.draw()
    sleep(0.4)
