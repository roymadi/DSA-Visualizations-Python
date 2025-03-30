import pygame
import time
import random
import os

pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)


WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()


font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
menu_font = pygame.font.SysFont("comicsansms", 50)


HIGH_SCORE_FILE = "highscore.txt"


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read())
    return 0


def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


def display_score(score):
    value = score_font.render("Score: " + str(score), True, BLUE)
    screen.blit(value, [10, 10])


def display_high_score(high_score):
    value = score_font.render("High Score: " + str(high_score), True, BLUE)
    screen.blit(value, [WIDTH - 280, 10])


def draw_snake(block_size, snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, GREEN, [segment[0], segment[1], block_size, block_size])


def message(msg, color, y_offset=0, font=font_style):
    mesg = font.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3 + y_offset])


def start_menu():
    menu = True
    difficulty = 10  # Default speed (Easy)
    while menu:
        screen.fill(BLACK)
        message("Snake Game", GREEN, -70, menu_font)
        message("Press S to Start", WHITE, 0)
        message("Press I for Instructions", WHITE, 50)
        message("Press D to Change Difficulty", WHITE, 100)
        message("Press Q to Quit", WHITE, 150)
        message(f"Current Difficulty: {get_difficulty_name(difficulty)}", WHITE, 200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu = False
                if event.key == pygame.K_i:
                    instructions()
                if event.key == pygame.K_d:
                    difficulty = change_difficulty(difficulty)
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

    return difficulty


def get_difficulty_name(speed):
    if speed == 5:
        return "Easy"
    elif speed == 10:
        return "Medium"
    elif speed == 15:
        return "Hard"
    return "Custom"


def change_difficulty(current_speed):
    speeds = [5, 10, 15]  
    current_index = speeds.index(current_speed) if current_speed in speeds else 0
    next_index = (current_index + 1) % len(speeds)
    return speeds[next_index]


def instructions():
    instruct = True
    while instruct:
        screen.fill(BLACK)
        message("Instructions:", GREEN, -70, menu_font)
        message("Use Arrow Keys to Move", WHITE, 0)
        message("Eat the Red Food to Grow", WHITE, 50)
        message("Avoid Walls and Yourself", WHITE, 100)
        message("Press B to Go Back", WHITE, 150)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    instruct = False


def game_loop(speed):
    game_over = False
    game_close = False

    x = WIDTH / 2
    y = HEIGHT / 2

    x_change = 0
    y_change = 0


    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE


    high_score = load_high_score()

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("You Lost! Press Q-Quit or C-Play Again", RED)
            display_score(snake_length - 1)
            display_high_score(high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = BLOCK_SIZE
                    x_change = 0

       
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += x_change
        y += y_change
        screen.fill(BLACK)

        
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        
        snake_head = [x, y]
        snake_list.append(snake_head)

     
        if len(snake_list) > snake_length:
            del snake_list[0]

    
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

     
        draw_snake(BLOCK_SIZE, snake_list)
        display_score(snake_length - 1)
        display_high_score(high_score)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

            if snake_length - 1 > high_score:
                high_score = snake_length - 1
                save_high_score(high_score)

        clock.tick(speed)

    pygame.quit()
    quit()

difficulty = start_menu()
game_loop(difficulty)