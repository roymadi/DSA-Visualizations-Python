import pygame
import random
import sys
import time

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualizer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BAR_COLOR = (30, 144, 255)
PURPLE = (147, 112, 219)

title_font = pygame.font.SysFont("Arial", 36, bold=True)
font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 16)

NUM_BARS = 30
MAX_BAR_HEIGHT = HEIGHT - 200
MIN_BAR_HEIGHT = 50
BAR_SPACING = 2

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color or (min(color[0]+50, 255), min(color[1]+50, 255), min(color[2]+50, 255))
        self.active = False
        
    def draw(self, screen):
        color = self.hover_color if self.rect.collidepoint(pygame.mouse.get_pos()) else self.color
        if self.active:
            pygame.draw.rect(screen, BLACK, self.rect.inflate(6, 6), border_radius=5)
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Slider:
    def __init__(self, x, y, width, height, min_value, max_value, initial_value, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x, y, 20, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.text = text
        self.dragging = False
        self.update_handle_position()
        
    def update_handle_position(self):
        value_range = self.max_value - self.min_value
        position_range = self.rect.width - self.handle_rect.width
        position = (self.value - self.min_value) / value_range * position_range
        self.handle_rect.x = self.rect.x + position
        
    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, self.handle_rect, border_radius=5)
        text_surface = small_font.render(f"{self.text}: {self.value}", True, BLACK)
        screen.blit(text_surface, (self.rect.x, self.rect.y - 20))
        
    def is_clicked(self, pos):
        return self.handle_rect.collidepoint(pos)
    
    def update_value(self, mouse_x):
        relative_x = max(0, min(mouse_x - self.rect.x, self.rect.width - self.handle_rect.width))
        position_range = self.rect.width - self.handle_rect.width
        value_range = self.max_value - self.min_value
        self.value = self.min_value + (relative_x / position_range) * value_range
        self.value = int(self.value)
        self.handle_rect.x = self.rect.x + relative_x

