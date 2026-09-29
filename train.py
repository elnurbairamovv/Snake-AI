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
            nn.Tanh(),
            nn.Linear(16, 16),
            nn.Tanh(),
            nn.Linear(16, 3)
        )

    
    def forward(self, x):
        x = self.flatten(x)
        logits = self.network_stack(x)          # get the raw values of output layer without using any activation function on the output layer

        return logits


def make_prediction(model: NeuralNetwork, snake: Snake) -> int:
    # pytorch requires inputs to the input layer to be a tensor so firstly turn the list object into a tensor object
    tensor = torch.tensor(snake.get_information()).unsqueeze(0)

    # out of all 3 predictions (straight, left, right) pick the prediction with the highest probability
    softmax = nn.Softmax(dim=1)                     # Softmax activation algorithm turns every prediction into a probability between 0 and 1. The sum total of the probabilities will add to 1
    logits = model(tensor)                          # raw unactivated predictions of the model
    activated_preds = softmax(logits)               # activate the predictions using softmax algorithm
    pred = torch.argmax(activated_preds)            # select the index of the prediction with the highest probability

    return int(pred)


def fitness_function(snake: Snake) -> float:
    return (snake.steps * snake.steps * pow(2, len(snake.snake)))


def main(pop_n: int) -> None:
    # initialize the population of snakes and the neural networks that each snake gets
    population = [(Snake(), NeuralNetwork()) for _ in range(pop_n)]
    curr_gen = 1

    while True:

        for snake, model in population:
            if snake.running:
                snake.step(action=make_prediction(model=model, snake=snake))

        if population_dead(population=population):  # check if every snake in the population is dead
            fitnesses = get_fitnesses(population=population)

            display_stats(fitnesses=fitnesses, curr_gen=curr_gen)

            break


def population_dead(population: list[tuple[Snake, NeuralNetwork]]) -> bool:
    all_dead = True                                 # use this variable to check if every snake is dead

    for snake, _ in population:
        if snake.running:
            all_dead = False                        # if at least one snake is alive then set all_dead = False and break because every snake is not dead
            break

    return all_dead


def display_stats(fitnesses: list[int], curr_gen: int) -> None:
    print("\n" + "=" * 14 + " Stats " + "=" * 14)
    print(f"Current Generation: {curr_gen}")
    print(f"Population Size: {len(fitnesses)}")
    print(f"Average Fitness: {(sum(fitnesses) / len(fitnesses)): 0.2f}")
    print(f"Best Fitness: {max(fitnesses)}")
    print(f"Worst Fitness: {min(fitnesses)}")
    print("=" * 35 + "\n")


def get_fitnesses(population: list[tuple[Snake, NeuralNetwork]]) -> list[int]:
    fitnesses = []

    for snake, _ in population:
        fitnesses.append(fitness_function(snake=snake))

    return fitnesses


# checks if the module is being accessed from train.py. doing this because I dont want train.py to mess up evaluate.py
if __name__ == "__main__":
    main(pop_n=100)
