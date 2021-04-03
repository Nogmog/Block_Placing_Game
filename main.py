import pygame
import os
import random

pygame.font.init()
pygame.mixer.init()

from Code.brick_shapes import bricks, brick_colours

#LOADING IMAGES
PROGRAMICON = pygame.image.load(os.path.join("Assets", "TetrisIcon.jpg"))
I_img = pygame.image.load(os.path.join("Assets", "I block.png"))
J_img = pygame.image.load(os.path.join("Assets", "J block.png"))
L_img = pygame.image.load(os.path.join("Assets", "L block.png"))
O_img = pygame.image.load(os.path.join("Assets", "O block.png"))
S_img = pygame.image.load(os.path.join("Assets", "S block.png"))
Z_img = pygame.image.load(os.path.join("Assets", "Z block.png"))
T_img = pygame.image.load(os.path.join("Assets", "T block.png"))
block_images = [I_img, J_img, L_img, O_img, S_img, Z_img, T_img]
resized_blocks = []

#"TEMPORARY" COLOURS
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
DARK_GREY = (64, 64, 64)
LIGHT_GREY = (102, 102, 102)

# GAME CONSTANTS
FPS = 60
WIDTH, HEIGHT = 720, 576 # 16:9 ratio
#WIDTH, HEIGHT = 1920, 1080

#VARIABLES
queue = []
bag_queue_14 = ["S", "S", "Z", "Z", "I", "I", "O", "O", "J", "J", "L", "L", "T", "T"]
queue_length = 7
block_per_grid = (HEIGHT - HEIGHT*0.1) // 20

#SETTING UP PYGAME
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BLOCK PLACING GAME")
MAIN_FONT = pygame.font.SysFont("Comic Sans MS", 20)
pygame.display.set_icon(PROGRAMICON)

def resize_images(size):
    for i in range(len(block_images)):
        block_images[i] = pygame.transform.scale(block_images[i], (size, size))
        #resized_blocks.append(pygame.transform.scale(block_images[i], (size, size)))

def blank_board():
    board = []
    for i in range(20):
        board_temp = [".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        board.append(board_temp)
    return board

def draw_blocks(starting_x, starting_y, board):
    for i in range(200): # draw each individual brick

        x_point = i % 10 
        y_point = i // 10
        if board[y_point][x_point] == ".":
            continue
        
        x_coordinate = starting_x +  (i % 10) * block_per_grid
        y_coordinate = starting_y +  (i // 10) * block_per_grid
        block = pygame.Rect(x_coordinate, y_coordinate, block_per_grid, block_per_grid)
        pygame.draw.rect(WINDOW, DARK_GREY, block)

def create_grid(game_state):
    total_width = block_per_grid * 10
    total_height = block_per_grid * 20
    starting_x, starting_y = (WIDTH / 2) - (total_width / 2), (HEIGHT / 2) - (total_height / 2)

    background_area = pygame.Rect(starting_x, starting_y, total_width, total_height)  
    pygame.draw.rect(WINDOW, YELLOW, background_area)

    draw_blocks(starting_x, starting_y, game_state)

    for i in range(11): # vertical lines
        lines = pygame.Rect(starting_x + (block_per_grid)*i, starting_y, 1, total_height)
        pygame.draw.rect(WINDOW, LIGHT_GREY, lines)

    for i in range(21): # horizontal lines
        lines = pygame.Rect(starting_x, starting_y + (block_per_grid)*i, total_width, 1)
        pygame.draw.rect(WINDOW, LIGHT_GREY, lines)
    
def show_queue(queue):
    total_width = block_per_grid * 3
    total_height = block_per_grid * 16
    starting_x, starting_y = (WIDTH / 2) + block_per_grid * 6, (HEIGHT / 2) - ( (block_per_grid * 20) / 2)

    background_area = pygame.Rect(starting_x, starting_y, total_width, total_height) 
    pygame.draw.rect(WINDOW, DARK_GREY, background_area)

    size = int(total_height // 8)
    centralise_x = int(total_width // 2 - size // 2) + starting_x

    resize_images(size)
    
    queue_text = MAIN_FONT.render("QUEUE", 1, WHITE)
    WINDOW.blit(queue_text, (starting_x,starting_y))

    for i in range(len(queue)):
        height = size * (i + 1)

        if queue[i] == "I":
            WINDOW.blit(block_images[0], (centralise_x, height))
        elif queue[i] == "J":
            WINDOW.blit(block_images[1], (centralise_x, height))
        elif queue[i] == "L":
            WINDOW.blit(block_images[2], (centralise_x, height))
        elif queue[i] == "O":
            WINDOW.blit(block_images[3], (centralise_x, height))
        elif queue[i] == "S":
            WINDOW.blit(block_images[4], (centralise_x, height))
        elif queue[i] == "Z":
            WINDOW.blit(block_images[5], (centralise_x, height))
        elif queue[i] == "T":
            WINDOW.blit(block_images[6], (centralise_x, height))
        
    
def update_queue(queue):
    global bag_queue_14
    while len(queue) < queue_length:
        if len(bag_queue_14) == 0:
            bag_queue_14 = ["S", "S", "Z", "Z", "I", "I", "O", "O", "J", "J", "L", "L", "T", "T"]

        random_int = random.randint(0, len(bag_queue_14) - 1)
        block = bag_queue_14[random_int]

        bag_queue_14.pop(random_int)
        queue.append(block)
    return queue

def block_to_game(board, next_block): # start from 3rd brick
    block_format = bricks.__getattribute__(bricks, next_block)
    block_format = block_format[0]
    for y in range(5):
        for x in range(5):
            item = block_format[y][x]

def gameplay():
    print("Starting new game!")
    game_state = blank_board()

    queue = update_queue([])
    clock = pygame.time.Clock()
    run = True
    block_in_play = False
    rotate = 0
    while run:
        clock.tick(FPS)
        
        if not block_in_play:
            block_in_play = True
            rotate = 0
            next_block = queue[0]
            block_to_game(game_state, next_block)
            queue = update_queue(queue)
        
        create_grid(game_state)
        show_queue(queue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        

        pygame.display.update()


if __name__ == "__main__":
    gameplay() 
