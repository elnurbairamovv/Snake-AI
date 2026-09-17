# import the necessary libraries:
import pygame
from random import randint


# TODO: draw the board to see how the neural network is doing
# at the end of the project try to add more features to remove some repetitive stuff


class Snake:
    # Constant variables:
    GAME_WIDTH = 1000
    GAME_HEIGHT = 1000
    TILE_SIZE = 50
    ROWS = int(GAME_HEIGHT / TILE_SIZE)
    COLUMNS = int(GAME_WIDTH / TILE_SIZE)
    WHITE = (200, 200, 200)
    BLACK = (0, 0, 0)
    RED = (255, 116, 108)
    GREEN = (193, 225, 193)
    SNAKE_X = 10 * TILE_SIZE                    # initial x position of snake's head will be a fixed constant
    SNAKE_Y = 10 * TILE_SIZE                    # initial y position of snake's head will be a fixed constant

    def __init__(self):
        self.reset()                            # initialize instance variables using reset method


    def step(self, action: int) -> list:
        self.apply_action(action)               # change the snake's velocity given the network's input

        self.update_body()                      # update each part in snake's body

        self.food_collision()                   # check if snake collides with food

        self.border_collision()                 # check if snake collides with border

        self.body_collision()                   # check if snake's head collides with snake's body

        self.starvation()                       # check if the snake hasn't eaten in a long time

        return self.get_information()           # get the board state and return it. this information will be the input layer of the network


    def apply_action(self, action: int) -> None:
        if action == 0 and self.velocity != (0, Snake.TILE_SIZE):
            self.velocity = (0, -Snake.TILE_SIZE)
        elif action == 1 and self.velocity != (0, -Snake.TILE_SIZE):
            self.velocity = (0, Snake.TILE_SIZE)
        elif action == 2 and self.velocity != (-Snake.TILE_SIZE, 0):
            self.velocity = (Snake.TILE_SIZE, 0)
        elif action == 3 and self.velocity != (Snake.TILE_SIZE, 0):
            self.velocity = (-Snake.TILE_SIZE, 0)


    def update_body(self) -> None:
        old_positions = [snake_part.copy() for snake_part in self.snake]
        self.snake[0].move_ip(self.velocity)

        for i in range(1, len(self.snake)):
            self.snake[i] = old_positions[i - 1]


    def food_collision(self) -> None:
        if self.snake[0].center == self.food:
            self.snake.append(self.food)
            # generate a new food in the board        
            food_x, food_y = self.get_random_pos()
            self.food = pygame.Rect(food_x, food_y, Snake.TILE_SIZE, Snake.TILE_SIZE)
            self.steps_since_eaten = 0
        else:
            self.steps_since_eaten += 1


    def border_collision(self) -> None:
        if self.snake[0].x == Snake.GAME_WIDTH or self.snake[0].y == Snake.GAME_HEIGHT or self.snake[0].x == -Snake.TILE_SIZE or self.snake[0].y == -Snake.TILE_SIZE:
            self.running = False                # if the snake collides with the border then end the game
    

    def body_collision(self) -> None:
        if self.snake[0] in self.snake[1:]:
            self.running = False                # if the snake's head collides with the snake's body then end the game

            
    def starvation(self) -> None:
        if self.steps_since_eaten >= 100:
            self.running = False                # end the game if the snake hasn't eaten in a long time


    def get_random_pos(self) -> tuple[float, float]:
        random_x, random_y = (randint(0, Snake.COLUMNS - 1) * Snake.TILE_SIZE, randint(0, Snake.ROWS - 1) * Snake.TILE_SIZE)
        
        while (pygame.Rect(random_x, random_y, Snake.TILE_SIZE, Snake.TILE_SIZE) in self.snake):
            random_x, random_y = (randint(0, Snake.COLUMNS - 1) * Snake.TILE_SIZE, randint(0, Snake.ROWS - 1) * Snake.TILE_SIZE)
    
        return random_x, random_y


    def reset(self) -> None:
        # snake is going to be a list because it is made up of many rectangles
        self.snake = [pygame.Rect(Snake.SNAKE_X, Snake.SNAKE_Y, Snake.TILE_SIZE, Snake.TILE_SIZE)]
        # the velocity of the snake's head
        self.velocity = (0, 0)

        # generate random x position and y position for the food such that it doesn't overlap with where the snake is
        food_x, food_y = self.get_random_pos()
        self.food = pygame.Rect(food_x, food_y, Snake.TILE_SIZE, Snake.TILE_SIZE)

        # this variable controls whether the game is running or not running
        self.running = True

        # this variable is to check how many steps the snake has taken since having eaten
        self.steps_since_eaten = 0


    def draw(self) -> None:
        pass


    def get_information(self) -> None:
        information = [0.0 for _ in range(19)]
        # Snake's head direction information: Do one hot encoding based on which direction the snake's head is moving
        # You can skip one of the directions because it is redundant since the degrees of freedom for direction is 3, this would be the approach IF my snake started automatically moving from the start
        # Which means, you cant skip any of the directions because they are all needed. At the start all the directions are 0 which means the degrees of freedom has to be 4 for direction
        if self.velocity == (0, -Snake.TILE_SIZE):
            information[0] = 1.0               # snake is heading up
        elif self.velocity == (0, Snake.TILE_SIZE):
            information[1] = 1.0               # snake is heading down
        elif self.velocity == (-Snake.TILE_SIZE, 0):
            information[2] = 1.0               # snake is heading left
        elif self.velocity == (Snake.TILE_SIZE, 0):
            information[3] = 1.0               # snake is heading right

        # Food direction information: Do one hot encoding again but for food this time
        # You cant skip any of the directions for food. The food might be above the snake's head but you also have to know if its to your right or to your left or neither. dof is 4
        if self.food.y < self.snake[0].y:
            information[4] = 1.0               # snake is below food
        if self.food.y > self.snake[0].y:
            information[5] = 1.0               # snake is above food
        if self.food.x < self.snake[0].x:
            information[6] = 1.0               # snake is to the right of food
        if self.food.x > self.snake[0].x:
            information[7] = 1.0               # snake is to the left of food

        # Danger information: Do one hot encoding again but for the immediate danger to the snake's head (e.g border and body part)
        # straight, left, right
        if information[0] == 1:                # if snake is heading up then the borders are top border, left border, and right border              
            if ((self.snake[0].y == 0) or
                (self.snake[0].move(0, -Snake.TILE_SIZE)) in self.snake[1:]):
                information[8] = 1.0           # immediate danger straight ahead
            if ((self.snake[0].x == 0) or
                (self.snake[0].move(-Snake.TILE_SIZE, 0)) in self.snake[1:]):
                information[9] = 1.0           # immediate danger to the left
            if ((self.snake[0].x + Snake.TILE_SIZE) == Snake.GAME_WIDTH or
                (self.snake[0].move(Snake.TILE_SIZE, 0)) in self.snake[1:]):
                information[10] = 1.0          # immediate danger to the right

        elif information[1] == 1:              # if snake is heading down then the borders are down border, right border, and left border
            if ((self.snake[0].y + Snake.TILE_SIZE) == Snake.GAME_HEIGHT or
                (self.snake[0].move(0, Snake.TILE_SIZE)) in self.snake[1:]):
                information[8] = 1.0           # immediate danger straight ahead
            if ((self.snake[0].x + Snake.TILE_SIZE) == Snake.GAME_WIDTH or
                (self.snake[0].move(Snake.TILE_SIZE, 0)) in self.snake[1:]):
                information[9] = 1.0           # immediate danger to the left
            if ((self.snake[0].x == 0) or
                (self.snake[0].move(-Snake.TILE_SIZE, 0)) in self.snake[1:]):
                information[10] = 1.0          # immediate danger to the right

        elif information[2] == 1:              # if snake is heading left then the borders are left border, bottom border, and top border
            if ((self.snake[0].x == 0) or
                (self.snake[0].move(-Snake.TILE_SIZE, 0)) in self.snake[1:]):
                information[8] = 1.0           # immediate danger straight ahead
            if ((self.snake[0].y + Snake.TILE_SIZE) == Snake.GAME_HEIGHT or
                (self.snake[0].move(0, Snake.TILE_SIZE)) in self.snake[1:]):
                information[9] = 1.0           # immediate danger to the left
            if ((self.snake[0].y == 0) or
                (self.snake[0].move(0, -Snake.TILE_SIZE)) in self.snake[1:]):
                information[10] = 1.0          # immediate danger to the right
            
        elif information[3] == 1:              # if snake is heading right then the borders are right border, top border, and bottom border
            if ((self.snake[0].x + Snake.TILE_SIZE) == Snake.GAME_WIDTH or
                (self.snake[0].move(Snake.TILE_SIZE, 0)) in self.snake[1:]):
                information[8] = 1.0           # immediate danger straight ahead
            if ((self.snake[0].y == 0) or
                (self.snake[0].move(0, -Snake.TILE_SIZE)) in self.snake[1:]):
                information[9] = 1.0           # immediate danger to the left
            if ((self.snake[0].y + Snake.TILE_SIZE) == Snake.GAME_HEIGHT or
                (self.snake[0].move(0, Snake.TILE_SIZE)) in self.snake[1:]):
                information[10] = 1.0          # immediate danger to the right

        # Danger information 2: Instead of ohe i will use distance of the border to the snake's head relative to the direction snake is going
        # straight, left, right
        if information[0] == 1:                # if snake is heading up then the borders are top border, left border, and right border
            information[11] = (self.snake[0].y - 0) / Snake.GAME_HEIGHT
            information[12] = (self.snake[0].x - 0) / Snake.GAME_WIDTH
            information[13] = (1000 - self.snake[0].x) / Snake.GAME_WIDTH

        elif information[1] == 1:              # if snake is heading down then the borders are down border, right border, and left border
            information[11] = (1000 - self.snake[0].y) / Snake.GAME_HEIGHT
            information[12] = (1000 - self.snake[0].x) / Snake.GAME_WIDTH
            information[13] = (self.snake[0].x - 0) / Snake.GAME_WIDTH

        elif information[2] == 1:              # if snake is heading left then the borders are left border, bottom border, and top border
            information[11] = (self.snake[0].x - 0) / Snake.GAME_WIDTH
            information[12] = (1000 - self.snake[0].y) / Snake.GAME_HEIGHT
            information[13] = (self.snake[0].y - 0) / Snake.GAME_HEIGHT

        elif information[3] == 1:              # if snake is heading right then the borders are right border, top border, and bottom border
            information[11] = (1000 - self.snake[0].x) / Snake.GAME_WIDTH
            information[12] = (self.snake[0].y - 0) / Snake.GAME_HEIGHT
            information[13] = (1000 - self.snake[0].y) / Snake.GAME_HEIGHT


        # Danger information 3: i will use distance to the closest body part from relative direction to snake's head
        # straight, left, right
        if information[0] == 1:                # if snake is heading up then the body parts are top part, left part, and right part
            for i in range(0, Snake.GAME_HEIGHT, Snake.TILE_SIZE):
                if (self.snake[0].move(0, -i) in self.snake[1:]):
                    information[14] = (self.snake[0].y - i) / Snake.GAME_HEIGHT  # distance to the body part straight ahead
                    break
            for i in range(0, Snake.GAME_WIDTH, Snake.TILE_SIZE):
                if (self.snake[0].move(-i, 0) in self.snake[1:]):
                    information[15] = (self.snake[0].x - i) / Snake.GAME_WIDTH   # distance to the body part at left
                    break
            for i in range(0, Snake.GAME_WIDTH, Snake.TILE_SIZE):
                if (self.snake[0].move(i, 0) in self.snake[1:]):
                    information[16] = (i - self.snake[0].x) / Snake.GAME_WIDTH   # distance to the body part at right
                    break

        elif information[1] == 1:              # if snake is heading down then the body parts are down part, right part, and left part
            for i in range(0, Snake.GAME_HEIGHT, Snake.TILE_SIZE):
                if (self.snake[0].move(0, i) in self.snake[1:]):
                    information[14] = (i - self.snake[0].y) / Snake.GAME_HEIGHT  # distance to the body part straight ahead
                    break
            for i in range(0, Snake.GAME_WIDTH, Snake.TILE_SIZE):
                if (self.snake[0].move(i, 0) in self.snake[1:]):
                    information[15] = (i - self.snake[0].x) / Snake.GAME_WIDTH   # distance to the body part at left
                    break
            for i in range(0, Snake.GAME_WIDTH, Snake.TILE_SIZE):
                if (self.snake[0].move(-i, 0) in self.snake[1:]):
                    information[16] = (self.snake[0].x - i) / Snake.GAME_WIDTH   # distance to the body part at right
                    break

        elif information[2] == 1:              # if snake is heading left then the body parts are left part, bottom part, and top part
            for i in range(0, Snake.GAME_WIDTH, Snake.TILE_SIZE):
                if (self.snake[0].move(-i, 0) in self.snake[1:]):
                    information[14] = (self.snake[0].x - i) / Snake.GAME_WIDTH   # distance to the body part straight ahead
                    break
            for i in range(0, Snake.GAME_HEIGHT, Snake.TILE_SIZE):
                if (self.snake[0].move(0, i) in self.snake[1:]):
                    information[15] = (i - self.snake[0].y) / Snake.GAME_HEIGHT  # distance to the body at left
                    break
            for i in range(0, Snake.GAME_HEIGHT, Snake.TILE_SIZE):
                if (self.snake[0].move(0, -i) in self.snake[1:]):
                    information[16] = (self.snake[0].y - i) / Snake.GAME_HEIGHT  # distance to the body part at right
                    break

        elif information[3] == 1:              # if snake is heading right then the body parts are right part, top part, and bottom part
            for i in range(0, Snake.GAME_WIDTH, Snake.TILE_SIZE):
                if (self.snake[0].move(i, 0) in self.snake[1:]):
                    information[14] = (i - self.snake[0].x) / Snake.GAME_WIDTH   # distance to the body part straight ahead
                    break  
            for i in range(0, Snake.GAME_HEIGHT, Snake.TILE_SIZE):
                if (self.snake[0].move(0, -i) in self.snake[1:]):
                    information[15] = (self.snake[0].y - i) / Snake.GAME_HEIGHT  # distance to the body part at left
                    break 
            for i in range(0, Snake.GAME_HEIGHT, Snake.TILE_SIZE):
                if (self.snake[0].move(0, i) in self.snake[1:]):
                    information[16] = (i - self.snake[0].y) / Snake.GAME_HEIGHT  # distance to the body part at right
                    break

        # Food direction information 2: basically the x and y distance from food
        information[17] = abs(self.snake[0].x - self.food.x) / Snake.GAME_WIDTH
        information[18] = abs(self.snake[0].y - self.food.y) / Snake.GAME_HEIGHT

        # NOTE: The reason I divided distances by GAME_WIDTH or GAME_HEIGTH is to normalize the distances
        # The ohe values are all 1.0 and the distance values can go as big as 1000
        # i don't want the network to put too much emphasis on larger values and thats why I normalized the distances which puts the distances between 0 and 1
        
        return information
    

# make sure that the code is being accessed from the snake.py module
if __name__ == "__main__":
    pygame.quit()
