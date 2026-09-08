# import the necessary libraries:
import pygame
from random import randint


def main() -> None:
    pygame.init()                               # initialize pygame
    window = pygame.display.set_mode(           # display the window
    size=(GAME_WIDTH,
          GAME_HEIGHT)
        )
    pygame.display.set_caption("Snake")         # create the title of the game
    clock = pygame.time.Clock()                 # used for frame rate

    board_array = [                             # initialize a board array. I need this to extract information for input layer
            "." for _ in range(ROWS * COLUMNS)
            ]
    curr_head_pos = 10 * 10                     # ROW * COLUMN
    board_array[curr_head_pos] = "s"            # initialize the snake's head position in the board_array

    # snake is going to be a list because it is made up of many rectangles
    snake = [pygame.Rect(SNAKE_X, SNAKE_Y, TILE_SIZE, TILE_SIZE)]

    # generate random x position and y position for the food such that it doesn't overlap with where the snake is
    food_x, food_y = get_random_pos(snake)
    food = pygame.Rect(food_x, food_y, TILE_SIZE, TILE_SIZE)

    # the velocity of the snake's head
    velocity = (0, 0)
    
    running = True                              # this variable controls whether the game is running or not running
    while running:
        window.fill(BLACK)
        draw_grid(window=window)
        
        for event in pygame.event.get():        # track every event that the user can do
            if event.type == pygame.QUIT:       # quit the game if the user clicks the X button at the top right
                running = False

            if event.type == pygame.KEYDOWN:    # check if the user pressed down a key on their keyboard
                if (event.key == pygame.K_UP) and not (velocity == (0, TILE_SIZE)):
                    velocity = (0, -TILE_SIZE)
                elif (event.key == pygame.K_DOWN) and not (velocity == (0, -TILE_SIZE)):
                    velocity = (0, TILE_SIZE)
                elif (event.key == pygame.K_RIGHT) and not (velocity == (-TILE_SIZE, 0)):
                    velocity = (TILE_SIZE, 0)
                elif (event.key == pygame.K_LEFT) and not (velocity == (TILE_SIZE, 0)):
                    velocity = (-TILE_SIZE, 0)

        snake[0].move_ip(velocity)
        update_board(board=board_array, obj="s", row=(snake[0].y / TILE_SIZE), column=(snake[0].x / TILE_SIZE))
        curr_head_pos = (snake[0].y / TILE_SIZE) * (snake[0].x / TILE_SIZE)

        if not (window.get_rect().contains(snake[0])):  # if the snake is outside of the board then end the game
            running = False

        if (snake[0] in snake[1:]):                     # if the snake head collides with the body then end the game
            running = False

        if snake[0].center == food.center:              # if the snake head collides with food then add to snake length
            snake.append(food)

            if len(snake) == (ROWS * COLUMNS):          # check if the snake covers the entire board
                running = False
            else:
                food_x, food_y = get_random_pos(snake=snake)
                update_board(board=board_array, obj="f", row=(food_y / TILE_SIZE), column=(food_x / TILE_SIZE))
                food = pygame.Rect(food_x, food_y, TILE_SIZE, TILE_SIZE)
            

        for snake_part in snake:
            pygame.draw.rect(surface=window, color=GREEN, rect=snake_part)

        for i in range(len(snake) - 1, 0, -1):  # this loop updates each rectangle in snake
            snake[i] = snake[i - 1].copy()
            update_board(board=board_array, obj="s", row=(snake[i].y / TILE_SIZE), column=(snake[i].x / TILE_SIZE))

        print(board_array)
        print(len(board_array))
        pygame.draw.rect(surface=window, color=RED, rect=food)
        pygame.display.update()                 # refresh game window
        clock.tick(10)                          # 10 frames per second


def get_random_pos(snake: pygame.Rect) -> tuple[float, float]:
    random_x, random_y = (randint(0, COLUMNS - 1) * TILE_SIZE, randint(0, ROWS - 1) * TILE_SIZE)

    while (pygame.Rect(random_x, random_y, TILE_SIZE, TILE_SIZE) in snake):
        random_x, random_y = (randint(0, COLUMNS - 1) * TILE_SIZE, randint(0, ROWS - 1) * TILE_SIZE)

    return random_x, random_y


def draw_grid(window: pygame.Surface) -> None:
    for x in range(0, GAME_WIDTH, TILE_SIZE):
        for y in range(0, GAME_HEIGHT, TILE_SIZE):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(surface=window, color=WHITE, rect=rect, width=1)


# if I receive a keypress from network output layer then I want to make that keypress happen in game using this function
def simulate_keypress(key) -> None:
    key_event = pygame.event.Event(pygame.KEYDOWN, key=key)

    pygame.event.post(key_event)


def update_board(board, obj: str, row: float, column: float) -> None:
    board[int(row * column)] = obj


# make sure that the code is being accessed from the snake.py module
if __name__ == "__main__":
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

    main()
    pygame.quit()
