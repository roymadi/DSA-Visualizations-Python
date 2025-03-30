import tkinter as tk
from tkinter import messagebox
import random
from customtkinter import CTk, CTkButton, CTkLabel, CTkEntry, CTkFrame, CTkCanvas

class FenwickTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (self.n + 2)

    def update(self, idx, delta):
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx

    def query(self, idx):
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & -idx
        return res

    def range_query(self, l, r):
        return self.query(r) - self.query(l - 1)

class FenwickForestGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Fenwick Forest")
        self.root.geometry("900x700")

        self.n = 10  # Number of forest sections
        self.ft = FenwickTree(self.n)

        self.create_widgets()
        self.update_visualization()

    def create_widgets(self):
        self.frame = CTkFrame(self.root, fg_color="#2E3440")
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.label = CTkLabel(self.frame, text="Fenwick Forest", font=("Arial", 28, "bold"), text_color="#ECEFF4")
        self.label.grid(row=0, column=0, columnspan=3, pady=20)

        self.canvas = CTkCanvas(self.frame, width=1100, height=400, bg="#3B4252", highlightthickness=0)
        self.canvas.grid(row=1, column=0, columnspan=5, pady=20)

        self.section_label = CTkLabel(self.frame, text="Section (1-10):", font=("Arial", 14), text_color="#ECEFF4")
        self.section_label.grid(row=2, column=0, pady=10)

        self.section_entry = CTkEntry(self.frame, width=100, font=("Arial", 14))
        self.section_entry.grid(row=2, column=1, pady=10)

        self.trees_label = CTkLabel(self.frame, text="Number of Trees:", font=("Arial", 14), text_color="#ECEFF4")
        self.trees_label.grid(row=3, column=0, pady=10)

        self.trees_entry = CTkEntry(self.frame, width=100, font=("Arial", 14))
        self.trees_entry.grid(row=3, column=1, pady=10)

        self.plant_button = CTkButton(self.frame, text="Plant Trees", command=self.plant_trees, font=("Arial", 14), fg_color="#5E81AC", hover_color="#81A1C1")
        self.plant_button.grid(row=4, column=0, pady=10)

        self.cut_button = CTkButton(self.frame, text="Cut Trees", command=self.cut_trees, font=("Arial", 14), fg_color="#BF616A", hover_color="#D08770")
        self.cut_button.grid(row=4, column=1, pady=10)

        self.query_label = CTkLabel(self.frame, text="Query Range (e.g., 1-5):", font=("Arial", 14), text_color="#ECEFF4")
        self.query_label.grid(row=2, column=2, pady=10)

        self.query_entry = CTkEntry(self.frame, width=100, font=("Arial", 14))
        self.query_entry.grid(row=2, column=3, pady=10)

        self.query_button = CTkButton(self.frame, text="Query Trees", command=self.query_trees, font=("Arial", 14), fg_color="#88C0D0", hover_color="#8FBCBB")
        self.query_button.grid(row=2, column=4, pady=10)

        self.event_button = CTkButton(self.frame, text="Random Event", command=self.random_event, font=("Arial", 14), fg_color="#A3BE8C", hover_color="#8FBCBB")
        self.event_button.grid(row=4, column=2, columnspan=1, pady=10)

    def update_visualization(self):
        self.canvas.delete("all") 
        section_width = 100
        padding = 20
        tree_color = "#A3BE8C"

        for i in range(1, self.n + 1):
            x1 = padding + (i - 1) * section_width
            y1 = 50
            x2 = x1 + section_width
            y2 = 350

            self.canvas.create_rectangle(x1, y1, x2, y2, outline="#4C566A", fill="#434C5E", width=2)

            self.canvas.create_text((x1 + x2) // 2, y1 - 20, text=f"Section {i}", font=("Arial", 12), fill="#ECEFF4")

            trees = self.ft.query(i) - self.ft.query(i - 1)
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=f"Trees: {trees}", font=("Arial", 12), fill="#ECEFF4")

            for j in range(trees):
                tree_x1 = x1 + 10 + (j % 5) * 12
                tree_y1 = y1 + 10 + (j // 5) * 12
                tree_x2 = tree_x1 + 8
                tree_y2 = tree_y1 + 12
                self.canvas.create_rectangle(tree_x1, tree_y1, tree_x2, tree_y2, fill=tree_color, outline="#4C566A")

    def plant_trees(self):
        try:
            section = int(self.section_entry.get())
            trees = int(self.trees_entry.get())
            if 1 <= section <= self.n:
                self.ft.update(section, trees)
                messagebox.showinfo("Success", f"Planted {trees} trees in section {section}.")
                self.update_visualization()
            else:
                messagebox.showerror("Error", "Section must be between 1 and 10.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def cut_trees(self):
        try:
            section = int(self.section_entry.get())
            trees = int(self.trees_entry.get())
            if 1 <= section <= self.n:
                self.ft.update(section, -trees)
                messagebox.showinfo("Success", f"Cut {trees} trees from section {section}.")
                self.update_visualization()
            else:
                messagebox.showerror("Error", "Section must be between 1 and 10.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input.")

    def query_trees(self):
        try:
            range_str = self.query_entry.get()
            l, r = map(int, range_str.split('-'))
            if 1 <= l <= r <= self.n:
                total = self.ft.range_query(l, r)
                messagebox.showinfo("Query Result", f"Total trees in sections {l}-{r}: {total}")
            else:
                messagebox.showerror("Error", "Invalid range.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input format. Use 'L-R'.")

    def random_event(self):
        event = random.choice(["fire", "storm", "growth"])
        section = random.randint(1, self.n)
        if event == "fire":
            trees_lost = random.randint(1, 10)
            self.ft.update(section, -trees_lost)
            messagebox.showinfo("Random Event", f"Forest fire in section {section}! Lost {trees_lost} trees.")
        elif event == "storm":
            trees_lost = random.randint(1, 5)
            self.ft.update(section, -trees_lost)
            messagebox.showinfo("Random Event", f"Storm in section {section}! Lost {trees_lost} trees.")
        elif event == "growth":
            trees_gained = random.randint(1, 5)
            self.ft.update(section, trees_gained)
            messagebox.showinfo("Random Event", f"Natural growth in section {section}! Gained {trees_gained} trees.")
        self.update_visualization()

if __name__ == "__main__":
    root = CTk()
    game = FenwickForestGame(root)
    root.mainloop()