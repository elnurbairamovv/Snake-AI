# import the necessary libraries:
import pygame
from random import randint


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

    def main(self) -> None:
        pygame.init()                               # initialize pygame
        window = pygame.display.set_mode(           # display the window
        size=(
            Snake.GAME_WIDTH,
            Snake.GAME_HEIGHT)
        )
        clock = pygame.time.Clock()

        while self.running:

            window.fill(Snake.BLACK)
            self.draw_grid(window=window)
            
            for event in pygame.event.get():        # track every event that the user can do
                if event.type == pygame.QUIT:       # quit the game if the user clicks the X button at the top right
                    self.running = False
    
                if event.type == pygame.KEYDOWN:    # check if the user pressed down a key on their keyboard
                    if (event.key == pygame.K_UP) and (self.velocity != (0, Snake.TILE_SIZE)) and not (self.turned_this_frame):
                        self.velocity = (0, -Snake.TILE_SIZE)
                        self.turned_this_frame = True
                    elif (event.key == pygame.K_DOWN) and (self.velocity != (0, -Snake.TILE_SIZE)) and not (self.turned_this_frame):
                        self.velocity = (0, Snake.TILE_SIZE)
                        self.turned_this_frame = True
                    elif (event.key == pygame.K_RIGHT) and (self.velocity != (-Snake.TILE_SIZE, 0)) and not (self.turned_this_frame):
                        self.velocity = (Snake.TILE_SIZE, 0)
                        self.turned_this_frame = True
                    elif (event.key == pygame.K_LEFT) and (self.velocity != (Snake.TILE_SIZE, 0)) and not (self.turned_this_frame):
                        self.velocity = (-Snake.TILE_SIZE, 0)
                        self.turned_this_frame = True

            self.snake[0].move_ip(self.velocity)                      # move the head of the snake
            
            if not (window.get_rect().contains(self.snake[0])):       # if the snake is outside of the board then end the game
                self.running = False
            
            if (self.snake[0] in self.snake[1:]):                     # if the snake head collides with the body then end the game
                self.running = False

            if self.snake[0].center == self.food.center:              # if the snake head collides with food then add to snake length
                self.snake.append(self.food)
    
                if len(self.snake) == (Snake.ROWS * Snake.COLUMNS):   # check if the snake covers the entire board
                    self.running = False
                else:                                                 # generate a new food in the board otherwise
                    food_x, food_y = self.get_random_pos()
                    self.food = pygame.Rect(food_x, food_y, Snake.TILE_SIZE, Snake.TILE_SIZE)

            for snake_part in self.snake:                             # draw the snake on the board
                pygame.draw.rect(surface=window, color=Snake.GREEN, rect=snake_part)
    
            for i in range(len(self.snake) - 1, 0, -1):               # this loop updates each part in snake list
                self.snake[i] = self.snake[i - 1].copy()

            self.turned_this_frame = False          # reset snake having turned this turn

            pygame.draw.rect(surface=window, color=Snake.RED, rect=self.food)
            pygame.display.update()                 # refresh game window
            clock.tick(10)                          # 10 frames per second

            print(f"snake x: {self.snake[0].x}")
            print(f"snake y: {self.snake[0].y}")


    def get_random_pos(self) -> tuple[float, float]:
        random_x, random_y = (randint(0, Snake.COLUMNS - 1) * Snake.TILE_SIZE, randint(0, Snake.ROWS - 1) * Snake.TILE_SIZE)
        
        while (pygame.Rect(random_x, random_y, Snake.TILE_SIZE, Snake.TILE_SIZE) in self.snake):
            random_x, random_y = (randint(0, Snake.COLUMNS - 1) * Snake.TILE_SIZE, randint(0, Snake.ROWS - 1) * Snake.TILE_SIZE)
    
        return random_x, random_y


    def simulate_keypress(self, key) -> None:
        key_event = pygame.event.Event(pygame.KEYDOWN, key=key)
        
        pygame.event.post(key_event)


    def draw_grid(self, window: pygame.Surface) -> None:
        for x in range(0, Snake.GAME_WIDTH, Snake.TILE_SIZE):
            for y in range(0, Snake.GAME_HEIGHT, Snake.TILE_SIZE):
                rect = pygame.Rect(x, y, Snake.TILE_SIZE, Snake.TILE_SIZE)
                pygame.draw.rect(surface=window, color=Snake.WHITE, rect=rect, width=1)


    def reset(self) -> None:
        # snake is going to be a list because it is made up of many rectangles
        self.snake = [pygame.Rect(Snake.SNAKE_X, Snake.SNAKE_Y, Snake.TILE_SIZE, Snake.TILE_SIZE)]
        # the velocity of the snake's head
        self.velocity = (0, 0)

        # generate random x position and y position for the food such that it doesn't overlap with where the snake is
        food_x, food_y = self.get_random_pos()
        self.food = pygame.Rect(food_x, food_y, Snake.TILE_SIZE, Snake.TILE_SIZE)

        # this variable is used to check if the snake has already moved
        self.turned_this_frame = False
        # this variable controls whether the game is running or not running
        self.running = True

        # this is the information i will be giving to the input layer of the neural network
        self.information = [0 for _ in range(16)]


    def get_information(self):
        # Snake's head direction information: Do one hot encoding based on which direction the snake's head is moving
        # You can skip one of the directions because it is redundant since the degrees of freedom for direction is 3, this would be the approach IF my snake started automatically moving from the start
        # Which means, you cant skip any of the directions because they are all needed. At the start all the directions are 0 which means the degrees of freedom has to be 4 for direction
        if self.velocity == (0, -Snake.TILE_SIZE):
            self.information[0] = 1                 # snake is heading up
        elif self.velocity == (0, Snake.TILE_SIZE):
            self.information[1] = 1                 # snake is heading down
        elif self.velocity == (-Snake.TILE_SIZE, 0):
            self.information[2] = 1                 # snake is heading left
        else:
            self.information[3] = 1                 # snake is heading right

        # Food direction information: Do one hot encoding again but for food this time
        # You cant skip any of the directions for food. The food might be above the snake's head but you also have to know if its to your right or to your left or neither. dof is 4
        if self.food.y < self.snake[0].y:
            self.information[4] = 1                 # snake is below food
        elif self.food.y > self.snake[0].y:
            self.information[5] = 1                 # snake is above food
        elif self.food.x < self.snake[0].x:
            self.information[6] = 1                 # snake is to the right of food
        elif self.food.x > self.snake[0].x:
            self.information[7] = 1                 # snake is to the left of food

        # Danger information: Do one hot encoding again but for the immediate danger to the snake's head (e.g border and body part)
        if ((self.snake[0].y - Snake.TILE_SIZE) == -50 or
            (self.snake[0].move(0, -Snake.TILE_SIZE)) in self.snake):
            self.information[8] = 1                 # there is immediate danger above the snake's head
        elif ((self.snake[0].y + Snake.TILE_SIZE) == Snake.GAME_WIDTH or
            (self.snake[0].move(0, Snake.TILE_SIZE)) in self.snake):
            self.information[9] = 1                 # there is immediate danger below the snake's head
        elif ((self.snake[0].x + Snake.TILE_SIZE) == Snake.GAME_WIDTH or
            (self.snake[0].move(Snake.TILE_SIZE, 0)) in self.snake):
            self.information[10] = 1                # there is immediate danger to the right of the snake's head
        elif ((self.snake[0].x - Snake.TILE_SIZE) == -50 or
            (self.snake[0].move(-Snake.TILE_SIZE, 0)) in self.snake):
            self.information[11] = 1                # there is immediate danger to the left of the snake's head

        # Danger information 2: Instead of ohe i will use distance of the border to the snake's head from every direction
        self.information[12] = self.snake_x - 0     # distance from top border

        # TODO: add the remaining informations for the input layer
        

# make sure that the code is being accessed from the snake.py module
if __name__ == "__main__":

    snake_0 = Snake()
    snake_0.main()
    pygame.quit()
