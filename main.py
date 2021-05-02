import pygame
import os
import random
import string

pygame.font.init()
pygame.mixer.init()

from Code.brick_shapes import bricks, brick_colours

#LOADING IMAGES
BLACK_WALL = pygame.image.load(os.path.join("Assets", "Black wall.png"))
LEGO_BG = pygame.image.load(os.path.join("Assets", "Lego background.jpg"))
SQUARE_BG = pygame.image.load(os.path.join("Assets", "Square background.jpg"))

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
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
DARK_GREY = (64, 64, 64)
LIGHT_GREY = (102, 102, 102)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192) 
BRONZE = (205, 127, 50)

# GAME CONSTANTS
FPS = 60
WIDTH, HEIGHT = 720, 576 # 16:9 ratio
#WIDTH, HEIGHT = 1920, 1080

#VARIABLES
queue = []
bag_queue_14 = ["S", "S", "Z", "Z", "I", "I", "O", "O", "J", "J", "L", "L", "T", "T"]
queue_length = 7
block_per_grid = (HEIGHT - HEIGHT*0.1) // 20

MAIN_FONT = pygame.font.SysFont("Comic Sans MS", 20)
SCORE_WORD = pygame.font.SysFont("Comic Sans MS", 20)
SCORE_NUMBER = pygame.font.SysFont("Comic Sans MS", 20)
WORD_FONT = pygame.font.SysFont("Comic Sans MS", 15)
BLACK_WALL = pygame.transform.scale(BLACK_WALL, (WIDTH, HEIGHT))
LEGO_BG = pygame.transform.scale(LEGO_BG, (WIDTH, HEIGHT))
SQUARE_BG = pygame.transform.scale(SQUARE_BG, (WIDTH, HEIGHT))

#SETTING UP PYGAME
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BLOCK PLACING GAME")
pygame.display.set_icon(T_img)

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
        
        block_colour = brick_colours.__getattribute__(brick_colours, board[y_point][x_point])

        x_coordinate = starting_x +  x_point * block_per_grid
        y_coordinate = starting_y +  y_point * block_per_grid
        block = pygame.Rect(x_coordinate, y_coordinate, block_per_grid, block_per_grid)
        pygame.draw.rect(WINDOW, block_colour, block)
    
    for i in range(16): # draws brick in game
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

    passed = 0
    for i in range(16):
        x = i % 4
        y = i // 4
        if block_pos[y + 1][x] == ".":
            continue
        c_block_x = x + block_pos[0][0]
        c_block_y = y + block_pos[0][1]

        if board[c_block_y][c_block_x] == ".": # x coord check
            passed += 1
    
    if passed != 4: return "GAME OVER"
    return block_pos


def move_block(coordinates, current_block, game_state): # function to move block
    #print("Move block initiated")
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
    
    #print(x_move, y_move)
    if x_move == 4 and y_move == 4:
        #print("Moving")
        current_block[0] = [current_block[0][0] + coordinates[0], current_block[0][1] + coordinates[1]]
        moved = True

    return moved

def rotate_block(current_block, game_state, rotate, movement):
    rotate += movement
    new_rotation = [current_block[0]]
    for i in range(16): # makes new rotated block
        x = i % 4
        y = i // 4
        item = current_block[y + 1][x]
        if item == "O":
            return current_block, rotate + movement
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

        if c_block_y > 19 or c_block_y < 0 or c_block_x > 9 or c_block_x < 0:
            continue

        if game_state[c_block_y][c_block_x] == ".": # x coord check
            movable += 1
    
    if movable == 4:
        return new_rotation, rotate
    else: return current_block, rotate + movement

def place_block(current_block, game_state):
    for num in range(16):
        x = num % 4
        y = num // 4

        item = current_block[y + 1][x]
        if item == ".": continue

        x_grid_position = x + current_block[0][0]
        y_grid_position = y + current_block[0][1]

        game_state[y_grid_position][x_grid_position] = item
        #print(game_state[y_grid_position][x_grid_position])
    
    return game_state

