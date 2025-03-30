import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

font = pygame.font.SysFont("Arial", 24)
large_font = pygame.font.SysFont("Arial", 36)

ROD_WIDTH = 10
ROD_HEIGHT = 300
ROD_GAP = 200
rod_positions = [
    (WIDTH // 4 - ROD_WIDTH // 2, HEIGHT // 2),
    (WIDTH // 2 - ROD_WIDTH // 2, HEIGHT // 2),
    (3 * WIDTH // 4 - ROD_WIDTH // 2, HEIGHT // 2),
]

DISK_HEIGHT = 20
MIN_DISK_WIDTH = 40
MAX_DISK_WIDTH = 200

num_disks = 3
rods = [[], [], []]  
selected_disk = None
selected_rod = None
moves = 0
game_started = False
show_instructions = False
show_victory = False

def initialize_rods():
    global rods
    rods = [[], [], []]
    for i in range(num_disks, 0, -1):
        rods[0].append(i)

def draw_rods():
    for pos in rod_positions:
        pygame.draw.rect(screen, BLACK, (pos[0], pos[1] - ROD_HEIGHT // 2, ROD_WIDTH, ROD_HEIGHT))

def draw_disks():
    for i, rod in enumerate(rods):
        for j, disk in enumerate(rod):
            disk_width = MIN_DISK_WIDTH + (disk - 1) * 20
            x = rod_positions[i][0] - disk_width // 2 + ROD_WIDTH // 2
            y = rod_positions[i][1] - (j + 1) * DISK_HEIGHT
            color = BLUE if disk == selected_disk else RED
            pygame.draw.rect(screen, color, (x, y, disk_width, DISK_HEIGHT))
            pygame.draw.rect(screen, BLACK, (x, y, disk_width, DISK_HEIGHT), 2) 

def display_menu():
    screen.fill(WHITE)
    title = large_font.render("Tower of Hanoi", True, BLACK)
    start_text = font.render("Press S to Start", True, BLACK)
    instructions_text = font.render("Press I for Instructions", True, BLACK)
    disk_text = font.render(f"Current Disks: {num_disks} (Press 3, 4, or 5 to Change)", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 300))
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, 350))
    screen.blit(disk_text, (WIDTH // 2 - disk_text.get_width() // 2, 400))
    pygame.display.flip()

def display_instructions():
    screen.fill(WHITE)
    instructions = [
        "How to Play:",
        "1. Click on a rod to select the top disk.",
        "2. Click on another rod to move the disk.",
        "3. You cannot place a larger disk on top of a smaller one.",
        "4. Move all disks to the rightmost rod to win.",
        "Press M to return to the main menu."
    ]
    y_offset = 100
    for line in instructions:
        text = font.render(line, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40
    pygame.display.flip()

def display_victory():
    screen.fill(WHITE)
    victory_text = large_font.render("You Win!", True, GREEN)
    moves_text = font.render(f"Moves: {moves}", True, BLACK)
    return_text = font.render("Press M to Return to Menu", True, BLACK)
    screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, 200))
    screen.blit(moves_text, (WIDTH // 2 - moves_text.get_width() // 2, 300))
    screen.blit(return_text, (WIDTH // 2 - return_text.get_width() // 2, 350))
    pygame.display.flip()

def check_win():
    return len(rods[2]) == num_disks

def main():
    global num_disks, rods, selected_disk, selected_rod, moves, game_started, show_instructions, show_victory

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if show_victory:
                    if event.key == pygame.K_m:  
                        show_victory = False
                elif not game_started and not show_instructions:
                    if event.key == pygame.K_s:  
                        game_started = True
                        initialize_rods()
                        moves = 0
                    elif event.key == pygame.K_i: 
                        show_instructions = True
                    elif event.key in [pygame.K_3, pygame.K_4, pygame.K_5]:  
                        num_disks = int(pygame.key.name(event.key))
                elif show_instructions:
                    if event.key == pygame.K_m:  
                        show_instructions = False
                elif game_started:
                    if event.key == pygame.K_m:  # Return to main menu
                        game_started = False

            if game_started and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                for i, pos in enumerate(rod_positions):
                    if pos[0] - 50 <= x <= pos[0] + 50 and pos[1] - ROD_HEIGHT // 2 <= y <= pos[1] + ROD_HEIGHT // 2:
                        if selected_disk is None:
                            if rods[i]:
                                selected_disk = rods[i][-1]
                                selected_rod = i
                        else:
                            if not rods[i] or rods[i][-1] > selected_disk:
                                rods[selected_rod].pop()
                                rods[i].append(selected_disk)
                                selected_disk = None
                                selected_rod = None
                                moves += 1
                                if check_win():
                                    show_victory = True
                                    game_started = False
                            else:
                                selected_disk = None
                                selected_rod = None

        screen.fill(WHITE)
        if show_victory:
            display_victory()
        elif show_instructions:
            display_instructions()
        elif game_started:
            draw_rods()
            draw_disks()
            text = font.render(f"Moves: {moves}", True, BLACK)
            screen.blit(text, (10, 10))
        else:
            display_menu()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()