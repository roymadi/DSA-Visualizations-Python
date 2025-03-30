import pygame
import math
import heapq
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense with A* Pathfinding")


WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
GRAY      = ( 50,  50,  50)
GREEN     = (  0, 255,   0)
RED       = (255,   0,   0)
BLUE      = (  0,   0, 255)
LIGHTBLUE = (173, 216, 230)
DARKGRAY  = (100, 100, 100)

ROWS = 15
COLS = 20
TILE_SIZE = WIDTH // COLS 


grid = None
start = (0, ROWS // 2)
end = (COLS - 1, ROWS // 2)

def reset_grid():
    global grid
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
   
    for i in range(5, 10):
        grid[ROWS // 2 - 1][i] = 1


class Node:
    def __init__(self, pos, parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, end, grid):
    open_list = []
    closed_set = set()
    start_node = Node(start)
    heapq.heappush(open_list, (start_node.f, start_node))

    while open_list:
        current = heapq.heappop(open_list)[1]
        if current.pos == end:
            path = []
            while current:
                path.append(current.pos)
                current = current.parent
            return path[::-1]
        closed_set.add(current.pos)
        x, y = current.pos
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        for pos in neighbors:
            nx, ny = pos
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                if grid[ny][nx] == 1 or pos in closed_set:
                    continue
                neighbor = Node(pos, current)
                neighbor.g = current.g + 1
                neighbor.h = heuristic(pos, end)
                neighbor.f = neighbor.g + neighbor.h
              
                skip = False
                for _, n in open_list:
                    if n.pos == neighbor.pos and n.f <= neighbor.f:
                        skip = True
                        break
                if not skip:
                    heapq.heappush(open_list, (neighbor.f, neighbor))
    return None


class Enemy:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.path = a_star(start, end, grid)
        self.current_index = 0
        self.x, self.y = self.get_pos_from_grid(self.path[self.current_index])
        self.speed = 2 
        self.radius = TILE_SIZE // 4
        self.health = 100

    def get_pos_from_grid(self, pos):
        grid_x, grid_y = pos
     
        return grid_x * TILE_SIZE + TILE_SIZE // 2, grid_y * TILE_SIZE + TILE_SIZE // 2

    def update(self):
        if self.current_index < len(self.path) - 1:
            target = self.get_pos_from_grid(self.path[self.current_index + 1])
            dx = target[0] - self.x
            dy = target[1] - self.y
            dist = math.hypot(dx, dy)
            if dist == 0:
                self.current_index += 1
            else:
                dx, dy = dx / dist, dy / dist
                self.x += dx * self.speed
                self.y += dy * self.speed
               
                if math.hypot(target[0] - self.x, target[1] - self.y) < self.speed:
                    self.current_index += 1

    def draw(self, win):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), self.radius)
      
        bar_width = self.radius * 2
        pygame.draw.rect(win, BLACK, (self.x - self.radius, self.y - self.radius - 10, bar_width, 5))
        pygame.draw.rect(win, GREEN, (self.x - self.radius, self.y - self.radius - 10, bar_width * (self.health / 100), 5))

class Tower:
    def __init__(self, pos):
        self.pos = pos  
        self.x = pos[0] * TILE_SIZE + TILE_SIZE // 2
        self.y = pos[1] * TILE_SIZE + TILE_SIZE // 2
        self.range = TILE_SIZE * 3
        self.fire_rate = 60  
        self.timer = 0
        self.damage = 20

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def draw(self, win):
        pygame.draw.circle(win, BLUE, (self.x, self.y), TILE_SIZE // 2)
     
        pygame.draw.circle(win, LIGHTBLUE, (self.x, self.y), self.range, 1)

    def can_fire(self):
        return self.timer == 0

    def reset_timer(self):
        self.timer = self.fire_rate

    def shoot(self, enemy):
        enemy.health -= self.damage


def draw_grid(win, grid):
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if grid[y][x] == 1:
                pygame.draw.rect(win, GRAY, rect)
            else:
                pygame.draw.rect(win, WHITE, rect)
           

def draw_start_end(win):
 
    start_rect = pygame.Rect(start[0] * TILE_SIZE, start[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    end_rect = pygame.Rect(end[0] * TILE_SIZE, end[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(win, GREEN, start_rect)
    pygame.draw.rect(win, RED, end_rect)

def draw_gold(win, gold):
    font = pygame.font.SysFont("Arial", 24)
    text_surface = font.render(f"Gold: {gold}", True, BLACK)
    win.blit(text_surface, (10, 10))

def draw_stats(win, kills, passes):
    font = pygame.font.SysFont("Arial", 24)
    stats_text = font.render(f"Kills: {kills}  Passes: {passes}", True, BLACK)
    win.blit(stats_text, (10, 40))

def draw_game_over(win, message):
    font = pygame.font.SysFont("Arial", 48)
    text_surface = font.render(message, True, BLACK)
    win.fill(WHITE)
    win.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, HEIGHT//2 - text_surface.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def start_screen():
    font = pygame.font.SysFont("Arial", 24)
    large_font = pygame.font.SysFont("Arial", 36)
    
 
    easy_button = pygame.Rect(50, HEIGHT - 140, 150, 50)
    medium_button = pygame.Rect(WIDTH//2 - 75, HEIGHT - 140, 150, 50)
    hard_button = pygame.Rect(WIDTH - 200, HEIGHT - 140, 150, 50)
    start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT - 70, 100, 50)
    
  
    difficulty_settings = {
        "Easy": {"gold": 600, "spawn_interval": 100, "win_kills": 25, "lose_passes": 15},
        "Medium": {"gold": 450, "spawn_interval": 80, "win_kills": 20, "lose_passes": 10},
        "Hard": {"gold": 300, "spawn_interval": 70, "win_kills": 15, "lose_passes": 10}
    }
    selected_difficulty = "Medium" 

    gold = difficulty_settings[selected_difficulty]["gold"]
    running = True

    while running:
        WIN.fill(WHITE)
        draw_grid(WIN, grid)
        draw_start_end(WIN)
        draw_gold(WIN, gold)
        

        title_surface = large_font.render("Tower Defense Challenge!", True, BLACK)
        WIN.blit(title_surface, (WIDTH//2 - title_surface.get_width()//2, 10))
        
        instructions = [
            "Right-click on grid cells to toggle obstacles (Cost: 10 gold).",
            "Left-click to place towers (Cost: 150 gold). ",
            "Defend against waves: if enough enemies pass, you lose; eliminate enough enemies to win.",
            "Select a difficulty and click START when ready."
        ]
        for idx, line in enumerate(instructions):
            text_surface = font.render(line, True, BLACK)
            WIN.blit(text_surface, (WIDTH//2 - text_surface.get_width()//2, 70 + idx * 30))
        

        pygame.draw.rect(WIN, LIGHTBLUE if selected_difficulty == "Easy" else DARKGRAY, easy_button)
        easy_text = font.render("Easy", True, BLACK)
        WIN.blit(easy_text, (easy_button.x + easy_button.width//2 - easy_text.get_width()//2,
                             easy_button.y + easy_button.height//2 - easy_text.get_height()//2))
        
        pygame.draw.rect(WIN, LIGHTBLUE if selected_difficulty == "Medium" else DARKGRAY, medium_button)
        med_text = font.render("Medium", True, BLACK)
        WIN.blit(med_text, (medium_button.x + medium_button.width//2 - med_text.get_width()//2,
                             medium_button.y + medium_button.height//2 - med_text.get_height()//2))
        
        pygame.draw.rect(WIN, LIGHTBLUE if selected_difficulty == "Hard" else DARKGRAY, hard_button)
        hard_text = font.render("Hard", True, BLACK)
        WIN.blit(hard_text, (hard_button.x + hard_button.width//2 - hard_text.get_width()//2,
                             hard_button.y + hard_button.height//2 - hard_text.get_height()//2))
        
      
        pygame.draw.rect(WIN, LIGHTBLUE, start_button)
        start_text = large_font.render("START", True, BLACK)
        WIN.blit(start_text, (start_button.x + start_button.width//2 - start_text.get_width()//2,
                              start_button.y + start_button.height//2 - start_text.get_height()//2))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mx, my = pygame.mouse.get_pos()
                grid_pos = (mx // TILE_SIZE, my // TILE_SIZE)
                gx, gy = grid_pos
                if 0 <= gx < COLS and 0 <= gy < ROWS:
                    if grid[gy][gx] == 0 and gold >= 10:
                        grid[gy][gx] = 1
                        gold -= 10
                    elif grid[gy][gx] == 1:
                        grid[gy][gx] = 0
                        gold += 10
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
              
                if easy_button.collidepoint((mx, my)):
                    selected_difficulty = "Easy"
                    gold = difficulty_settings[selected_difficulty]["gold"]
                elif medium_button.collidepoint((mx, my)):
                    selected_difficulty = "Medium"
                    gold = difficulty_settings[selected_difficulty]["gold"]
                elif hard_button.collidepoint((mx, my)):
                    selected_difficulty = "Hard"
                    gold = difficulty_settings[selected_difficulty]["gold"]
           
                elif start_button.collidepoint((mx, my)):
                    running = False
        pygame.time.delay(20)
    return difficulty_settings[selected_difficulty]


def game_loop(difficulty):
    clock = pygame.time.Clock()
    enemies = []
    towers = []
    spawn_timer = 0
   
    current_spawn_interval = difficulty["spawn_interval"]
    time_counter = 0  

    gold = difficulty["gold"]
    kill_count = 0
    pass_count = 0

    running = True
    while running:
        dt = clock.tick(60)  
        time_counter += dt / 1000.0 
        
        
        if time_counter > 10:
           
            current_spawn_interval = max(20, current_spawn_interval - 10)
            time_counter = 0  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                grid_pos = (mx // TILE_SIZE, my // TILE_SIZE)
                if grid_pos != start and grid_pos != end:
                    if not any(tower.pos == grid_pos for tower in towers):
                        if gold >= 150:
                            towers.append(Tower(grid_pos))
                            gold -= 150
         
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mx, my = pygame.mouse.get_pos()
                grid_pos = (mx // TILE_SIZE, my // TILE_SIZE)
                gx, gy = grid_pos
                if 0 <= gx < COLS and 0 <= gy < ROWS:
                    if grid[gy][gx] == 0 and gold >= 10:
                        grid[gy][gx] = 1
                        gold -= 10
                    elif grid[gy][gx] == 1:
                        grid[gy][gx] = 0
                        gold += 10

   
        spawn_timer += 1
        if spawn_timer >= current_spawn_interval:
            enemy = Enemy(grid, start, end)
            if enemy.path:  
                enemies.append(enemy)
            spawn_timer = 0


        for enemy in enemies[:]:
            enemy.update()
            if enemy.health <= 0:
                enemies.remove(enemy)
                gold += 100  # reward for killing an enemy
                kill_count += 1
            elif enemy.current_index >= len(enemy.path) - 1:
                enemies.remove(enemy)
                pass_count += 1


        if pass_count >= difficulty["lose_passes"]:
            draw_game_over(WIN, "You Lose!")
            running = False
        if kill_count >= difficulty["win_kills"]:
            draw_game_over(WIN, "You Win!")
            running = False


        for tower in towers:
            tower.update()
            for enemy in enemies:
                distance = math.hypot(tower.x - enemy.x, tower.y - enemy.y)
                if distance <= tower.range and tower.can_fire():
                    tower.shoot(enemy)
                    tower.reset_timer()
                    break


        WIN.fill(WHITE)
        draw_grid(WIN, grid)
        draw_start_end(WIN)
        for tower in towers:
            tower.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
        draw_gold(WIN, gold)
        draw_stats(WIN, kill_count, pass_count)
        pygame.display.update()

    return gold

def main():
    while True:
        reset_grid() 
        difficulty = start_screen() 
        _ = game_loop(difficulty)

if __name__ == "__main__":
    main()
