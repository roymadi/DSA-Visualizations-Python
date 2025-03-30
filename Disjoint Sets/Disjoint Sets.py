import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.component_count = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in the same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            self.size[root_x] += self.size[root_y]
        
        self.component_count -= 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
    
    def component_size(self, x):
        return self.size[self.find(x)]
    
    def get_component_count(self):
        return self.component_count


class ConnectedComponentsGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Connected Components Game")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        self.grid_size = 6  
        self.node_radius = 20
        self.nodes = []
        self.edges = []
        self.selected_nodes = []
        self.disjoint_set = None
        self.target_components = 1
        self.moves = 0
        self.game_active = False
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 12))
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("TFrame", background="#f0f0f0")
        
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(self.top_frame, text="Grid Size:").pack(side=tk.LEFT, padx=5)
        self.grid_size_var = tk.StringVar(value="6")
        grid_sizes = ["4", "5", "6", "7", "8"]
        self.grid_combo = ttk.Combobox(self.top_frame, textvariable=self.grid_size_var, 
                                       values=grid_sizes, width=5, state="readonly")
        self.grid_combo.pack(side=tk.LEFT, padx=5)
        self.grid_combo.bind("<<ComboboxSelected>>", self.update_grid_size)
        
        self.new_game_btn = ttk.Button(self.top_frame, text="New Game", command=self.new_game)
        self.new_game_btn.pack(side=tk.LEFT, padx=20)
        
        self.info_frame = ttk.Frame(self.top_frame)
        self.info_frame.pack(side=tk.RIGHT)
        
        self.moves_label = ttk.Label(self.info_frame, text="Moves: 0")
        self.moves_label.pack(side=tk.RIGHT, padx=10)
        
        self.components_label = ttk.Label(self.info_frame, text="Components: 0")
        self.components_label.pack(side=tk.RIGHT, padx=10)
        
        self.target_label = ttk.Label(self.info_frame, text="Target: 0")
        self.target_label.pack(side=tk.RIGHT, padx=10)
        
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, background="#ffffff", 
                               highlightthickness=1, highlightbackground="#cccccc")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        self.instruction_frame = ttk.Frame(self.main_frame)
        self.instruction_frame.pack(fill=tk.X, pady=10)
        
        instructions = """
        Instructions:
        1. Click on two nodes to connect them
        2. Try to reach the target number of connected components with minimal moves
        3. Blue nodes are in the same component, differently colored nodes are in different components
        """
        self.instruction_label = ttk.Label(self.instruction_frame, text=instructions)
        self.instruction_label.pack(pady=5)
        
        self.new_game()
    
    def update_grid_size(self, event=None):
        self.grid_size = int(self.grid_size_var.get())
        self.new_game()
    
    def new_game(self):
        self.nodes = []
        self.edges = []
        self.selected_nodes = []
        self.moves = 0
        self.moves_label.config(text=f"Moves: {self.moves}")
        
        node_count = self.grid_size * self.grid_size
        self.disjoint_set = DisjointSet(node_count)
        
        self.target_components = random.randint(1, max(1, node_count // 4))
        self.target_label.config(text=f"Target: {self.target_components}")
        self.components_label.config(text=f"Components: {self.disjoint_set.get_component_count()}")
        
        self.canvas.delete("all")
        self.create_grid()
        self.draw_nodes()
        self.game_active = True
    
    def create_grid(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 600
        if canvas_height <= 1:
            canvas_height = 400
        
        horizontal_spacing = canvas_width / (self.grid_size + 1)
        vertical_spacing = canvas_height / (self.grid_size + 1)
        
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                node_id = row * self.grid_size + col
                x = (col + 1) * horizontal_spacing
                y = (row + 1) * vertical_spacing
                self.nodes.append((x, y, node_id))
    
    def draw_nodes(self):
        self.canvas.delete("node")
        self.canvas.delete("edge")
        self.canvas.delete("text")
        
        for edge in self.edges:
            node1 = self.nodes[edge[0]]
            node2 = self.nodes[edge[1]]
            self.canvas.create_line(node1[0], node1[1], node2[0], node2[1], 
                                   width=3, fill="#555555", tags="edge")
        
        root_to_color = {}
        colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", 
                 "#1abc9c", "#d35400", "#34495e", "#27ae60", "#e67e22"]
        
        for x, y, node_id in self.nodes:
            root = self.disjoint_set.find(node_id)
            if root not in root_to_color:
                root_to_color[root] = colors[len(root_to_color) % len(colors)]
            
            color = root_to_color[root]
            
            if node_id in self.selected_nodes:
                border_color = "#ff0000"
                border_width = 3
            else:
                border_color = "#000000"
                border_width = 1
            
            self.canvas.create_oval(x - self.node_radius, y - self.node_radius,
                                  x + self.node_radius, y + self.node_radius,
                                  fill=color, outline=border_color, width=border_width,
                                  tags=("node", f"node-{node_id}"))
            
            self.canvas.create_text(x, y, text=str(node_id), fill="white", font=("Helvetica", 10, "bold"),
                                  tags=("text", f"text-{node_id}"))
    
    def on_canvas_click(self, event):
        if not self.game_active:
            return
        
        x, y = event.x, event.y
        for node_x, node_y, node_id in self.nodes:
            distance = math.sqrt((x - node_x) ** 2 + (y - node_y) ** 2)
            if distance <= self.node_radius:
                self.select_node(node_id)
                break
    
    def select_node(self, node_id):
        if node_id in self.selected_nodes:
            self.selected_nodes.remove(node_id)
        else:
            self.selected_nodes.append(node_id)
        
        if len(self.selected_nodes) == 2:
            self.connect_nodes(self.selected_nodes[0], self.selected_nodes[1])
            self.selected_nodes = []
        
        self.draw_nodes()
    
    def connect_nodes(self, node1, node2):
        if self.disjoint_set.connected(node1, node2):
            messagebox.showinfo("Info", "These nodes are already connected!")
            return
        
        self.edges.append((node1, node2))
        self.disjoint_set.union(node1, node2)
        
        self.moves += 1
        self.moves_label.config(text=f"Moves: {self.moves}")
        self.components_label.config(text=f"Components: {self.disjoint_set.get_component_count()}")
        
        if self.disjoint_set.get_component_count() == self.target_components:
            self.game_active = False
            messagebox.showinfo("Congratulations", 
                               f"You reached the target of {self.target_components} components in {self.moves} moves!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectedComponentsGame(root)
    root.mainloop()