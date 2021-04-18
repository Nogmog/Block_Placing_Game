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

#GAME FUNCTIONS
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

def draw_blocks(starting_x, starting_y, board, current_block):
    for i in range(200): # draw each individual brick

        x_point = i % 10
        y_point = i // 10
        if board[y_point][x_point] == ".":
            continue
        
        x_coordinate = starting_x +  x_point * block_per_grid
        y_coordinate = starting_y +  y_point * block_per_grid
        block = pygame.Rect(x_coordinate, y_coordinate, block_per_grid, block_per_grid)
        pygame.draw.rect(WINDOW, DARK_GREY, block)
    
    for i in range(16):
        x = i % 4
        y = i // 4

        item = current_block[y + 1][x]
        if item == ".": continue

        block_colour = brick_colours.__getattribute__(brick_colours, item)

        c_block_x = x + current_block[0][0]
        c_block_y = y + current_block[0][1]
        
        x_coordinate = starting_x +  c_block_x * block_per_grid
        y_coordinate = starting_y +  c_block_y * block_per_grid

        block = pygame.Rect(x_coordinate, y_coordinate, block_per_grid, block_per_grid)
        pygame.draw.rect(WINDOW, block_colour, block)

def create_grid(game_state, current_block):
    total_width = block_per_grid * 10
    total_height = block_per_grid * 20
    starting_x, starting_y = (WIDTH / 2) - (total_width / 2), (HEIGHT / 2) - (total_height / 2)

    background_area = pygame.Rect(starting_x, starting_y, total_width, total_height)  
    pygame.draw.rect(WINDOW, DARK_GREY, background_area)

    draw_blocks(starting_x, starting_y, game_state, current_block)

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
    block_pos = [[3, 0], block_format[0], block_format[1], block_format[2], block_format[3]]
    return block_pos


def move_block(coordinates, current_block, game_state): # function to move block
    print("Move block initiated")
    x_move = 0
    y_move = 0
    moved = False
    for i in range(16):
        x = i % 4
        y = i // 4

        item = current_block[y + 1][x]
        if item == ".": continue
        
        c_block_x = x + current_block[0][0]
        c_block_y = y + current_block[0][1]
        
        if c_block_x + coordinates[0] >= 0 and c_block_x + coordinates[0] < 10: # check if in range of game
            if game_state[c_block_y][c_block_x + coordinates[0]] == ".": # x coord check
                x_move += 1
        
        if c_block_y + coordinates[1] >= 0 and c_block_y + coordinates[1] < 20:
            if game_state[c_block_y + coordinates[1]][c_block_x] == ".": # y coord check
                y_move += 1
    
    print(x_move, y_move)
    if x_move == 4 and y_move == 4:
        print("Moving")
        current_block[0] = [current_block[0][0] + coordinates[0], current_block[0][1] + coordinates[1]]
        moved = True

    return moved

def rotate_block(current_block, game_state, rotate):
    print("Rotate block initiated")
    new_rotation = [current_block[0]]
    for i in range(16): # makes new rotated block
        x = i % 4
        y = i // 4
        item = current_block[y + 1][x]
        if item == "O":
            return current_block, rotate - 1
        elif item != ".":
            rotation_length = len(bricks.__getattribute__(bricks, item))
            new_rotate_list = bricks.__getattribute__(bricks, item)[rotate % rotation_length]

            for x in range(4): # as new_rotate_list is a separate list, we are separating so it is in the normal format
                new_rotation.append(new_rotate_list[x])
            break

    movable = 0
    for i in range(16):
        x = i % 4
        y = i // 4

        if new_rotation[y + 1][x] == ".":
            continue

        c_block_x = x + new_rotation[0][0]
        c_block_y = y + new_rotation[0][1]

        if game_state[c_block_y][c_block_x] == ".": # x coord check
            movable += 1
    print(movable)
    if movable == 4:
        return new_rotation, rotate
    else: return current_block, rotate - 1

def place_block(current_block, game_state):
    for num in range(16):
        print(num)
        x = num % 4
        y = num // 4

        item = current_block[y + 1][x]
        if item == ".": continue

        x_grid_position = x + current_block[0][0]
        y_grid_position = y + current_block[0][1]
        print(x_grid_position, y_grid_position)

        game_state[y_grid_position][x_grid_position] = item
        #print(game_state[y_grid_position][x_grid_position])
    
    return game_state



def gameplay():
    print("Starting new game!")
    game_state = blank_board()

    queue = update_queue([])
    clock = pygame.time.Clock()

    run = True
    block_in_play = False
    rotate = 0
    current_block = []
    level = 1
    drop_time = 0
    while run:
        clock.tick(FPS)
        drop_time += clock.get_rawtime()
        
        if not block_in_play:
            block_in_play = True
            rotate = 0
            next_block = queue[0]
            queue.pop(0)
            current_block = block_to_game(game_state, next_block)
            drop_time = 0
            queue = update_queue(queue)
        
        create_grid(game_state, current_block)
        show_queue(queue)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: # move left
                    move_block([-1, 0], current_block, game_state)
                if event.key == pygame.K_RIGHT: # move right 
                   move_block([1, 0], current_block, game_state)
                if event.key == pygame.K_UP: # rotate
                    current_block, rotate = rotate_block(current_block, game_state, rotate + 1)
                if event.key == pygame.K_DOWN: # down
                    move_block([0, 1], current_block, game_state)
                    drop_time = 0
        pygame.display.update()
        #print(drop_time)
        if (drop_time / 200) > (1 / level):
            drop_time = 0
            moved = move_block([0, 1], current_block, game_state)

            if not moved:
                game_state = place_block(current_block, game_state)
                print(game_state)
                block_in_play = False
            
        

if __name__ == "__main__":
    gameplay() 
