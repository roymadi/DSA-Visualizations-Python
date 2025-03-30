import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (100, 200, 100)
TREASURE_COLOR = (255, 215, 0)
BUTTON_COLOR = (50, 150, 250)
BUTTON_HOVER = (30, 100, 200)
TREASURE_OUTLINE = (150, 100, 50) 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Treasure Hunt - Divide & Conquer")
font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 30)

grid_size = 4
tile_size = WIDTH // grid_size
score = 0
attempts = 0
treasure_pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
found_treasure = False

def draw_grid():
    for x in range(0, WIDTH, tile_size):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, tile_size):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y))

def draw_treasure(x, y):
    cell_x, cell_y = x * tile_size, y * tile_size
    pygame.draw.rect(screen, TREASURE_COLOR, (cell_x, cell_y, tile_size, tile_size))  # Yellow base

    pygame.draw.rect(screen, TREASURE_OUTLINE, (cell_x + 10, cell_y + 25, tile_size - 20, tile_size - 35), border_radius=5)
    pygame.draw.rect(screen, TREASURE_OUTLINE, (cell_x + 20, cell_y + 15, tile_size - 40, 10))  # Chest lid

    pygame.draw.circle(screen, (255, 223, 0), (cell_x + tile_size // 2, cell_y + tile_size - 20), 5)

def get_hint(selected_pos):
    if selected_pos == treasure_pos:
        return "You found the Treasure!"
    elif selected_pos[0] > treasure_pos[0]:
        return "Go Left"
    elif selected_pos[0] < treasure_pos[0]:
        return "Go Right"
    elif selected_pos[1] > treasure_pos[1]:
        return "Go Up"
    elif selected_pos[1] < treasure_pos[1]:
        return "Go Down"

def draw_button(text, x, y, w, h, hover=False):
    color = BUTTON_HOVER if hover else BUTTON_COLOR
    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    text_surface = button_font.render(text, True, TEXT_COLOR)
    screen.blit(text_surface, (x + w // 4, y + h // 4))

def main():
    global attempts, found_treasure, treasure_pos, score, grid_size, tile_size
    running = True
    selected_pos = None
    hint_text = "Find the Treasure!"

    while running:
        screen.fill(BG_COLOR)
        draw_grid()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_hover = 200 <= mouse_x <= 400 and 500 <= mouse_y <= 550

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not found_treasure:
                x, y = pygame.mouse.get_pos()
                selected_pos = (x // tile_size, y // tile_size)
                attempts += 1
                hint_text = get_hint(selected_pos)
                if selected_pos == treasure_pos:
                    found_treasure = True
                    score += max(100 - (attempts * 5), 10)
            if event.type == pygame.MOUSEBUTTONDOWN and found_treasure:
                if button_hover:
                    grid_size += 1 if grid_size < 8 else 0
                    tile_size = WIDTH // grid_size
                    treasure_pos = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))
                    attempts = 0
                    found_treasure = False
                    hint_text = "Find the Treasure!"

        if selected_pos and not found_treasure:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (selected_pos[0] * tile_size, selected_pos[1] * tile_size, tile_size, tile_size))

        if found_treasure:
            draw_treasure(treasure_pos[0], treasure_pos[1])
            hint_text = f"Congratulations! Found in {attempts} attempts!"
            draw_button("Next Level", 200, 500, 200, 50, button_hover)

        hint_surface = font.render(hint_text, True, TEXT_COLOR)
        score_surface = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(hint_surface, (20, 20))
        screen.blit(score_surface, (20, 60))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()