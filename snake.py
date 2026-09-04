# import the necessary libraries:
import pygame
from random import randint


def main() -> None:
    pygame.init()                       # initialize pygame
    window = pygame.display.set_mode(   # display the window
    size=(GAME_WIDTH,
          GAME_HEIGHT)
        )
    pygame.display.set_caption("Snake") # create the title of the game
    clock = pygame.time.Clock()         # used for frame rate

    # generate random x position and y position for the food such that it doesn't overlap with where the snake is
    food_x = randint(0, COLUMNS) * TILE_SIZE
    food_y = randint(0, ROWS) * TILE_SIZE
    food = pygame.Rect(left=food_x, top=food_y, width=TILE_SIZE, height=TILE_SIZE)
    # snake is going to be a list because it is made up of many rectangles
    # snake = []
    
    running = True                      # this variable controls whether the game is running or not running
    while running:
        window.fill(BLACK)
        # draw_grid(window=window)
        
        for event in pygame.event.get():        # track every event that the user can do
            if event.type == pygame.QUIT:       # quit the game if the user clicks the X button at the top right
                running = False

        pygame.draw.rect(surface=window, color=RED, rect=food)
        pygame.display.update()                 # refresh game window
        clock.tick(10)                          # 10 frames per second


def draw_grid(window: pygame.Surface):
    for x in range(0, GAME_WIDTH, TILE_SIZE):
        for y in range(0, GAME_HEIGHT, TILE_SIZE):
            rect = pygame.Rect(left=x, top=y, width=TILE_SIZE, height=TILE_SIZE)
            pygame.draw.rect(surface=window, color=WHITE, rect=rect, width=1)


# make sure that the code is being accessed from the snake.py module
if __name__ == "__main__":
    # Constant variables:
    GAME_WIDTH = 1000
    GAME_HEIGHT = 1000
    TILE_SIZE = 20
    ROWS = int(GAME_HEIGHT / TILE_SIZE)
    COLUMNS = int(GAME_WIDTH / TILE_SIZE)
    WHITE = (200, 200, 200)
    BLACK = (0, 0, 0)
    RED = (255, 116, 108)
    GREEN = (193, 225, 193)

    board_array = []

    main()
    pygame.quit()
