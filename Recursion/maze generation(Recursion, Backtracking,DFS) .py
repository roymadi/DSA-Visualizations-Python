import tkinter as tk
from tkinter import ttk
import random
import time

class MazeGenerator:
    def __init__(self, rows, cols, cell_size=30):
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.grid = [[Cell(row, col) for col in range(cols)] for row in range(rows)]
        self.current = self.grid[0][0]
        self.stack = []
        
      
        self.root = tk.Tk()
        self.root.title("Maze Generator - Recursive Backtracking")
        self.root.configure(bg='#2d2d2d')
        
        self.canvas = tk.Canvas(self.root, 
                              width=cols*cell_size, 
                              height=rows*cell_size,
                              bg='#1a1a1a',
                              highlightthickness=0)
        self.canvas.pack(pady=20, padx=20)
        
        self.btn_frame = ttk.Frame(self.root)
        self.btn_frame.pack(pady=10)
        
        self.generate_btn = ttk.Button(self.btn_frame, 
                                      text="Generate New Maze", 
                                      command=self.generate_new_maze)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        self.solve_btn = ttk.Button(self.btn_frame, 
                                   text="Solve Maze", 
                                   command=self.solve_maze,
                                   state=tk.DISABLED)
        self.solve_btn.pack(side=tk.LEFT, padx=5)
        
        self.draw_grid()
        
    def generate_new_maze(self):
        self.reset_grid()
        self.generate_maze()
        self.solve_btn['state'] = tk.NORMAL
        
    def reset_grid(self):
        self.grid = [[Cell(row, col) for col in range(self.cols)] for row in range(self.rows)]
        self.current = self.grid[0][0]
        self.stack = []
        self.draw_grid()
        
    def draw_grid(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = row * self.cell_size
                
                if self.grid[row][col].walls['top']:
                    self.canvas.create_line(x, y, x + self.cell_size, y, fill='#ffffff', width=2)
                if self.grid[row][col].walls['right']:
                    self.canvas.create_line(x + self.cell_size, y, x + self.cell_size, y + self.cell_size, fill='#ffffff', width=2)
                if self.grid[row][col].walls['bottom']:
                    self.canvas.create_line(x, y + self.cell_size, x + self.cell_size, y + self.cell_size, fill='#ffffff', width=2)
                if self.grid[row][col].walls['left']:
                    self.canvas.create_line(x, y, x, y + self.cell_size, fill='#ffffff', width=2)
                
         
                if self.grid[row][col] == self.current:
                    self.canvas.create_rectangle(x+2, y+2, x+self.cell_size-2, y+self.cell_size-2, 
                                               fill='#ff4444', outline='')
        
    def get_neighbors(self, cell):
        neighbors = []
        directions = {
            'top': (cell.row-1, cell.col),
            'right': (cell.row, cell.col+1),
            'bottom': (cell.row+1, cell.col),
            'left': (cell.row, cell.col-1)
        }
        
        for direction, (row, col) in directions.items():
            if 0 <= row < self.rows and 0 <= col < self.cols:
                neighbor = self.grid[row][col]
                if not neighbor.visited:
                    neighbors.append((direction, neighbor))
        
        return neighbors
    
    def remove_walls(self, current, neighbor, direction):
        current.walls[direction] = False
        opposite = {'top': 'bottom', 'right': 'left', 'bottom': 'top', 'left': 'right'}[direction]
        neighbor.walls[opposite] = False
        
    def generate_maze(self):
        self.current.visited = True
        neighbors = self.get_neighbors(self.current)
        
        if neighbors:
            direction, next_cell = random.choice(neighbors)
            self.stack.append(self.current)
            self.remove_walls(self.current, next_cell, direction)
            self.current = next_cell
            self.draw_grid()
            self.root.after(10, self.generate_maze)
        elif self.stack:
            self.current = self.stack.pop()
            self.draw_grid()
            self.root.after(10, self.generate_maze)
            
    def solve_maze(self):
        start = self.grid[0][0]
        end = self.grid[self.rows-1][self.cols-1]
        stack = [start]
        came_from = {}
        
        while stack:
            current = stack.pop()
            if current == end:
                break
                

            neighbors = []
            directions = {
                'top': (current.row-1, current.col),
                'right': (current.row, current.col+1),
                'bottom': (current.row+1, current.col),
                'left': (current.row, current.col-1)
            }
            
            for direction, (row, col) in directions.items():
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    neighbor = self.grid[row][col]
                    if not current.walls[direction] and neighbor not in came_from:
                        neighbors.append(neighbor)
                        came_from[neighbor] = current
            
            for neighbor in neighbors:
                stack.append(neighbor)
        
  
        path = []
        current = end
        while current != start:
            path.append(current)
            current = came_from.get(current, start)
        path.append(start)
        path.reverse()
        

        for cell in path:
            x = cell.col * self.cell_size + self.cell_size//2
            y = cell.row * self.cell_size + self.cell_size//2
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='#4444ff', outline='')
            self.root.update()
            time.sleep(0.01)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col)) 

if __name__ == "__main__":
    maze = MazeGenerator(20, 20, cell_size=25)
    maze.root.mainloop()