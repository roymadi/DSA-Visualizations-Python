import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 300, 420  
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
FONT_SIZE = 40
BUTTON_HEIGHT = 70
MENU_HEIGHT = 60
ANIMATION_SPEED = 10  

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BUTTON_COLOR = (52, 152, 219)
TEXT_COLOR = (255, 255, 255)
MENU_COLOR = (41, 128, 185)
HIGHLIGHT_COLOR = (52, 152, 219)
RESULT_COLOR = (255, 0, 0)
POPUP_COLOR = (255, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

font = pygame.font.SysFont("Arial", FONT_SIZE)
menu_font = pygame.font.SysFont("Arial", 20)
result_font = pygame.font.SysFont("Arial", 30)
popup_font = pygame.font.SysFont("Arial", 25)

board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

EASY = "Easy"
MEDIUM = "Medium"
HARD = "Hard"
difficulty_levels = [EASY, MEDIUM, HARD]
difficulty = MEDIUM 

MENU = "menu"
PLAYING = "playing"
game_state = PLAYING 

fade_alpha = 0
winning_line = None  
result_text = None 
popup_text = None  
popup_timer = 0  


def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 3 * SQUARE_SIZE), (WIDTH, 3 * SQUARE_SIZE), LINE_WIDTH)

    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT - BUTTON_HEIGHT - MENU_HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT - BUTTON_HEIGHT - MENU_HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                surface = pygame.Surface((CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2), pygame.SRCALPHA)
                pygame.draw.circle(surface, (*CIRCLE_COLOR, fade_alpha), (CIRCLE_RADIUS, CIRCLE_RADIUS), CIRCLE_RADIUS, LINE_WIDTH)
                screen.blit(surface, (col * SQUARE_SIZE + SQUARE_SIZE // 2 - CIRCLE_RADIUS, row * SQUARE_SIZE + SQUARE_SIZE // 2 - CIRCLE_RADIUS))
            elif board[row][col] == "X":
                surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                pygame.draw.line(surface, (*CROSS_COLOR, fade_alpha), (SPACE, SQUARE_SIZE - SPACE), (SQUARE_SIZE - SPACE, SPACE), CROSS_WIDTH)
                pygame.draw.line(surface, (*CROSS_COLOR, fade_alpha), (SPACE, SPACE), (SQUARE_SIZE - SPACE, SQUARE_SIZE - SPACE), CROSS_WIDTH)
                screen.blit(surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))


def check_winner(board, player):
    for row in range(3):
        if all([cell == player for cell in board[row]]):
            return ("row", row)
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return ("col", col)

    if all([board[i][i] == player for i in range(3)]):
        return ("diag1", 0)
    if all([board[i][2 - i] == player for i in range(3)]):
        return ("diag2", 0)
    return None


def is_board_full(board):
    return all([cell is not None for row in board for cell in row])


def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 1
    elif check_winner(board, "X"):
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = None
                    best_score = min(score, best_score)
        return best_score


def ai_move():
    if difficulty == EASY:
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] is None]
        if empty_cells:
            row, col = random.choice(empty_cells)
            board[row][col] = "O"
    elif difficulty == MEDIUM:
        if random.random() < 0.4:
            empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] is None]
            if empty_cells:
                row, col = random.choice(empty_cells)
                board[row][col] = "O"
        else:
            best_score = -float("inf")
            move = None
            for row in range(3):
                for col in range(3):
                    if board[row][col] is None:
                        board[row][col] = "O"
                        score = minimax(board, 0, False)
                        board[row][col] = None
                        if score > best_score:
                            best_score = score
                            move = (row, col)
            if move:
                board[move[0]][move[1]] = "O"
    elif difficulty == HARD:
        best_score = -float("inf")
        move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = "O"
                    score = minimax(board, 0, False)
                    board[row][col] = None
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        if move:
            board[move[0]][move[1]] = "O"


