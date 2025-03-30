import pygame
import random
import sys
import heapq
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import time

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)
DARKER_GRAY = (20, 20, 20)
GRID_COLOR = (50, 50, 50)


SHAPES = {
    'I': {'shape': [
        ['.....',
         '.....',
         'IIII.',
         '.....',
         '.....'],
        ['..I..',
         '..I..',
         '..I..',
         '..I..',
         '.....']
    ], 'color': (0, 255, 255)},  
    'J': {'shape': [
        ['.....',
         '.J...',
         '.JJJ.',
         '.....',
         '.....'],
        ['.....',
         '..JJ.',
         '..J..',
         '..J..',
         '.....'],
        ['.....',
         '.....',
         '.JJJ.',
         '...J.',
         '.....'],
        ['.....',
         '..J..',
         '..J..',
         '.JJ..',
         '.....']
    ], 'color': (0, 0, 255)},  
    'L': {'shape': [
        ['.....',
         '...L.',
         '.LLL.',
         '.....',
         '.....'],
        ['.....',
         '..L..',
         '..L..',
         '..LL.',
         '.....'],
        ['.....',
         '.....',
         '.LLL.',
         '.L...',
         '.....'],
        ['.....',
         '.LL..',
         '..L..',
         '..L..',
         '.....']
    ], 'color': (255, 165, 0)},  
    'O': {'shape': [
        ['.....',
         '.....',
         '.OO..',
         '.OO..',
         '.....']
    ], 'color': (255, 255, 0)},  
    'S': {'shape': [
        ['.....',
         '.....',
         '..SS.',
         '.SS..',
         '.....'],
        ['.....',
         '..S..',
         '..SS.',
         '...S.',
         '.....']
    ], 'color': (0, 255, 0)}, 
    'T': {'shape': [
        ['.....',
         '..T..',
         '.TTT.',
         '.....',
         '.....'],
        ['.....',
         '..T..',
         '..TT.',
         '..T..',
         '.....'],
        ['.....',
         '.....',
         '.TTT.',
         '..T..',
         '.....'],
        ['.....',
         '..T..',
         '.TT..',
         '..T..',
         '.....']
    ], 'color': (128, 0, 128)}, 
    'Z': {'shape': [
        ['.....',
         '.....',
         '.ZZ..',
         '..ZZ.',
         '.....'],
        ['.....',
         '...Z.',
         '..ZZ.',
         '..Z..',
         '.....']
    ], 'color': (255, 0, 0)}  
}


CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700


PRIORITY_VALUES = {
    'I': 1,  
    'T': 2,  
    'L': 3,  
    'J': 3,
    'O': 4,  
    'S': 5,  
    'Z': 5
}

