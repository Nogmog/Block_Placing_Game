import pygame
import os


#"TEMPORARY" COLOURS
YELLOW = (255, 255, 0)
DARK_GREY = (64, 64, 64)
LIGHT_GREY = (102, 102, 102)

# GAME CONSTANTS
FPS = 60
WIDTH, HEIGHT = 720, 576 # 16:9 ratio
#WIDTH, HEIGHT = 1920, 1080
PROGRAMICON = pygame.image.load(os.path.join("Assets", "TetrisIcon.jpg"))

#SETTING UP PYGAME
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BLOCK PLACING GAME")
pygame.display.set_icon(PROGRAMICON)



def create_grid():
    block_per_grid = (HEIGHT - HEIGHT*0.1) // 20
    total_width = block_per_grid * 10
    total_height = block_per_grid * 20
    starting_x, starting_y = (WIDTH / 2) - (total_width / 2), (HEIGHT / 2) - (total_height / 2)

    background_area = pygame.Rect(starting_x, starting_y, total_width, total_height)  
    pygame.draw.rect(WINDOW, YELLOW, background_area)

    for i in range(200): # draw each individual brick
        x_coordinate = starting_x +  (i % 10) * block_per_grid
        y_coordinate = starting_y +  (i // 10) * block_per_grid
        block = pygame.Rect(x_coordinate, y_coordinate, block_per_grid, block_per_grid)
        pygame.draw.rect(WINDOW, DARK_GREY, block)

    for i in range(11): # vertical lines
        lines = pygame.Rect(starting_x + (block_per_grid)*i, starting_y, 2, total_height)
        pygame.draw.rect(WINDOW, LIGHT_GREY, lines)

    for i in range(21): # horizontal lines
        lines = pygame.Rect(starting_x, starting_y + (block_per_grid)*i, total_width, 2)
        pygame.draw.rect(WINDOW, LIGHT_GREY, lines)
        
    pygame.display.update()

def gameplay():
    create_grid()


if __name__ == "__main__":
    gameplay() 