def remove_blocks(game_state, score, level): # Removes blocks if in line
    combo = 0
    start_checking = False
    for y in range(19, -1, -1):
        line_full = False
        for x in range(10):
            if game_state[y][x] == ".":
                break

            if x == 9:
                line_full = True
                start_checking = True
            
        if line_full and start_checking:
            combo += 1
        elif not line_full and start_checking:
            print(combo, " lines cleared")
            
            for i in range(combo):
                game_state.pop(y + i + 1)
                game_state.insert(0, [".", ".", ".", ".", ".", ".", ".", ".", ".", "."])
            score += ((2 ** combo) * (level + 1))* 10
            break
    return score, combo

def show_extras(score, level, hold_brick):
    #Showing Score
    starting_x, starting_y = (WIDTH / 2) + block_per_grid * 6, (HEIGHT / 2) + ( (block_per_grid * 12) / 2)
    score_words = MAIN_FONT.render("SCORE", 1, WHITE)
    score_numbers = MAIN_FONT.render(str(score), 1, WHITE)
    WINDOW.blit(score_words, (starting_x,starting_y))
    WINDOW.blit(score_numbers, (starting_x, starting_y + block_per_grid))

    #Showing Level
    level_x, level_y = (WIDTH / 2) - (block_per_grid * 8), (HEIGHT / 2) - (block_per_grid * 6)
    level_words = MAIN_FONT.render("LEVEL", 1, WHITE)
    level_numbers = MAIN_FONT.render(str(level), 1, WHITE)
    WINDOW.blit(level_words, (level_x, level_y))
    WINDOW.blit(level_numbers, (level_x, level_y + block_per_grid))
    
    #Show held brick
    brick_y = (HEIGHT / 2) - (block_per_grid * 9)
    if hold_brick == "I":
        WINDOW.blit(block_images[0], (level_x, brick_y))
    elif hold_brick == "J":
        WINDOW.blit(block_images[1], (level_x, brick_y))
    elif hold_brick == "L":
        WINDOW.blit(block_images[2], (level_x, brick_y))
    elif hold_brick == "O":
        WINDOW.blit(block_images[3], (level_x, brick_y))
    elif hold_brick == "S":
        WINDOW.blit(block_images[4], (level_x, brick_y))
    elif hold_brick == "Z":
        WINDOW.blit(block_images[5], (level_x, brick_y))
    elif hold_brick == "T":
        WINDOW.blit(block_images[6], (level_x, brick_y))

def game_over(score):
    size_x, size_y = WIDTH // 2, HEIGHT // 3
    x_pos, y_pos = (WIDTH / 2) - (size_x / 2), (HEIGHT / 2) - (size_y / 2)

    game_over_text = MAIN_FONT.render("GAME OVER", 1, WHITE)
    score_text = MAIN_FONT.render("SCORE: "+str(score), 1, WHITE)

    alphabet = string.ascii_uppercase
    letter_one, letter_two, letter_three = 0, 0, 0
    letter_choices = [letter_one, letter_two, letter_three]

    letter_x = x_pos + size_x // 2
    current_choice = 0
    letter_colours = [YELLOW, WHITE, WHITE]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    letter_choices[current_choice] += 1
                if event.key == pygame.K_DOWN: 
                    letter_choices[current_choice] -= 1
                if event.key == pygame.K_RIGHT:
                    letter_colours[current_choice] = WHITE
                    current_choice = (current_choice + 1) % 3
                    letter_colours[current_choice] = YELLOW
                if event.key == pygame.K_LEFT:
                    letter_colours[current_choice] = WHITE
                    current_choice = (current_choice - 1) % 3
                    letter_colours[current_choice] = YELLOW
                if event.key == pygame.K_RETURN: # Entering score
                    name = alphabet[letter_choices[0] % 26] + alphabet[letter_choices[1] % 26] + alphabet[letter_choices[2] % 26]
                    file = open(os.path.join("Code", "Leaderboard.txt"), "a+")
                    file.write(name+":"+str(score)+"\n")
                    file.close()
                    main_menu()
                    
        
        background_window = pygame.Rect(x_pos, y_pos, size_x, size_y) 
        pygame.draw.rect(WINDOW, DARK_GREY, background_window)
        WINDOW.blit(game_over_text, (x_pos, y_pos))
        WINDOW.blit(score_text, (x_pos, y_pos + 50))

        first_letter = MAIN_FONT.render(alphabet[letter_choices[0] % 26], 1, letter_colours[0])
        second_letter = MAIN_FONT.render(alphabet[letter_choices[1] % 26], 1, letter_colours[1])
        third_letter = MAIN_FONT.render(alphabet[letter_choices[2] % 26], 1, letter_colours[2])

        WINDOW.blit(first_letter, (letter_x, y_pos + 100))
        WINDOW.blit(second_letter, (letter_x + block_per_grid, y_pos + 100))
        WINDOW.blit(third_letter, (letter_x + (block_per_grid * 2), y_pos + 100))

        pygame.display.update()

