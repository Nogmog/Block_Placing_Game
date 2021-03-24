import pygame
import os


# grid: 10 x 20
# GAME CONSTANTS
FPS = 60
WIDTH, HEIGHT = 720, 576 # 16:9 ratio
PROGRAMICON = pygame.image.load(os.path.join(os.pardir, "Assets", "TetrisIcon.jpg"))

#SETTING UP PYGAME
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BLOCK PLACING GAME")
pygame.display.set_icon(PROGRAMICON)



def create_grid():
    pass


def gameplay():
    create_grid()


if __name__ == "__main__":
    gameplay() 