def draw_menu():
    pygame.draw.rect(screen, MENU_COLOR, (0, HEIGHT - BUTTON_HEIGHT - MENU_HEIGHT, WIDTH, MENU_HEIGHT))
    for i, level in enumerate(difficulty_levels):
        text = menu_font.render(level, True, TEXT_COLOR if difficulty != level else HIGHLIGHT_COLOR)
        screen.blit(text, (i * (WIDTH // 3) + 20, HEIGHT - BUTTON_HEIGHT - MENU_HEIGHT + 15))


def draw_restart_button():
    pygame.draw.rect(screen, BUTTON_COLOR, (0, HEIGHT - BUTTON_HEIGHT, WIDTH, BUTTON_HEIGHT))
    text = font.render("Restart", True, TEXT_COLOR)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - BUTTON_HEIGHT + 10))


def reset_game():
    global board, player_turn, fade_alpha, winning_line, result_text
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player_turn = True
    fade_alpha = 0
    winning_line = None
    result_text = None
    screen.fill(BG_COLOR)
    draw_lines()
    draw_menu()
    draw_restart_button()
    pygame.display.update()


def draw_winning_line():
    if winning_line:
        line_type, index = winning_line
        if line_type == "row":
            start_pos = (0, (index + 0.5) * SQUARE_SIZE)
            end_pos = (WIDTH, (index + 0.5) * SQUARE_SIZE)
        elif line_type == "col":
            start_pos = ((index + 0.5) * SQUARE_SIZE, 0)
            end_pos = ((index + 0.5) * SQUARE_SIZE, HEIGHT - BUTTON_HEIGHT - MENU_HEIGHT)
        elif line_type == "diag1":
            start_pos = (0, 0)
            end_pos = (WIDTH, HEIGHT - BUTTON_HEIGHT - MENU_HEIGHT)
        elif line_type == "diag2":
            start_pos = (WIDTH, 0)
            end_pos = (0, HEIGHT - BUTTON_HEIGHT - MENU_HEIGHT)
        pygame.draw.line(screen, RESULT_COLOR, start_pos, end_pos, LINE_WIDTH * 2)


def draw_result():
    if result_text:
        text_surface = result_font.render(result_text, True, RESULT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, text_rect)


def draw_popup():
    if popup_text:
        text_surface = popup_font.render(popup_text, True, POPUP_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text_surface, text_rect)


def main():
    global difficulty, game_state, fade_alpha, winning_line, result_text, popup_text, popup_timer
    reset_game()
    player_turn = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if game_state == MENU:
                    for i, level in enumerate(difficulty_levels):
                        if i * (WIDTH // 3) <= mouseX < (i + 1) * (WIDTH // 3) and HEIGHT - BUTTON_HEIGHT - MENU_HEIGHT <= mouseY < HEIGHT - BUTTON_HEIGHT:
                            difficulty = level
                            game_state = PLAYING
                            reset_game()
                elif game_state == PLAYING:
                    if mouseY < HEIGHT - BUTTON_HEIGHT - MENU_HEIGHT: 
                        if player_turn:
                            clicked_row = mouseY // SQUARE_SIZE
                            clicked_col = mouseX // SQUARE_SIZE

                            if board[clicked_row][clicked_col] is None:
                                board[clicked_row][clicked_col] = "X"
                                player_turn = False

                                winner = check_winner(board, "X")
                                if winner:
                                    winning_line = winner
                                    result_text = "You Won!"
                                elif is_board_full(board):
                                    result_text = "It's a Tie!"
                                else:
                                    draw_figures()
                                    pygame.display.update()
                    elif HEIGHT - BUTTON_HEIGHT <= mouseY < HEIGHT: 
                        popup_text = "Select Difficulty Level"
                        popup_timer = pygame.time.get_ticks() + 2000  
                        reset_game()
                        game_state = MENU

        if game_state == PLAYING and not player_turn:
            ai_move()
            player_turn = True

            winner = check_winner(board, "O")
            if winner:
                winning_line = winner
                result_text = "You Lose!"
            elif is_board_full(board):
                result_text = "It's a Tie!"
            else:
                draw_figures()
                pygame.display.update()

        if fade_alpha < 255:
            fade_alpha += ANIMATION_SPEED
            if fade_alpha > 255:
                fade_alpha = 255

        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        draw_menu()
        draw_restart_button()
        if winning_line:
            draw_winning_line()
        if result_text:
            draw_result()
        if popup_text and pygame.time.get_ticks() < popup_timer:
            draw_popup()
        pygame.display.update()


if __name__ == "__main__":
    main()