def gameplay():
    print("Starting new game!")
    game_state = blank_board()

    queue = update_queue([])
    clock = pygame.time.Clock()

    run = True
    block_in_play = False
    hold_brick = ""
    hold_change = True
    rotate = 0
    current_block = []
    level = 1
    drop_time = 0
    score = 0
    lines_cleared = 0
    while run:
        clock.tick(FPS)
        drop_time += clock.get_rawtime()
        WINDOW.blit(BLACK_WALL, (0, 0))
        
        if not block_in_play:
            block_in_play = True
            hold_change = True
            rotate = 0
            current_block = block_to_game(game_state, queue[0])
            if current_block == "GAME OVER":
                run = False
                continue

            queue.pop(0)
            drop_time = 0
            queue = update_queue(queue)
        
        create_grid(game_state, current_block)
        show_queue(queue)
        show_extras(score, level, hold_brick)

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
                    current_block, rotate = rotate_block(current_block, game_state, rotate, 1)
                if event.key == pygame.K_z: # anti - clockwise
                    current_block, rotate = rotate_block(current_block, game_state, rotate, -1)
                if event.key == pygame.K_DOWN: # down
                    moved = move_block([0, 1], current_block, game_state)
                    if moved:
                        drop_time = 0
                if event.key == pygame.K_c: #hold block
                    if hold_change:
                        hold_change = False
                        drop_time = 0

                        for i in range(16):
                            x = i % 4
                            y = i // 4

                            item = current_block[y + 1][x]
                            if item == ".": continue
                            else: 
                                brick_name = item 
                                break
                        
                        if hold_brick == "":
                            hold_brick = brick_name
                            current_block = block_to_game(game_state, queue[0])
                            queue.pop(0)
                            queue = update_queue(queue)
                        
                        else:
                            current_block = block_to_game(game_state, hold_brick)
                            hold_brick = brick_name

                            
        pygame.display.update()

        if (drop_time / 200) > (1 / level):
            drop_time = 0
            moved = move_block([0, 1], current_block, game_state)

            if not moved:
                game_state = place_block(current_block, game_state)
                block_in_play = False
                score += 1
                score, clears = remove_blocks(game_state, score, level)
                lines_cleared += clears
                level = (lines_cleared // 10) + 1

    game_over(score)

def sort_leaderboard():
    
    print("Sorting")
    reading_file = open(os.path.join("Code", "Leaderboard.txt"), "r+")
    read_lines = reading_file.readlines()

    scores = []
    for x in range(len(read_lines)):
        temp = read_lines[x].split(":")
        temp[1] = temp[1].rstrip("\n")
        scores.append(temp)
    
    scores.sort(reverse=True, key=lambda x: int(x[1]))
    
    write_file = open(os.path.join("Code", "Leaderboard.txt"), "w+")
    for i in range(len(scores)):
        glued = scores[i][0]+":"+scores[i][1]+"\n"
        write_file.write(glued)
    write_file.close()

def options():
    run = True
    while run:
        WINDOW.blit(LEGO_BG, (0, 0))

        mx, my = pygame.mouse.get_pos()

        title_text = MAIN_FONT.render("OPTIONS", 1, WHITE)
        size1 = WORD_FONT.render("1920 x 1080", 1, WHITE)
        size2 = WORD_FONT.render("720 x 576", 1, WHITE)
        size3 = WORD_FONT.render("1280 x 720", 1, WHITE)

        size1_bg = pygame.Rect(block_per_grid, (HEIGHT // 3), size1.get_width(), size1.get_height())
        size2_bg = pygame.Rect(block_per_grid, (HEIGHT // 3) + (block_per_grid * 2), size2.get_width(), size2.get_height())
        size3_bg = pygame.Rect(block_per_grid, (HEIGHT // 3) + (block_per_grid * 4), size3.get_width(), size3.get_height())

        backgrounds = [size1_bg, size2_bg, size3_bg]
        
        WINDOW.blit(title_text, (WIDTH // 2 - (title_text.get_width() // 2), block_per_grid))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pass
        
        for x in range(len(backgrounds)):
            item = backgrounds[x]
            if item.collidepoint((mx, my)):
                pygame.draw.rect(WINDOW, brick_colours.T, item)
            else: pygame.draw.rect(WINDOW, LIGHT_GREY, item)
        
        WINDOW.blit(size1, (block_per_grid, (HEIGHT // 3)))
        WINDOW.blit(size2, (block_per_grid, (HEIGHT // 3) + (block_per_grid * 2)))
        WINDOW.blit(size3, (block_per_grid, (HEIGHT // 3) + (block_per_grid * 4)))
        
        pygame.display.update()
    main_menu()

def leaderboard():
    sort_leaderboard()
    
    run = True
    org_width, org_height = WIDTH // 2, HEIGHT - (block_per_grid * 3)
    starting_x, starting_y = WIDTH // 2 - (org_width // 2), block_per_grid * 3
    amount = int((org_height - (block_per_grid * 5)) // 40) + 3
    print(amount)
    
    while run:
        WINDOW.blit(LEGO_BG, (0, 0))
        background = pygame.Rect(starting_x, starting_y, org_width, org_height)
        pygame.draw.rect(WINDOW, DARK_GREY, background)

        title_text = MAIN_FONT.render("LEADERBOARD", 1, WHITE)
        WINDOW.blit(title_text, (WIDTH // 2 - (title_text.get_width() // 2), block_per_grid))

        file = open(os.path.join("Code", "Leaderboard.txt"), "r+")
        for i in range(amount):
            current_line = file.readline()
            if current_line != "":
                score = current_line[4::].rstrip("\n")
                name = current_line[:3]
            else:
                name = "NONE"
                score = "0"
            
            podium_width = (org_width - (block_per_grid * 3)) // 3
            if i == 0:
                gold_text = MAIN_FONT.render(name, 1, WHITE)
                WINDOW.blit(gold_text, (starting_x + (org_width // 2) - gold_text.get_width() // 2, starting_y + block_per_grid))

                gold_block = pygame.Rect(starting_x + (org_width // 2) - podium_width // 2, starting_y + (block_per_grid * 2), podium_width, block_per_grid * 5)
                pygame.draw.rect(WINDOW, GOLD, gold_block)

                gold_score_text = MAIN_FONT.render(score, 1, BLACK)
                WINDOW.blit(gold_score_text, (starting_x + (org_width // 2) - gold_score_text.get_width() // 2, starting_y + (block_per_grid * 6)))
            elif i == 1:
                silver_text = MAIN_FONT.render(name, 1, WHITE)
                WINDOW.blit(silver_text, (starting_x + (org_width // 2) - silver_text.get_width() // 2 - podium_width, starting_y + block_per_grid * 2))

                silver_block = pygame.Rect(starting_x + (org_width // 2) - (podium_width // 2) - podium_width, starting_y + (block_per_grid * 3), podium_width, block_per_grid * 4)
                pygame.draw.rect(WINDOW, SILVER, silver_block)

                silver_score_text = MAIN_FONT.render(score, 1, BLACK)
                WINDOW.blit(silver_score_text, (starting_x + (org_width // 2) - silver_score_text.get_width() // 2 - podium_width, starting_y + (block_per_grid * 6)))
            elif i == 2:
                bronze_text = MAIN_FONT.render(name, 1, WHITE)
                WINDOW.blit(bronze_text, (starting_x + (org_width // 2) - bronze_text.get_width() // 2 + podium_width, starting_y + block_per_grid * 3))

                bronze_block = pygame.Rect(starting_x + (org_width // 2) - (podium_width // 2) + podium_width, starting_y + (block_per_grid * 4), podium_width, block_per_grid * 3)
                pygame.draw.rect(WINDOW, BRONZE, bronze_block)

                bronze_score_text = MAIN_FONT.render(score, 1, BLACK)
                WINDOW.blit(bronze_score_text, (starting_x + (org_width // 2) - bronze_score_text.get_width() // 2 + podium_width, starting_y + (block_per_grid * 6)))
            else:
                words = str(i + 1) + ". "+name+": "+score
                player_text = WORD_FONT.render(words, 1, WHITE)
                WINDOW.blit(player_text, (starting_x + block_per_grid, (block_per_grid * 11) + (32 * (i - 3))))
                #org_height - (block_per_grid * 5)) // 40
                
                
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        #file.close()
        pygame.display.update()
    main_menu()

def main_menu():
    run = True

    while run:
        width, height = 200, 30
        WINDOW.blit(LEGO_BG, (0, 0))
        title_text = MAIN_FONT.render("BLOCK PLACING GAME", 1, WHITE)
        play_text = WORD_FONT.render("PLAY GAME", 1, WHITE)
        option_text = WORD_FONT.render("OPTIONS", 1, WHITE)
        leaderboard_text = WORD_FONT.render("LEADERBOARD", 1, WHITE)

        play_bg = pygame.Rect(block_per_grid, (HEIGHT // 3), width, height)
        option_bg = pygame.Rect(block_per_grid, (HEIGHT // 3) + (block_per_grid * 2), width, height)
        leaderboard_bg = pygame.Rect(block_per_grid, (HEIGHT // 3) + (block_per_grid * 4), width, height)

        pygame.draw.rect(WINDOW, LIGHT_GREY, play_bg)
        pygame.draw.rect(WINDOW, LIGHT_GREY, option_bg)
        pygame.draw.rect(WINDOW, LIGHT_GREY, leaderboard_bg)
        
        WINDOW.blit(title_text, (WIDTH // 2 - (title_text.get_width() // 2), block_per_grid))

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if play_bg.collidepoint((mx, my)):
                        gameplay()
                    elif option_bg.collidepoint((mx, my)):
                        options()
                    elif leaderboard_bg.collidepoint((mx, my)):
                        leaderboard()


        if play_bg.collidepoint((mx, my)):
            pygame.draw.rect(WINDOW, brick_colours.T, play_bg)
        else: pygame.draw.rect(WINDOW, LIGHT_GREY, play_bg)

        if option_bg.collidepoint((mx, my)):
            pygame.draw.rect(WINDOW, brick_colours.T, option_bg)
        else: pygame.draw.rect(WINDOW, LIGHT_GREY, option_bg)
        
        if leaderboard_bg.collidepoint((mx, my)):
            pygame.draw.rect(WINDOW, brick_colours.T, leaderboard_bg)
        else: pygame.draw.rect(WINDOW, LIGHT_GREY, leaderboard_bg)
        
        WINDOW.blit(play_text, (block_per_grid, HEIGHT // 3))
        WINDOW.blit(option_text, (block_per_grid, (HEIGHT // 3) + (block_per_grid * 2)))
        WINDOW.blit(leaderboard_text, (block_per_grid, (HEIGHT // 3) + (block_per_grid * 4)))

        pygame.display.update()
        
            

                



if __name__ == "__main__":
    main_menu() 
