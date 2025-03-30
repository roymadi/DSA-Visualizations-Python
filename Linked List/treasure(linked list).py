import tkinter as tk
from tkinter import messagebox, PhotoImage
import random
from PIL import Image, ImageTk
import os

class ClueNode:
    def __init__(self, location, clue_text, is_treasure=False):
        self.location = location
        self.clue_text = clue_text
        self.next = None
        self.is_treasure = is_treasure

class TreasureHunt:
    def __init__(self):
        self.head = None
        self.current = None
        self.steps = 0
    
    def add_clue(self, location, clue_text, is_treasure=False):
        new_node = ClueNode(location, clue_text, is_treasure)
        
        if not self.head:
            self.head = new_node
            return
            
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
    
    def start_hunt(self):
        self.current = self.head
        self.steps = 0
        return self.current
    
    def next_clue(self):
        if self.current and self.current.next:
            self.current = self.current.next
            self.steps += 1
            return self.current
        return None
    
    def is_at_treasure(self):
        return self.current and self.current.is_treasure
    
    def get_current_location(self):
        return self.current.location if self.current else None
    
    def get_current_clue(self):
        return self.current.clue_text if self.current else None
    
    def get_steps_taken(self):
        """Get total steps taken so far"""
        return self.steps

class TreasureHuntApp:
    
    LOCATIONS = [
        "Ancient Library", "Hidden Cave", "Old Lighthouse", 
        "Mysterious Forest", "Abandoned Mansion", "Secret Garden",
        "Forgotten Well", "Haunted Graveyard", "Crystal Lake",
        "Mountain Peak", "Desert Oasis", "Sunken Ship"
    ]
    
    CLUE_TEMPLATES = [
        "The next clue is hidden where the sun casts no shadow. Head to the {}.",
        "Look for the next clue where whispers echo. Make your way to the {}.",
        "Your journey continues where water meets sky. Proceed to the {}.",
        "The path forward is revealed in the ancient texts. Go to the {}.",
        "Seek wisdom where the old spirits dwell. Travel to the {}.",
        "The stars guide your next step. They point to the {}.",
        "A guardian of secrets holds your next clue. Find them at the {}."
    ]
    
    def __init__(self, root):
        self.root = root
        self.root.title("Treasure Hunt Adventure")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.bg_color = "#2c3e50"
        self.text_color = "#ecf0f1"
        self.accent_color = "#e74c3c"
        self.button_color = "#3498db"
        self.root.configure(bg=self.bg_color)
        
        self.font_title = ("Helvetica", 24, "bold")
        self.font_normal = ("Helvetica", 12)
        self.font_clue = ("Helvetica", 14, "italic")
        
        self.hunt = None
        self.game_active = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header frame
        self.header_frame = tk.Frame(self.root, bg=self.bg_color)
        self.header_frame.pack(pady=20, fill=tk.X)
        
        self.title_label = tk.Label(
            self.header_frame, 
            text="Treasure Hunt Adventure", 
            font=self.font_title,
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.pack()
        
        self.content_frame = tk.Frame(self.root, bg=self.bg_color)
        self.content_frame.pack(pady=10, expand=True, fill=tk.BOTH)
        
        self.location_label = tk.Label(
            self.content_frame,
            text="Current Location: None",
            font=self.font_normal,
            bg=self.bg_color,
            fg=self.text_color
        )
        self.location_label.pack(pady=10)
        
        self.clue_frame = tk.Frame(
            self.content_frame,
            bg="#34495e",
            width=600,
            height=200,
            padx=20,
            pady=20
        )
        self.clue_frame.pack(pady=20)
        self.clue_frame.pack_propagate(False)
        
        self.clue_label = tk.Label(
            self.clue_frame,
            text="Press 'Start New Hunt' to begin your adventure!",
            font=self.font_clue,
            bg="#34495e",
            fg=self.text_color,
            wraplength=550,
            justify=tk.CENTER
        )
        self.clue_label.pack(expand=True)
        
        self.steps_label = tk.Label(
            self.content_frame,
            text="Steps taken: 0",
            font=self.font_normal,
            bg=self.bg_color,
            fg=self.text_color
        )
        self.steps_label.pack(pady=10)
        
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=20)
        
        self.start_button = tk.Button(
            self.button_frame,
            text="Start New Hunt",
            font=self.font_normal,
            bg=self.button_color,
            fg=self.text_color,
            padx=20,
            pady=10,
            command=self.start_new_hunt
        )
        self.start_button.grid(row=0, column=0, padx=10)
        
        self.next_button = tk.Button(
            self.button_frame,
            text="Follow This Clue",
            font=self.font_normal,
            bg=self.button_color,
            fg=self.text_color,
            padx=20,
            pady=10,
            command=self.follow_clue,
            state=tk.DISABLED
        )
        self.next_button.grid(row=0, column=1, padx=10)
        
        self.footer = tk.Label(
            self.root,
            text="Follow the clues to find the hidden treasure!",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.footer.pack(side=tk.BOTTOM, pady=10)
        
    def start_new_hunt(self):
        self.hunt = TreasureHunt()
        
        path_length = random.randint(5, 8)
        selected_locations = random.sample(self.LOCATIONS, path_length)
        
        for i in range(path_length - 1):
            location = selected_locations[i]
            next_location = selected_locations[i + 1]
            clue_template = random.choice(self.CLUE_TEMPLATES)
            clue_text = clue_template.format(next_location)
            self.hunt.add_clue(location, clue_text)
        
        final_location = selected_locations[-1]
        self.hunt.add_clue(
            final_location,
            "Congratulations! You've found the hidden treasure!",
            is_treasure=True
        )
        
        self.game_active = True
        first_node = self.hunt.start_hunt()
        
        self.location_label.config(text=f"Current Location: {first_node.location}")
        self.clue_label.config(text=first_node.clue_text)
        self.steps_label.config(text=f"Steps taken: {self.hunt.get_steps_taken()}")
        self.next_button.config(state=tk.NORMAL)
        
    def follow_clue(self):
        if not self.game_active:
            return
            
        next_node = self.hunt.next_clue()
        
        if next_node:
            self.location_label.config(text=f"Current Location: {next_node.location}")
            self.clue_label.config(text=next_node.clue_text)
            self.steps_label.config(text=f"Steps taken: {self.hunt.get_steps_taken()}")
            
            if self.hunt.is_at_treasure():
                self.game_complete()
        else:
            messagebox.showinfo("End of Path", "There are no more clues to follow.")
            
    def game_complete(self):
        steps = self.hunt.get_steps_taken()
        messagebox.showinfo(
            "Treasure Found!",
            f"Congratulations! You've found the treasure in {steps} steps!"
        )
        self.next_button.config(state=tk.DISABLED)
        self.game_active = False

if __name__ == "__main__":
    root = tk.Tk()
    app = TreasureHuntApp(root)
    root.mainloop()