@dataclass(order=True)
class PrioritizedBlock:
    priority: int
    block_type: str = field(compare=False)
    creation_time: float = field(compare=False)

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.next_pieces = []
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.last_move_time = time.time()
        
        self.block_heap = []
        self.initialize_block_heap()
        
        self.new_piece()
        
        self.title_font = pygame.font.Font(None, 48)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        self.fall_speed = 0.5
    
    def initialize_block_heap(self):
        for block_type in SHAPES.keys():
           
            for i in range(3):  
                creation_time = time.time() + (i * 0.001)
                priority = PRIORITY_VALUES[block_type]
                adjusted_priority = priority + random.uniform(-0.1, 0.1)
                heapq.heappush(self.block_heap, PrioritizedBlock(
                    priority=adjusted_priority,
                    block_type=block_type,
                    creation_time=creation_time
                ))
    
    def refill_heap_if_needed(self):
        if len(self.block_heap) < 10:
            for block_type in SHAPES.keys():
                creation_time = time.time()
                priority = PRIORITY_VALUES[block_type]
                adjusted_priority = priority + random.uniform(-0.1, 0.1)
                heapq.heappush(self.block_heap, PrioritizedBlock(
                    priority=adjusted_priority,
                    block_type=block_type,
                    creation_time=creation_time
                ))
    
    def new_piece(self):
        if not self.block_heap:
            self.initialize_block_heap()
        
        prioritized_block = heapq.heappop(self.block_heap)
        shape_key = prioritized_block.block_type
        
        self.refill_heap_if_needed()
        
        shape_data = SHAPES[shape_key]
        self.current_piece = {
            'shape': shape_data['shape'][0],
            'color': shape_data['color'],
            'x': GRID_WIDTH // 2 - 2,
            'y': 0,
            'rotation': 0,
            'type': shape_key
        }
        
        if not self.valid_position():
            self.game_over = True
    
    def get_shape_coords(self, shape):
        coords = []
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell != '.':
                    coords.append((j, i))
        return coords
    
    def valid_position(self, x=None, y=None, shape=None):
        if x is None:
            x = self.current_piece['x']
        if y is None:
            y = self.current_piece['y']
        if shape is None:
            shape = self.current_piece['shape']
        
        coords = self.get_shape_coords(shape)
        
        for cx, cy in coords:
            nx, ny = x + cx, y + cy
            
            if nx < 0 or nx >= GRID_WIDTH or ny >= GRID_HEIGHT:
                return False
            
            if ny >= 0 and self.grid[ny][nx] != 0:
                return False
        
        return True
    
    def rotate_piece(self):
        if self.current_piece['type'] == 'O':  
            return
        
        shape_data = SHAPES[self.current_piece['type']]
        next_rotation = (self.current_piece['rotation'] + 1) % len(shape_data['shape'])
        next_shape = shape_data['shape'][next_rotation]
        
        if self.valid_position(shape=next_shape):
            self.current_piece['rotation'] = next_rotation
            self.current_piece['shape'] = next_shape
    
    def move_left(self):
        if self.valid_position(x=self.current_piece['x'] - 1):
            self.current_piece['x'] -= 1
    
    def move_right(self):
        if self.valid_position(x=self.current_piece['x'] + 1):
            self.current_piece['x'] += 1
    
    def move_down(self):
        if self.valid_position(y=self.current_piece['y'] + 1):
            self.current_piece['y'] += 1
            return True
        else:
            self.lock_piece()
            return False
    
    def drop(self):
        while self.move_down():
            pass
    
    def lock_piece(self):
        coords = self.get_shape_coords(self.current_piece['shape'])
        
        for cx, cy in coords:
            nx, ny = self.current_piece['x'] + cx, self.current_piece['y'] + cy
            if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                self.grid[ny][nx] = self.current_piece['color']
        
        self.clear_lines()
        
        self.new_piece()
    
    def clear_lines(self):
        lines_to_clear = []
        
        for i, row in enumerate(self.grid):
            if all(cell != 0 for cell in row):
                lines_to_clear.append(i)
        
        if lines_to_clear:
            for line in sorted(lines_to_clear, reverse=True):
                del self.grid[line]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
            
            lines_count = len(lines_to_clear)
            self.lines_cleared += lines_count
            self.score += lines_count * lines_count * 100 * self.level
            
            self.level = max(1, self.lines_cleared // 10 + 1)
            self.fall_speed = max(0.1, 0.5 - (self.level - 1) * 0.05)
    
    def draw_grid(self):
        self.screen.fill(BLACK)
        
        play_area_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - (GRID_WIDTH * CELL_SIZE) // 2,
            50,
            GRID_WIDTH * CELL_SIZE,
            GRID_HEIGHT * CELL_SIZE
        )
        pygame.draw.rect(self.screen, DARKER_GRAY, play_area_rect)
        
        for i in range(GRID_WIDTH + 1):
            x = play_area_rect.left + i * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COLOR, (x, play_area_rect.top), (x, play_area_rect.bottom))
        
        for i in range(GRID_HEIGHT + 1):
            y = play_area_rect.top + i * CELL_SIZE
            pygame.draw.line(self.screen, GRID_COLOR, (play_area_rect.left, y), (play_area_rect.right, y))
        
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell != 0:
                    rect = pygame.Rect(
                        play_area_rect.left + x * CELL_SIZE,
                        play_area_rect.top + y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, cell, rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
        
        if self.current_piece:
            for cx, cy in self.get_shape_coords(self.current_piece['shape']):
                x = self.current_piece['x'] + cx
                y = self.current_piece['y'] + cy
                
                if y >= 0:  
                    rect = pygame.Rect(
                        play_area_rect.left + x * CELL_SIZE,
                        play_area_rect.top + y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, self.current_piece['color'], rect)
                    pygame.draw.rect(self.screen, WHITE, rect, 1)
        
        info_panel = pygame.Rect(play_area_rect.right + 20, play_area_rect.top, 200, 400)
        pygame.draw.rect(self.screen, GRAY, info_panel)
        
        if self.block_heap:
            next_blocks = []
            temp_heap = self.block_heap.copy()
            
            for _ in range(min(3, len(temp_heap))):
                next_blocks.append(heapq.heappop(temp_heap))
            
            next_text = self.font.render("Next Blocks:", True, WHITE)
            self.screen.blit(next_text, (info_panel.left + 10, info_panel.top + 10))
            
            for i, block in enumerate(next_blocks):
                shape_key = block.block_type
                shape_data = SHAPES[shape_key]
                
                block_text = self.small_font.render(
                    f"{shape_key} (Priority: {block.priority:.1f})", 
                    True, 
                    WHITE
                )
                self.screen.blit(block_text, (info_panel.left + 10, info_panel.top + 50 + i * 100))
                
                shape = shape_data['shape'][0]
                for cy, row in enumerate(shape):
                    for cx, cell in enumerate(row):
                        if cell != '.':
                            preview_rect = pygame.Rect(
                                info_panel.left + 20 + cx * (CELL_SIZE // 2),
                                info_panel.top + 80 + i * 100 + cy * (CELL_SIZE // 2),
                                CELL_SIZE // 2,
                                CELL_SIZE // 2
                            )
                            pygame.draw.rect(self.screen, shape_data['color'], preview_rect)
                            pygame.draw.rect(self.screen, WHITE, preview_rect, 1)
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, WHITE)
        
        self.screen.blit(score_text, (info_panel.left + 10, info_panel.top + 350))
        self.screen.blit(level_text, (info_panel.left + 10, info_panel.top + 390))
        self.screen.blit(lines_text, (info_panel.left + 10, info_panel.top + 430))
        
        title_text = self.title_font.render("Tetris", True, WHITE)
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 10))
        
        controls_y = play_area_rect.bottom + 20
        controls_text = self.small_font.render(
            "Controls: side arrow to move, up arrow to rotate, down arrow to move down, Space to drop, Q to quit", 
            True, 
            WHITE
        )
        self.screen.blit(
            controls_text, 
            (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, controls_y)
        )
        
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.title_font.render("GAME OVER", True, WHITE)
            restart_text = self.font.render("Press R to restart", True, WHITE)
            
            self.screen.blit(
                game_over_text, 
                (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50)
            )
            self.screen.blit(
                restart_text, 
                (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10)
            )
    
    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = None
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.last_move_time = time.time()
        
        self.block_heap = []
        self.initialize_block_heap()
        
        self.new_piece()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if not self.game_over:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.move_left()
                        elif event.key == pygame.K_RIGHT:
                            self.move_right()
                        elif event.key == pygame.K_UP:
                            self.rotate_piece()
                        elif event.key == pygame.K_DOWN:
                            self.move_down()
                        elif event.key == pygame.K_SPACE:
                            self.drop()
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.reset_game()
            
            if not self.game_over and time.time() - self.last_move_time > self.fall_speed:
                self.move_down()
                self.last_move_time = time.time()
            
            self.draw_grid()
            
            pygame.display.flip()
            
            self.clock.tick(self.fps)

if __name__ == "__main__":
    game = TetrisGame()
    game.run()