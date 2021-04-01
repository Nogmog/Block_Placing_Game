import pygame
import os
import random


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
pygame.display.set_icon(PROGRAMICON)

def resize_images(size):
    for i in range(len(block_images) - 1):
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
    total_height = block_per_grid * 10 #queue_length + block_per_grid
    starting_x, starting_y = (WIDTH / 2) + block_per_grid * 6, (HEIGHT / 2) - ( (block_per_grid * 20) / 2)

    background_area = pygame.Rect(starting_x, starting_y, total_width, total_height) 
    pygame.draw.rect(WINDOW, YELLOW, background_area)

    size = int((total_height - block_per_grid) // 9)
    resize_images(size)
    
    centralise_x = int(total_width // 2 - size // 2) + starting_x

    for i in range(len(queue) - 1):
        height = size * (i + 1)
        if queue[i] == "S":
            print(i,": S block")
            WINDOW.blit(S_img, (centralise_x, height))
    
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


def gameplay():
    print("Starting new game!")
    game_state = blank_board()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        create_grid(game_state)
        new_queue = update_queue(queue)
        show_queue(new_queue)
        pygame.display.update()


if __name__ == "__main__":
    gameplay() 