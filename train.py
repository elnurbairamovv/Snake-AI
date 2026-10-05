# import the necessary libraries:
import torch
import torch.nn as nn
from snake import Snake
from time import sleep
import numpy as np
from random import randint


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


def main(pop_n: int, gen_n: int) -> None:
    # initialize the population of snakes and the neural networks that each snake gets
    population = [(Snake(), NeuralNetwork()) for _ in range(pop_n)]
    curr_gen = 1

    while curr_gen <= gen_n:

        for snake, model in population:
            if snake.running:
                snake.step(action=make_prediction(model=model, snake=snake))

        if population_dead(population=population):  # check if every snake in the population is dead
            fitnesses = get_fitnesses(population=population)

            display_stats(fitnesses=fitnesses, curr_gen=curr_gen)

            # TODO: breed the neural networks
            # 1. start with the selection process (done)
            population = selection(population)
            # 2. get the weights of each network
            weights, shapes = get_weights(population)
            # 3. finish the crossover function
            population = crossover(population, weights, shapes)
            # NOTE: if u want to update a network's weights manually then use model.fc.weight along with torch.no_grad()
            # also you'll prob have to do some experimentation with model.fc.weight

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
        snake.fitness = fitness_function(snake=snake)
        fitnesses.append(snake.fitness)

    return fitnesses


def selection(population: list[tuple[Snake, NeuralNetwork]]) -> list[tuple[Snake, NeuralNetwork]]:
    # sort the population based on each snake fitness
    population = sorted(population, key=lambda pop: pop[0].fitness, reverse=True)

    # slice the population to 20% its original size
    population = population[:int(0.2 * len(population))]

    return population


def get_weights(population: list[tuple[Snake, NeuralNetwork]]) -> tuple[list[list], list]:
    all_weights = []
    shapes = []

    for _, model in population:
        # collect the weights of each layer for an individual model into a list
        temp_weights = [param.detach().cpu().numpy().flatten() for param in model.parameters()]

        # concatenate all the weights into one big list
        temp_weights = np.concat(temp_weights)

        # append all the weights of one individual model to the list
        all_weights.append(temp_weights)

    # after i merge two parent weights together I'll have to reshape it to its original tensor shapes. in order to do that I have to save the original shapes
    # btw i already checked but, all the models have same shapes for their layers so i can just use the shape of the first model in the list
    for param in population[0][1].parameters():
        shapes.append(param.shape)

    return all_weights, shapes


def crossover(population: list[tuple[Snake, NeuralNetwork]]) -> list[tuple[Snake, NeuralNetwork]]:
    weights, shapes = get_weights(population)       # get the weights of every model but flatten them to make indexing easier and get their shapes so you can reshape them at the end

    child_weights = []

    for _ in range(np.ceil(len(weights) / 2)):
        # select the two parent weights. its okay to select with replacement
        parent_1_weight = weights[randint(0, len(weights) - 1)]
        parent_2_weight = weights[randint(0, len(weights) - 1)]

        # its fine to select either parent since the shapes are all the same. basically i am gonna merge two parent weights using slicing
        crossover_point = randint(0, parent_1_weight)

        child_1_weight = np.concat([parent_1_weight[crossover_point:], parent_2_weight[:crossover_point]])
        child_2_weight = np.concat([parent_2_weight[crossover_point:], parent_1_weight[:crossover_point]])

        child_weights.append(child_1_weight)
        child_weights.append(child_2_weight)

    for i in range(len(weights)):
        weights[i] = child_weights[i]

    for i, (snake, model) in enumerate(population):
        snake.reset()                               # reinitialize all the snakes

        

# checks if the module is being accessed from train.py. doing this because I dont want train.py to mess up evaluate.py
if __name__ == "__main__":
    main(pop_n=100, gen_n=20)
