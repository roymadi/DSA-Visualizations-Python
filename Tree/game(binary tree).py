import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinaryTreeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Tree Explorer")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.bg_color = "#f0f0f0"
        self.node_color = "#3498db"
        self.highlight_color = "#e74c3c"
        self.line_color = "#2c3e50"
        self.text_color = "#ecf0f1"
        
        self.root.configure(bg=self.bg_color)
        
        self.tree_root = None
        
        self.setup_frames()
        
        self.setup_canvas()
        
        self.setup_controls()
        
        self.current_mode = "explore" 
        self.quiz_answer = None
        self.selected_node = None
        
        self.create_random_tree()

    def setup_frames(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.control_frame = ttk.Frame(self.main_frame, padding="5")
        self.control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.info_frame = ttk.Frame(self.main_frame, padding="5")
        self.info_frame.pack(fill=tk.X, pady=(10, 0))

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.canvas_frame, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.bind("<Configure>", self.draw_tree)
        self.canvas.bind("<Button-1>", self.canvas_click)
        
        self.canvas.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    def setup_controls(self):
        self.style.configure("TButton", padding=6, relief="flat", background="#3498db")
        self.style.map("TButton", background=[("active", "#2980b9")])
        
        mode_frame = ttk.LabelFrame(self.control_frame, text="Mode")
        mode_frame.pack(side=tk.LEFT, padx=5)
        
        self.mode_var = tk.StringVar(value="explore")
        modes = [
            ("Explore", "explore"),
            ("Insert", "insert"),
            ("Delete", "delete"),
            ("Search", "search"),
            ("Quiz", "quiz")
        ]
        
        for text, mode in modes:
            ttk.Radiobutton(mode_frame, text=text, variable=self.mode_var, 
                            value=mode, command=self.change_mode).pack(side=tk.LEFT, padx=5)
        
        value_frame = ttk.Frame(self.control_frame)
        value_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(value_frame, text="Value:").pack(side=tk.LEFT)
        self.value_entry = ttk.Entry(value_frame, width=8)
        self.value_entry.pack(side=tk.LEFT, padx=5)
        
        action_frame = ttk.Frame(self.control_frame)
        action_frame.pack(side=tk.LEFT, padx=5)
        
        self.action_button = ttk.Button(action_frame, text="Execute", command=self.execute_action)
        self.action_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(action_frame, text="Random Tree", command=self.create_random_tree).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Clear Tree", command=self.clear_tree).pack(side=tk.LEFT, padx=5)
        
        zoom_frame = ttk.Frame(self.control_frame)
        zoom_frame.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(zoom_frame, text="Zoom +", command=lambda: self.adjust_zoom(1.2)).pack(side=tk.LEFT, padx=5)
        ttk.Button(zoom_frame, text="Zoom -", command=lambda: self.adjust_zoom(0.8)).pack(side=tk.LEFT, padx=5)
        
        self.info_text = tk.Text(self.info_frame, height=4, wrap=tk.WORD, bg="#ecf0f1", font=("Arial", 10))
        self.info_text.pack(fill=tk.X)
        self.info_text.insert(tk.END, "Welcome to Binary Tree Explorer! Select a mode to start exploring binary trees.")
        self.info_text.config(state=tk.DISABLED)
        
        self.zoom_level = 1.0

    def adjust_zoom(self, factor):
        self.zoom_level *= factor
        self.draw_tree()

    def update_info_text(self, text):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, text)
        self.info_text.config(state=tk.DISABLED)

    def change_mode(self):
        self.current_mode = self.mode_var.get()
        self.selected_node = None
        
        if self.current_mode == "explore":
            self.update_info_text("Explore mode: Click on nodes to see their properties.")
        elif self.current_mode == "insert":
            self.update_info_text("Insert mode: Enter a value and click Execute to add a new node.")
        elif self.current_mode == "delete":
            self.update_info_text("Delete mode: Click on a node to select it for deletion, then click Execute.")
        elif self.current_mode == "search":
            self.update_info_text("Search mode: Enter a value and click Execute to find it in the tree.")
        elif self.current_mode == "quiz":
            self.start_quiz()
        
        self.draw_tree()

    def start_quiz(self):
        if not self.tree_root:
            self.update_info_text("Create a tree first to start the quiz!")
            return
            
        quiz_types = [
            "What is the height of this tree?",
            "How many leaf nodes are in this tree?",
            "Is this a balanced binary tree?",
            "What's the inorder traversal of this tree?"
        ]
        
        quiz_type = random.choice(quiz_types)
        self.update_info_text(f"Quiz: {quiz_type}\nClick Execute when ready to answer.")
        
        if quiz_type == "What is the height of this tree?":
            self.quiz_answer = self.calculate_height(self.tree_root)
        elif quiz_type == "How many leaf nodes are in this tree?":
            self.quiz_answer = self.count_leaf_nodes(self.tree_root)
        elif quiz_type == "Is this a balanced binary tree?":
            self.quiz_answer = self.is_balanced(self.tree_root)
        elif quiz_type == "What's the inorder traversal of this tree?":
            inorder = []
            self.inorder_traversal(self.tree_root, inorder)
            self.quiz_answer = inorder

    def calculate_height(self, node):
        if not node:
            return 0
        return 1 + max(self.calculate_height(node.left), self.calculate_height(node.right))
    
    def count_leaf_nodes(self, node):
        if not node:
            return 0
        if not node.left and not node.right:
            return 1
        return self.count_leaf_nodes(node.left) + self.count_leaf_nodes(node.right)
    
    def is_balanced(self, node):
        if not node:
            return True
        
        left_height = self.calculate_height(node.left)
        right_height = self.calculate_height(node.right)
        
        if abs(left_height - right_height) <= 1 and self.is_balanced(node.left) and self.is_balanced(node.right):
            return True
        return False
    
    def inorder_traversal(self, node, result):
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.value)
            self.inorder_traversal(node.right, result)

    def execute_action(self):
        if self.current_mode == "insert":
            try:
                value = int(self.value_entry.get())
                self.insert_node(value)
                self.update_info_text(f"Inserted node with value {value}")
                self.value_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer")
                
        elif self.current_mode == "delete":
            if self.selected_node:
                self.update_info_text(f"Deleted node with value {self.selected_node}")
                self.delete_node(self.tree_root, self.selected_node)
                self.selected_node = None
                self.draw_tree()
            else:
                messagebox.showinfo("Info", "Please select a node to delete first")
                
        elif self.current_mode == "search":
            try:
                value = int(self.value_entry.get())
                found = self.search_node(self.tree_root, value, [])
                if found:
                    self.update_info_text(f"Found node with value {value}")
                else:
                    self.update_info_text(f"Value {value} not found in the tree")
                self.value_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid integer")
                
        elif self.current_mode == "quiz":
            self.check_quiz_answer()

    def check_quiz_answer(self):
        answer_dialog = tk.Toplevel(self.root)
        answer_dialog.title("Quiz Answer")
        answer_dialog.geometry("300x150")
        
        ttk.Label(answer_dialog, text="Your answer:").pack(pady=(10, 5))
        
        answer_entry = ttk.Entry(answer_dialog, width=20)
        answer_entry.pack(pady=5)
        answer_entry.focus_set()
        
        def submit_answer():
            user_answer = answer_entry.get().strip()
            correct = False
            
            if isinstance(self.quiz_answer, int):
                try:
                    if int(user_answer) == self.quiz_answer:
                        correct = True
                except ValueError:
                    pass
            elif isinstance(self.quiz_answer, bool):
                if user_answer.lower() in ["true", "yes", "1"] and self.quiz_answer:
                    correct = True
                elif user_answer.lower() in ["false", "no", "0"] and not self.quiz_answer:
                    correct = True
            elif isinstance(self.quiz_answer, list):
                try:
                    # Parse the user's answer as a list of integers
                    user_list = [int(x.strip()) for x in user_answer.replace('[', '').replace(']', '').split(',')]
                    if user_list == self.quiz_answer:
                        correct = True
                except:
                    pass
            
            if correct:
                result_text = "Correct! Well done!"
            else:
                result_text = f"Incorrect. The correct answer is {self.quiz_answer}."
            
            result_label = ttk.Label(answer_dialog, text=result_text)
            result_label.pack(pady=10)
            
            submit_button.config(state=tk.DISABLED)
            
            answer_dialog.after(3000, answer_dialog.destroy)
            
            self.start_quiz()
        
        submit_button = ttk.Button(answer_dialog, text="Submit", command=submit_answer)
        submit_button.pack(pady=10)
        
        answer_dialog.bind("<Return>", lambda event: submit_answer())

    def create_random_tree(self):
        self.clear_tree()
        values = random.sample(range(1, 100), min(15, random.randint(7, 15)))
        
        for value in values:
            self.insert_node(value)
            
        self.draw_tree()
        self.update_info_text("Created a new random binary search tree")

    def clear_tree(self):
        self.tree_root = None
        self.draw_tree()
        self.update_info_text("Tree cleared")

    def insert_node(self, value):
        if not self.tree_root:
            self.tree_root = TreeNode(value)
        else:
            self._insert_recursive(self.tree_root, value)
        
        self.draw_tree()
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = TreeNode(value)
            else:
                self._insert_recursive(node.right, value)

    def delete_node(self, root, value):
        if not root:
            return None
            
        if value < root.value:
            root.left = self.delete_node(root.left, value)
        elif value > root.value:
            root.right = self.delete_node(root.right, value)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left
               
            root.value = self.min_value_node(root.right).value
            
            root.right = self.delete_node(root.right, root.value)
            
        return root
    
    def min_value_node(self, node):
        current = node
        
        while current.left:
            current = current.left
            
        return current

    def search_node(self, node, value, path=None):
        if path is None:
            path = []
            
        if not node:
            return False
            
        path.append(node.value)
        
        if node.value == value:
            self.draw_tree(search_path=path, highlight_value=value)
            return True
        
        if value < node.value:
            return self.search_node(node.left, value, path)
        else:
            return self.search_node(node.right, value, path)
            
    def count_nodes(self, node):
        if not node:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    def draw_tree(self, event=None, search_path=None, highlight_value=None):
        self.canvas.delete("all")
        
        if not self.tree_root:
            return
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        tree_height = self.calculate_height(self.tree_root)
        node_count = self.count_nodes(self.tree_root)
        
        vertical_spacing = 80 * self.zoom_level
        
        canvas_height = (tree_height + 1) * vertical_spacing + 100
        self.canvas.configure(scrollregion=(0, 0, width, max(canvas_height, height)))
        
        node_positions = {}
        
        def calculate_positions(node, level, horizontal_position=None):
            if not node:
                return
            
            if horizontal_position is None:
                horizontal_position = 0
            
            if level not in node_positions:
                node_positions[level] = []
            
            node_positions[level].append((node, horizontal_position))
            
            offset = max(2 ** (tree_height - level - 1), 1) * 10 * self.zoom_level
            
            calculate_positions(node.left, level + 1, horizontal_position - offset)
            calculate_positions(node.right, level + 1, horizontal_position + offset)
        
        calculate_positions(self.tree_root, 0)
        
        min_x_spacing = 10 * self.zoom_level 
        
        for level in sorted(node_positions.keys()):
            node_positions[level].sort(key=lambda x: x[1])
            
            for i in range(1, len(node_positions[level])):
                prev_node, prev_pos = node_positions[level][i-1]
                curr_node, curr_pos = node_positions[level][i]
                
                if curr_pos - prev_pos < min_x_spacing:
                    shift = min_x_spacing - (curr_pos - prev_pos)
                    node_positions[level][i] = (curr_node, curr_pos + shift)
                    
                    def shift_subtree(node, shift_amount, level):
                        for l in range(level + 1, max(node_positions.keys()) + 1):
                            for j, (n, pos) in enumerate(node_positions[l]):
                                if self.is_descendant(curr_node, n):
                                    node_positions[l][j] = (n, pos + shift_amount)
                    
                    shift_subtree(curr_node, shift, level)
        
        all_positions = [pos for level in node_positions.values() for _, pos in level]
        min_pos = min(all_positions)
        max_pos = max(all_positions)
        center_offset = (min_pos + max_pos) / 2
        
        for level in node_positions:
            for node, pos in node_positions[level]:
                x = width/2 + (pos - center_offset)
                y = 50 + level * vertical_spacing
                
                if node.left:
                    child_level = level + 1
                    child_pos = next(pos for n, pos in node_positions[child_level] if n == node.left)
                    child_x = width/2 + (child_pos - center_offset)
                    child_y = 50 + child_level * vertical_spacing
                    self.canvas.create_line(x, y, child_x, child_y, fill=self.line_color, width=2)
                
                if node.right:
                    child_level = level + 1
                    child_pos = next(pos for n, pos in node_positions[child_level] if n == node.right)
                    child_x = width/2 + (child_pos - center_offset)
                    child_y = 50 + child_level * vertical_spacing
                    self.canvas.create_line(x, y, child_x, child_y, fill=self.line_color, width=2)
        
        for level in node_positions:
            for node, pos in node_positions[level]:
                x = width/2 + (pos - center_offset)
                y = 50 + level * vertical_spacing
                
                node_radius = 20 * self.zoom_level
                
                node_color = self.node_color
                
                if search_path and node.value in search_path:
                    node_color = "#f39c12"  
                
                if (highlight_value and node.value == highlight_value) or (self.selected_node and node.value == self.selected_node):
                    node_color = self.highlight_color
                
                self.canvas.create_oval(
                    x-node_radius, y-node_radius, 
                    x+node_radius, y+node_radius, 
                    fill=node_color, outline=self.line_color, width=2
                )
                
                font_size = max(int(12 * self.zoom_level), 8)
                self.canvas.create_text(x, y, text=str(node.value), fill=self.text_color, font=("Arial", font_size, "bold"))
    
    def is_descendant(self, ancestor, node):
        if ancestor == node:
            return True
            
        if not ancestor:
            return False
            
        return self.is_descendant(ancestor.left, node) or self.is_descendant(ancestor.right, node)

    def canvas_click(self, event):
        if not self.tree_root:
            return
            
        x, y = event.x, event.y
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        tree_height = self.calculate_height(self.tree_root)
        
        vertical_spacing = 80 * self.zoom_level
        node_radius = 20 * self.zoom_level
        
        canvas_x = self.canvas.canvasx(x)
        canvas_y = self.canvas.canvasy(y)
        
        node_positions = {}
        
        def calculate_positions(node, level, horizontal_position=None):
            if not node:
                return
            
            if horizontal_position is None:
                horizontal_position = 0
            
            if level not in node_positions:
                node_positions[level] = []
            
            node_positions[level].append((node, horizontal_position))
            
            offset = max(2 ** (tree_height - level - 1), 1) * 10 * self.zoom_level
            
            calculate_positions(node.left, level + 1, horizontal_position - offset)
            calculate_positions(node.right, level + 1, horizontal_position + offset)
        
        calculate_positions(self.tree_root, 0)
        
        min_x_spacing = 10 * self.zoom_level  
        
        for level in sorted(node_positions.keys()):
            node_positions[level].sort(key=lambda x: x[1])
            
            for i in range(1, len(node_positions[level])):
                prev_node, prev_pos = node_positions[level][i-1]
                curr_node, curr_pos = node_positions[level][i]
                
                if curr_pos - prev_pos < min_x_spacing:
                    shift = min_x_spacing - (curr_pos - prev_pos)
                    node_positions[level][i] = (curr_node, curr_pos + shift)
                    
                    def shift_subtree(node, shift_amount, level):
                        for l in range(level + 1, max(node_positions.keys()) + 1):
                            for j, (n, pos) in enumerate(node_positions[l]):
                                if self.is_descendant(curr_node, n):
                                    node_positions[l][j] = (n, pos + shift_amount)
                    
                    shift_subtree(curr_node, shift, level)
        
        all_positions = [pos for level in node_positions.values() for _, pos in level]
        min_pos = min(all_positions)
        max_pos = max(all_positions)
        center_offset = (min_pos + max_pos) / 2
        
        clicked_node = None
        
        for level in node_positions:
            for node, pos in node_positions[level]:
                node_x = width/2 + (pos - center_offset)
                node_y = 50 + level * vertical_spacing
             
                if (abs(canvas_x - node_x) <= node_radius and 
                    abs(canvas_y - node_y) <= node_radius):
                    clicked_node = node
                    break
            if clicked_node:
                break
        
        if clicked_node:
            if self.current_mode == "explore":
                node_info = self.get_node_info(self.tree_root, clicked_node.value)
                self.update_info_text(node_info)
            elif self.current_mode == "delete":
                self.selected_node = clicked_node.value
                self.update_info_text(f"Selected node {clicked_node.value} for deletion. Click Execute to confirm.")
                self.draw_tree()

    def get_node_info(self, root, value):
        # Find the node
        node = self.find_node(root, value)
        
        if not node:
            return f"Node {value} not found."
            
        height = self.calculate_node_height(root, value)
        depth = self.calculate_node_depth(root, value)
        
        info = f"Node: {value}\n"
        info += f"Height: {height}\n"
        info += f"Depth: {depth}\n"
        
        if node.left:
            info += f"Left child: {node.left.value}\n"
        else:
            info += "Left child: None\n"
            
        if node.right:
            info += f"Right child: {node.right.value}\n"
        else:
            info += "Right child: None\n"
            
        parent = self.find_parent(root, value)
        if parent:
            info += f"Parent: {parent.value}"
        else:
            info += "Parent: None (Root node)"
            
        return info
    
    def find_node(self, node, value):
        if not node:
            return None
            
        if node.value == value:
            return node
            
        if value < node.value:
            return self.find_node(node.left, value)
        else:
            return self.find_node(node.right, value)
    
    def find_parent(self, node, value, parent=None):
        if not node:
            return None
            
        if node.value == value:
            return parent
            
        if value < node.value:
            return self.find_parent(node.left, value, node)
        else:
            return self.find_parent(node.right, value, node)
    
    def calculate_node_height(self, node, value):
        target = self.find_node(node, value)
        if not target:
            return -1
        return self.calculate_height(target) - 1 
    
    def calculate_node_depth(self, node, value, current_depth=0):
        if not node:
            return -1
            
        if node.value == value:
            return current_depth
            
        if value < node.value:
            return self.calculate_node_depth(node.left, value, current_depth + 1)
        else:
            return self.calculate_node_depth(node.right, value, current_depth + 1)

def main():
    root = tk.Tk()
    app = BinaryTreeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()