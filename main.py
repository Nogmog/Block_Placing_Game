import pygame
import os


# grid: 10 x 20
#"TEMPORARY" COLOURS
YELLOW = (255, 255, 0)
GREY = (102, 102, 102)

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

    main_frame = pygame.Rect(starting_x, starting_y, total_width, total_height)  
    pygame.draw.rect(WINDOW, YELLOW, main_frame)

    for i in range(200):
        print(i)
        x_coordinate = starting_x +  (i % 10) * 10 * block_per_grid
        y_coordinate = starting_y +  (i // 10) * block_per_grid
        block = pygame.Rect(x_coordinate, y_coordinate, block_per_grid, block_per_grid)
        pygame.draw.rect(WINDOW, GREY, block)
        
    pygame.display.update()

def gameplay():
    create_grid()


if __name__ == "__main__":
    gameplay() 
