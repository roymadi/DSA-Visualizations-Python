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

bfs_generator = None
bfs_path = []     
bfs_visited = set()  
step_delay = 100   

def reset_maze():
    global maze, bfs_generator, bfs_path, bfs_visited
    maze = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    bfs_generator = None
    bfs_path = []
    bfs_visited = set()

def generate_random_maze(prob_wall=0.3):
    global maze, bfs_generator, bfs_path, bfs_visited
    maze = [[1 if random.random() < prob_wall else 0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    maze[start[0]][start[1]] = 0
    maze[goal[0]][goal[1]] = 0
    bfs_generator = None
    bfs_path = []
    bfs_visited = set()

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
            elif (i, j) in bfs_path:
                pygame.draw.rect(surface, BLUE, rect)
            elif maze[i][j] == 1:
                draw_wall(surface, rect)
            else:
                pygame.draw.rect(surface, WHITE, rect)
            
            pygame.draw.rect(surface, GREY, rect, 1)  

    for (i, j) in bfs_visited:
        if (i, j) not in bfs_path and (i, j) != start and (i, j) != goal:
            x = GRID_OFFSET_X + j * CELL_SIZE
            y = GRID_OFFSET_Y + i * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, YELLOW, rect)

def bellman_ford_generator(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    distances = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    predecessors = [[None for _ in range(cols)] for _ in range(rows)]
    distances[start[0]][start[1]] = 0

    for _ in range(rows * cols - 1):
        updated = False
        updated_nodes = []
        for i in range(rows):
            for j in range(cols):
                if maze[i][j] == 1 or distances[i][j] == float('inf'):
                    continue  

                for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and maze[ni][nj] == 0:
                        if distances[i][j] + 1 < distances[ni][nj]:
                            distances[ni][nj] = distances[i][j] + 1
                            predecessors[ni][nj] = (i, j)
                            updated = True
                            updated_nodes.append((ni, nj))
        yield ('visit', updated_nodes, predecessors, distances.copy())
        if not updated:
            break  

    path = []
    node = goal
    if distances[goal[0]][goal[1]] != float('inf'):
        while node is not None:
            path.append(node)
            node = predecessors[node[0]][node[1]]
        path.reverse()
    yield ('done', path, predecessors, distances)

def main():
    global bfs_generator, bfs_path, bfs_visited, step_delay
    pygame.init()
    pygame.display.set_caption("Interactive Maze with Bellman-Ford Pathfinding")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    start_bfs_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((600, 100), (150, 50)),
        text='Start Bellman-Ford',
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

    is_bfs_running = False
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
                        bfs_generator = None
                        bfs_path = []
                        bfs_visited = set()
                        path_length_label.set_text("Path Length: N/A")

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_bfs_button:
                        bfs_generator = bellman_ford_generator(maze, start, goal)
                        bfs_path = []
                        bfs_visited = set()
                        is_bfs_running = True
                        path_length_label.set_text("Path Length: N/A")
                    if event.ui_element == reset_button:
                        reset_maze()
                        is_bfs_running = False
                        path_length_label.set_text("Path Length: N/A")
                    if event.ui_element == random_button:
                        generate_random_maze(prob_wall=0.3)
                        is_bfs_running = False
                        path_length_label.set_text("Path Length: N/A")
                elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == speed_slider:
                        step_delay = int(event.value)
                        speed_label.set_text(f"Speed: {step_delay} ms")

            manager.process_events(event)

        manager.update(time_delta)

        if is_bfs_running and bfs_generator and time_since_last_step >= step_delay:
            try:
                state, data, parent, distances = next(bfs_generator)
                if state == 'visit':
                    new_visits = data
                    bfs_visited.update(new_visits)
                elif state == 'done':
                    bfs_path = data
                    is_bfs_running = False
                    path_length_label.set_text(f"Path Length: {len(bfs_path)}")
                time_since_last_step = 0
            except StopIteration:
                is_bfs_running = False

        screen.fill(WHITE)
        draw_grid(screen)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()