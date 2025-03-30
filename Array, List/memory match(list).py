import tkinter as tk
from tkinter import Frame, Label, Button
import random
import time

class ImprovedMemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Memory Matching Game")
        self.root.geometry("600x700")
        self.root.configure(bg="#2C3E50")

        self.rows = 4
        self.cols = 4
        self.timer_running = False
        self.time_elapsed = 0
        self.moves = 0
        self.score = 0
        
        self.symbols = ["♠", "♥", "♦", "♣", "★", "✿", "❋", "♫"] * 2
        self.colors = {
            "♠": "#34495E", "♥": "#E74C3C", "♦": "#3498DB", 
            "♣": "#2ECC71", "★": "#F1C40F", "✿": "#9B59B6", 
            "❋": "#1ABC9C", "♫": "#E67E22"
        }
        random.shuffle(self.symbols)
        
        self.buttons = []    
        self.flipped = []     
        self.matched_pairs = [] 
        self.matches = 0     
        
        self.create_header()
        self.create_grid()
        self.create_footer()
        
        self.start_timer()
    
    def create_header(self):
        header_frame = Frame(self.root, bg="#34495E", pady=10)
        header_frame.pack(fill="x")
        
        title_label = Label(header_frame, text="MEMORY MATCH", font=("Arial", 24, "bold"), 
                           bg="#34495E", fg="#ECF0F1")
        title_label.pack()
        
        self.stats_frame = Frame(self.root, bg="#2C3E50", pady=10)
        self.stats_frame.pack(fill="x")
        
        self.timer_label = Label(self.stats_frame, text="Time: 0s", font=("Arial", 14),
                               bg="#2C3E50", fg="#ECF0F1", width=10)
        self.timer_label.pack(side="left", padx=20)
        
        self.moves_label = Label(self.stats_frame, text="Moves: 0", font=("Arial", 14),
                               bg="#2C3E50", fg="#ECF0F1", width=10)
        self.moves_label.pack(side="left", padx=20)
        
        self.score_label = Label(self.stats_frame, text="Score: 0", font=("Arial", 14),
                               bg="#2C3E50", fg="#ECF0F1", width=10)
        self.score_label.pack(side="left", padx=20)
        
        self.new_game_button = Button(self.stats_frame, text="New Game", font=("Arial", 12, "bold"),
                                bg="#3498DB", fg="#ECF0F1", bd=0, relief="raised",
                                command=self.reset_game)
        self.new_game_button.pack(side="left", padx=20)
    
    def create_grid(self):
        self.grid_frame = Frame(self.root, bg="#2C3E50", padx=20, pady=20)
        self.grid_frame.pack()
        
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                card_frame = Frame(self.grid_frame, bg="#7F8C8D", 
                                 width=100, height=100, padx=2, pady=2)
                card_frame.grid(row=i, column=j, padx=8, pady=8)
                card_frame.grid_propagate(False)  # Keep frame size fixed
                
                button = Button(
                    card_frame,
                    text="",
                    font=("Arial", 24, "bold"),
                    width=4,
                    height=2,
                    bg="#7F8C8D",
                    activebackground="#95A5A6",
                    bd=0,
                    relief="raised",
                    command=lambda i=i, j=j: self.flip_card(i, j),
                )
                button.pack(fill="both", expand=True)
                row.append(button)
            self.buttons.append(row)
    
    def create_footer(self):
        footer_frame = Frame(self.root, bg="#34495E", pady=10)
        footer_frame.pack(fill="x", side="bottom")
        
        footer_text = Label(footer_frame, text="Match all pairs to win!", 
                          font=("Arial", 12, "italic"), bg="#34495E", fg="#ECF0F1")
        footer_text.pack()
    
    def flip_card(self, i, j):
        button = self.buttons[i][j]
        card_idx = i * self.cols + j
        
        if button["text"] == "" and len(self.flipped) < 2 and (i, j) not in self.matched_pairs:
            symbol = self.symbols[card_idx]
            button["text"] = symbol
            button["bg"] = self.colors[symbol]
            button["fg"] = "white"
            
            self.flipped.append((i, j))
            
            if len(self.flipped) == 2:
                self.moves += 1
                self.moves_label.config(text=f"Moves: {self.moves}")
                
                self.root.after(500, self.check_match)
    
    def check_match(self):
        (i1, j1), (i2, j2) = self.flipped
        idx1, idx2 = i1 * self.cols + j1, i2 * self.cols + j2
        
        if self.symbols[idx1] == self.symbols[idx2]:
            self.matches += 1
            self.matched_pairs.extend([(i1, j1), (i2, j2)])
            
         
            bonus = 500
            time_factor = max(0.5, 1 - (self.time_elapsed / 100))
            points = int(bonus * time_factor)
            self.score += points
            self.score_label.config(text=f"Score: {self.score}")
            
            for _ in range(3):
                for (i, j) in self.flipped:
                    self.buttons[i][j]["bg"] = "#2ECC71"  # Green flash
                self.root.update()
                time.sleep(0.1)
                for (i, j) in self.flipped:
                    self.buttons[i][j]["bg"] = self.colors[self.symbols[i * self.cols + j]]
                self.root.update()
                time.sleep(0.1)
            
            if self.matches == (self.rows * self.cols) // 2:
                self.timer_running = False
                self.show_win_message()
        else:
            for (i, j) in self.flipped:
                self.buttons[i][j]["text"] = ""
                self.buttons[i][j]["bg"] = "#7F8C8D"
        
        self.flipped = []
    
    def show_win_message(self):
        """Show win message with a "Start Game" option."""
        message = (f"Congratulations! You won!\n\n"
                  f"Time: {self.time_elapsed} seconds\n"
                  f"Moves: {self.moves}\n"
                  f"Score: {self.score}\n\n"
                  f"Click 'Start Game' to play again.")
        
        self.win_label = Label(self.root, text=message, font=("Arial", 14), bg="#2C3E50", fg="#ECF0F1")
        self.win_label.place(relx=0.5, rely=0.5, anchor="center")
        
        self.start_game_button = Button(self.root, text="Start Game", font=("Arial", 12, "bold"),
                                bg="#3498DB", fg="#ECF0F1", bd=0, relief="raised",
                                command=self.reset_game)
        self.start_game_button.place(relx=0.5, rely=0.65, anchor="center")
    
    def start_timer(self):
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if self.timer_running:
            self.time_elapsed += 1
            self.timer_label.config(text=f"Time: {self.time_elapsed}s")
            self.root.after(1000, self.update_timer)
    
    def reset_game(self):
        # Stop the timer
        self.timer_running = False
        
        self.time_elapsed = 0
        self.moves = 0
        self.score = 0
        self.matches = 0
        self.flipped = []
        self.matched_pairs = []
        
        random.shuffle(self.symbols)
        
        self.timer_label.config(text="Time: 0s")
        self.moves_label.config(text="Moves: 0")
        self.score_label.config(text="Score: 0")
        
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j]["text"] = ""
                self.buttons[i][j]["bg"] = "#7F8C8D"
        
        if hasattr(self, "win_label"):
            self.win_label.destroy()
        if hasattr(self, "start_game_button"):
            self.start_game_button.destroy()
        
        self.start_timer()

if __name__ == "__main__":
    root = tk.Tk()
    game = ImprovedMemoryGame(root)
    root.mainloop()