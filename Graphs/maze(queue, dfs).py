import pygame
import pygame_gui
import sys
import random
from collections import deque

WIDTH, HEIGHT = 800, 600
GRID_ROWS, GRID_COLS = 20, 20
CELL_SIZE = 25  
GRID_OFFSET_X = 50 
GRID_OFFSET_Y = 50

WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)  
STRIPE_COLOR = (70, 70, 70)  
BLUE = (66, 135, 245)
GREEN = (76, 187, 23)
RED = (219, 50, 54)
GREY = (200, 200, 200)
YELLOW = (255, 255, 0)

maze = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
start = (0, 0)
goal = (GRID_ROWS - 1, GRID_COLS - 1)

dfs_generator = None
dfs_path = []     
dfs_visited = set()  
step_delay = 100   

def reset_maze():
    global maze, dfs_generator, dfs_path, dfs_visited
    maze = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    dfs_generator = None
    dfs_path = []
    dfs_visited = set()

def generate_random_maze(prob_wall=0.3):
    global maze, dfs_generator, dfs_path, dfs_visited
    maze = [[1 if random.random() < prob_wall else 0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    maze[start[0]][start[1]] = 0
    maze[goal[0]][goal[1]] = 0
    dfs_generator = None
    dfs_path = []
    dfs_visited = set()

def draw_wall(surface, rect):
    pygame.draw.rect(surface, DARK_GRAY, rect)
    stripe_spacing = 4
    for x in range(rect.left, rect.right, stripe_spacing):
        pygame.draw.line(surface, STRIPE_COLOR, (x, rect.top), (x, rect.bottom), 1)

def draw_grid(surface):
    for i in range(GRID_ROWS):
        for j in range(GRID_COLS):
            x = GRID_OFFSET_X + j * CELL_SIZE
            y = GRID_OFFSET_Y + i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
         
            if (i, j) == start:
                pygame.draw.rect(surface, GREEN, rect)
            elif (i, j) == goal:
                pygame.draw.rect(surface, RED, rect)
            elif (i, j) in dfs_path:
                pygame.draw.rect(surface, BLUE, rect)
            elif maze[i][j] == 1:
                draw_wall(surface, rect)
            else:
                pygame.draw.rect(surface, WHITE, rect)
            
            pygame.draw.rect(surface, GREY, rect, 1)  

    for (i, j) in dfs_visited:
        if (i, j) not in dfs_path and (i, j) != start and (i, j) != goal:
            x = GRID_OFFSET_X + j * CELL_SIZE
            y = GRID_OFFSET_Y + i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, YELLOW, rect)

def dfs_generator_func(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    stack = [start]
    visited = set([start])
    parent = {start: None}

    while stack:
        current = stack.pop()
        yield ('visit', current, dict(parent), set(visited))
        if current == goal:
            break

        r, c = current
        # Explore neighbors: down, up, right, left
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                stack.append((nr, nc))
                visited.add((nr, nc))
                parent[(nr, nc)] = current
                yield ('visit', (nr, nc), dict(parent), set(visited))

    path = []
    node = goal if goal in parent else None
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()
    yield ('done', path, dict(parent), set(visited))

def main():
    global dfs_generator, dfs_path, dfs_visited, step_delay
    pygame.init()
    pygame.display.set_caption("Interactive Maze with Dynamic DFS Animation")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    start_dfs_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 100), (150, 50)),
        text='Start DFS',
        manager=manager
    )
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 200), (150, 50)),
        text='Reset Maze',
        manager=manager
    )
    random_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 300), (150, 50)),
        text='Random Maze',
        manager=manager
    )

    speed_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((600, 400), (150, 50)),
        start_value=step_delay,
        value_range=(10, 500),
        manager=manager
    )

    speed_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((600, 450), (150, 30)),
        text=f"Speed: {step_delay} ms",
        manager=manager
    )

    path_length_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((600, 500), (150, 50)),
        text="Path Length: N/A",
        manager=manager
    )

    is_dfs_running = False
    time_since_last_step = 0

    running = True
    while running:
        time_delta = clock.tick(60)
        time_since_last_step += time_delta

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (GRID_OFFSET_X <= mouse_x < GRID_OFFSET_X + GRID_COLS * CELL_SIZE and
                    GRID_OFFSET_Y <= mouse_y < GRID_OFFSET_Y + GRID_ROWS * CELL_SIZE):
                    j = (mouse_x - GRID_OFFSET_X) // CELL_SIZE
                    i = (mouse_y - GRID_OFFSET_Y) // CELL_SIZE
                    if (i, j) != start and (i, j) != goal:
                        maze[i][j] = 0 if maze[i][j] == 1 else 1
                        dfs_generator = None
                        dfs_path = []
                        dfs_visited = set()
                        path_length_label.set_text("Path Length: N/A")

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_dfs_button:
                        dfs_generator = dfs_generator_func(maze, start, goal)
                        dfs_path = []
                        dfs_visited = set()
                        is_dfs_running = True
                        path_length_label.set_text("Path Length: N/A")
                    if event.ui_element == reset_button:
                        reset_maze()
                        is_dfs_running = False
                        path_length_label.set_text("Path Length: N/A")
                    if event.ui_element == random_button:
                        generate_random_maze(prob_wall=0.3)
                        is_dfs_running = False
                        path_length_label.set_text("Path Length: N/A")
                elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == speed_slider:
                        step_delay = int(event.value)
                        speed_label.set_text(f"Speed: {step_delay} ms")

            manager.process_events(event)

        manager.update(time_delta)

        if is_dfs_running and dfs_generator and time_since_last_step >= step_delay:
            try:
                state, data, parent, visited = next(dfs_generator)
                dfs_visited = visited
                if state == 'done':
                    dfs_path = data
                    is_dfs_running = False
                    path_length_label.set_text(f"Path Length: {len(dfs_path)}")
                time_since_last_step = 0
            except StopIteration:
                is_dfs_running = False

        screen.fill(WHITE)
        draw_grid(screen)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()