class MetricsTracker:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.comparisons = 0
        self.swaps = 0
        self.running = False
        
    def start(self):
        self.start_time = time.time()
        self.elapsed_time = 0
        self.comparisons = 0
        self.swaps = 0
        self.running = True
        
    def stop(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
    
    def update(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
    
    def draw(self, screen):
        metrics = [
            f"Time: {self.elapsed_time:.2f}s",
            f"Comparisons: {self.comparisons:,}",
            f"Swaps: {self.swaps:,}"
        ]
        x = WIDTH - 400  
        y = HEIGHT - 35
        #y = 120
        for metric in metrics:
            text = small_font.render(metric, True, BLACK)
            screen.blit(text, (x, y))
            x += 150  

def generate_bars(n=NUM_BARS):
    return random.sample(range(MIN_BAR_HEIGHT, MAX_BAR_HEIGHT), n)

def draw_bars(bars, highlighted=None, sorted_part=-1):
    screen.fill(WHITE)
    title = title_font.render("Sorting Algorithm Visualizer", True, DARK_BLUE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    bar_width = (WIDTH - (len(bars)+1) * BAR_SPACING) // len(bars)
    x_start = BAR_SPACING
    
    for i, height in enumerate(bars):
        color = BAR_COLOR
        if highlighted and i in highlighted:
            color = RED
        elif i > sorted_part and sorted_part != -1:
            color = GREEN
        pygame.draw.rect(screen, color, (x_start, HEIGHT - height - 120, bar_width, height))
        text = small_font.render(str(height), True, BLACK)
        text_rect = text.get_rect(center=(x_start + bar_width//2, HEIGHT - height - 100))
        screen.blit(text, text_rect)
        x_start += bar_width + BAR_SPACING


def bubble_sort(arr, metrics, speed):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            metrics.comparisons += 1
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                metrics.swaps += 1
                yield [j, j+1]
            else:
                yield [j, j+1]
    yield None

def selection_sort(arr, metrics, speed):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            metrics.comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
            yield [i, j, min_idx]
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            metrics.swaps += 1
        yield [i, min_idx]
    yield None

def insertion_sort(arr, metrics, speed):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0:
            metrics.comparisons += 1
            if key < arr[j]:
                arr[j+1] = arr[j]
                metrics.swaps += 1
                j -= 1
            else:
                break
            yield [j+1, j+2]
        arr[j+1] = key
        yield [i, j+1]
    yield None

def quick_sort(arr, metrics, speed):
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            metrics.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                metrics.swaps += 1
                yield [i, j, high]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        metrics.swaps += 1
        yield [i+1]
        return i+1
    
    def qsort(low, high):
        if low < high:
            pi = yield from partition(low, high)
            yield from qsort(low, pi-1)
            yield from qsort(pi+1, high)
    
    yield from qsort(0, len(arr)-1)
    yield None

def merge_sort(arr, metrics, speed):
    def merge(start, mid, end):
        left = arr[start:mid+1]
        right = arr[mid+1:end+1]
        i = j = 0
        k = start
        
        while i < len(left) and j < len(right):
            metrics.comparisons += 1
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
            metrics.swaps += 1
            yield [k-1]
        
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            metrics.swaps += 1
            yield [k-1]
        
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            metrics.swaps += 1
            yield [k-1]
    
    def msort(start, end):
        if start < end:
            mid = (start + end) // 2
            yield from msort(start, mid)
            yield from msort(mid+1, end)
            yield from merge(start, mid, end)
    
    yield from msort(0, len(arr)-1)
    yield None

def main():
    running = True
    clock = pygame.time.Clock()
    bars = generate_bars()
    sorting = False
    sort_generator = None
    current_algorithm = "bubble"
    speed = 50
    metrics = MetricsTracker()
    
    algorithms = {
        "bubble": ("Bubble Sort", ORANGE, bubble_sort),
        "selection": ("Selection Sort", PURPLE, selection_sort),
        "insertion": ("Insertion Sort", DARK_BLUE, insertion_sort),
        "quick": ("Quick Sort", RED, quick_sort),
        "merge": ("Merge Sort", GREEN, merge_sort)
    }
    

    algo_buttons = []
    x_pos = 50
    for algo in algorithms:
        name, color, _ = algorithms[algo]
        algo_buttons.append(Button(x_pos, 70, 150, 40, name, color))
        x_pos += 160
    

    algo_buttons[0].active = True
    

    controls_y = HEIGHT - 80
    start_button = Button(50, controls_y, 100, 40, "Start", GREEN)
    reset_button = Button(170, controls_y, 100, 40, "Reset", DARK_GRAY)
    
 
    speed_slider = Slider(330, controls_y + 10, 150, 20, 1, 100, speed, "Speed")
    bars_slider = Slider(550, controls_y + 10, 150, 20, 10, 100, NUM_BARS, "Bars")
    
    dragging_slider = None

    while running:
        mouse_pos = pygame.mouse.get_pos()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(mouse_pos) and not sorting:
                    sorting = True
                    metrics.start()
                    _, _, algo_func = algorithms[current_algorithm]
                    sort_generator = algo_func(bars, metrics, speed)
                elif reset_button.is_clicked(mouse_pos):
                    bars = generate_bars(int(bars_slider.value))
                    sorting = False
                    sort_generator = None
                    metrics.stop()
                elif speed_slider.is_clicked(mouse_pos):
                    dragging_slider = speed_slider
                elif bars_slider.is_clicked(mouse_pos) and not sorting:
                    dragging_slider = bars_slider
                else:
                    for i, btn in enumerate(algo_buttons):
                        if btn.is_clicked(mouse_pos) and not sorting:
                            current_algorithm = list(algorithms.keys())[i]
                            for button in algo_buttons:
                                button.active = False
                            btn.active = True

            if event.type == pygame.MOUSEBUTTONUP:
                if dragging_slider == bars_slider and not sorting:
                    bars = generate_bars(int(bars_slider.value))
                dragging_slider = None

            if event.type == pygame.MOUSEMOTION and dragging_slider:
                dragging_slider.update_value(event.pos[0])
                if dragging_slider == speed_slider:
                    speed = speed_slider.value

 
        if sorting:
            try:
                highlighted = next(sort_generator)
                if highlighted is None:
                    sorting = False
                    metrics.stop()
                metrics.update()
            except StopIteration:
                sorting = False
                metrics.stop()

     
        draw_bars(bars, highlighted if sorting else None)
        
      
        for btn in algo_buttons:
            btn.draw(screen)
        
       
        pygame.draw.rect(screen, WHITE, (0, HEIGHT-100, WIDTH, 100))
        start_button.draw(screen)
        reset_button.draw(screen)
        speed_slider.draw(screen)
        bars_slider.draw(screen)
        
        
        metrics.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()