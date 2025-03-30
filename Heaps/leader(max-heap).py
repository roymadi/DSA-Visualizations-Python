import heapq
import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
from datetime import datetime
import json
import os

class Leaderboard:
    def __init__(self):
        self.heap = []
        self.player_history = {}  
        
    def add_player(self, name, score, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        heapq.heappush(self.heap, (-score, name, timestamp))
        
        if name not in self.player_history:
            self.player_history[name] = []
        self.player_history[name].append((score, timestamp))
    
    def get_top_players(self, n):
        return heapq.nsmallest(n, self.heap)
    
    def get_player_history(self, name):
        return self.player_history.get(name, [])
    
    def search_player(self, name):
        results = []
        for score, player_name, timestamp in self.heap:
            if name.lower() in player_name.lower():
                results.append((-score, player_name, timestamp))
        return results
    
    def delete_player(self, name, score):
        for i, entry in enumerate(self.heap):
            entry_score, entry_name, _ = entry
            if entry_name == name and entry_score == -score:
                self.heap.pop(i)
                self.rebuild_heap()
                if name in self.player_history:
                    self.player_history[name] = [h for h in self.player_history[name] if h[0] != score]
                    if not self.player_history[name]:
                        del self.player_history[name]
                return True
        return False
    
    def rebuild_heap(self):
        heapq.heapify(self.heap)
    
    def reset(self):
        self.heap = []
        self.player_history = {}
    
    def save_to_file(self, filename="leaderboard_data.json"):
        data = {
            "entries": [(str(-score), name, timestamp) for score, name, timestamp in self.heap],
            "player_history": {name: [(str(score), timestamp) for score, timestamp in history] 
                              for name, history in self.player_history.items()}
        }
        with open(filename, "w") as f:
            json.dump(data, f)
    
    def load_from_file(self, filename="leaderboard_data.json"):
        if not os.path.exists(filename):
            return False
        
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            self.heap = []
            for score, name, timestamp in data["entries"]:
                heapq.heappush(self.heap, (-int(score), name, timestamp))
            
            self.player_history = {}
            for name, history in data["player_history"].items():
                self.player_history[name] = [(int(score), timestamp) for score, timestamp in history]
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False

class LeaderboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Leaderboard")
        self.root.geometry("800x600")
        self.style = Style(theme="superhero")
        
        self.leaderboard = Leaderboard()
        self.leaderboard.load_from_file()  
        
        self.create_menu()
        self.create_tabs()
        
        if not self.leaderboard.heap:
            sample_data = [
                ("Alice", 100),
                ("Bob", 200),
                ("Charlie", 150),
                ("David", 180),
                ("Eve", 120)
            ]
            for name, score in sample_data:
                self.leaderboard.add_player(name, score)
        
        self.update_leaderboard()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_command(label="Load", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Add Player", command=self.add_player)
        edit_menu.add_command(label="Delete Selected", command=self.delete_selected)
        edit_menu.add_command(label="Reset All", command=self.reset_leaderboard)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        
        self.theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Themes", menu=self.theme_menu)
        
        themes = ["superhero", "darkly", "cyborg", "solar", "flatly", "litera", "minty", "lumen", "cosmo"]
        self.current_theme = tk.StringVar()
        self.current_theme.set("superhero")
        
        for theme in themes:
            self.theme_menu.add_radiobutton(
                label=theme.capitalize(),
                variable=self.current_theme,
                value=theme,
                command=lambda t=theme: self.change_theme(t)
            )
    
    def create_tabs(self):
        self.tabControl = ttk.Notebook(self.root)
        
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text="Leaderboard")
        
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text="Player Stats")
        
        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab3, text="Search")
        
        self.tabControl.pack(expand=1, fill="both")
        
        self.setup_leaderboard_tab()
        self.setup_stats_tab()
        self.setup_search_tab()
    
    def setup_leaderboard_tab(self):
        top_frame = ttk.Frame(self.tab1)
        top_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ttk.Label(top_frame, text="Game Leaderboard", font=("Helvetica", 18, "bold"))
        title_label.pack(side="left", padx=10)
        
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(side="right", padx=10)
        
        add_button = ttk.Button(button_frame, text="Add Player", command=self.add_player)
        add_button.pack(side="left", padx=5)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_selected)
        delete_button.pack(side="left", padx=5)
        
        reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_leaderboard)
        reset_button.pack(side="left", padx=5)
        
        columns = ("rank", "name", "score", "date")
        self.tree = ttk.Treeview(self.tab1, columns=columns, show="headings", height=20)
        
        self.tree.heading("rank", text="Rank")
        self.tree.heading("name", text="Player Name")
        self.tree.heading("score", text="Score")
        self.tree.heading("date", text="Date Added")
        
        self.tree.column("rank", width=50, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("score", width=100, anchor="e")
        self.tree.column("date", width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(self.tab1, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=1, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.tab1, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
    
    def setup_stats_tab(self):
        # Player selection
        selection_frame = ttk.Frame(self.tab2)
        selection_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(selection_frame, text="Select Player:").pack(side="left", padx=5)
        
        self.player_var = tk.StringVar()
        self.player_combo = ttk.Combobox(selection_frame, textvariable=self.player_var)
        self.player_combo.pack(side="left", padx=5)
        
        ttk.Button(selection_frame, text="View Stats", command=self.view_player_stats).pack(side="left", padx=5)
        
        stats_frame = ttk.LabelFrame(self.tab2, text="Player Statistics")
        stats_frame.pack(fill="both", expand=1, padx=10, pady=10)
        
        columns = ("date", "score")
        self.stats_tree = ttk.Treeview(stats_frame, columns=columns, show="headings", height=15)
        
        self.stats_tree.heading("date", text="Date")
        self.stats_tree.heading("score", text="Score")
        
        self.stats_tree.column("date", width=200, anchor="w")
        self.stats_tree.column("score", width=100, anchor="e")
        
        self.summary_frame = ttk.Frame(stats_frame)
        self.summary_frame.pack(side="top", fill="x", padx=10, pady=10)
        
        self.best_score_var = tk.StringVar(value="Best Score: -")
        self.avg_score_var = tk.StringVar(value="Average Score: -")
        self.total_games_var = tk.StringVar(value="Total Games: -")
        
        ttk.Label(self.summary_frame, textvariable=self.best_score_var, font=("Helvetica", 12)).pack(side="left", padx=20)
        ttk.Label(self.summary_frame, textvariable=self.avg_score_var, font=("Helvetica", 12)).pack(side="left", padx=20)
        ttk.Label(self.summary_frame, textvariable=self.total_games_var, font=("Helvetica", 12)).pack(side="left", padx=20)
        
        scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=scrollbar.set)
        
        self.stats_tree.pack(side="left", fill="both", expand=1, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
    
    def setup_search_tab(self):
        search_frame = ttk.Frame(self.tab3)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(search_frame, text="Search Player:").pack(side="left", padx=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side="left", padx=5)
        
        ttk.Button(search_frame, text="Search", command=self.search_players).pack(side="left", padx=5)
        
        columns = ("name", "score", "date")
        self.search_tree = ttk.Treeview(self.tab3, columns=columns, show="headings", height=20)
        
        self.search_tree.heading("name", text="Player Name")
        self.search_tree.heading("score", text="Score")
        self.search_tree.heading("date", text="Date Added")
        
        self.search_tree.column("name", width=200, anchor="w")
        self.search_tree.column("score", width=100, anchor="e")
        self.search_tree.column("date", width=150, anchor="center")
        
        scrollbar = ttk.Scrollbar(self.tab3, orient="vertical", command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar.set)
        
        self.search_tree.pack(side="left", fill="both", expand=1, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
    
    def update_leaderboard(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        player_names = set()
        
        top_players = self.leaderboard.get_top_players(100)  # Show up to 100 players
        for i, (score, name, timestamp) in enumerate(top_players, 1):
            self.tree.insert("", "end", values=(i, name, -score, timestamp))
            player_names.add(name)
        
        self.player_combo['values'] = sorted(list(player_names))
        
        total_players = len(top_players)
        self.status_var.set(f"Total players: {total_players}")
    
    def add_player(self):
        popup = tk.Toplevel(self.root)
        popup.title("Add Player")
        popup.geometry("350x200")
        popup.transient(self.root)
        popup.grab_set()
        
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
        frame = ttk.Frame(popup, padding="20 20 20 20")
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Player Name:").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(frame, width=25)
        name_entry.grid(row=0, column=1, pady=5, padx=5)
        name_entry.focus_set()
        
        ttk.Label(frame, text="Score:").grid(row=1, column=0, sticky="w", pady=5)
        score_entry = ttk.Entry(frame, width=25)
        score_entry.grid(row=1, column=1, pady=5, padx=5)
        
        error_var = tk.StringVar()
        error_label = ttk.Label(frame, textvariable=error_var, foreground="red")
        error_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        def save_player():
            name = name_entry.get().strip()
            score_text = score_entry.get().strip()
            
            if not name:
                error_var.set("Please enter a player name")
                return
            
            try:
                score = int(score_text)
                if score < 0:
                    error_var.set("Score must be a positive number")
                    return
            except ValueError:
                error_var.set("Score must be a valid number")
                return
            
            self.leaderboard.add_player(name, score)
            self.update_leaderboard()
            self.save_data()  # Auto-save when adding new player
            popup.destroy()
        
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Save", command=save_player).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=5)
    
    def delete_selected(self):
        selected_item = self.tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Information", "Please select a player to delete")
            return
        
        values = self.tree.item(selected_item, 'values')
        name = values[1]
        score = int(values[2])
        
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {name} with score {score}?")
        
        if confirm:
            if self.leaderboard.delete_player(name, score):
                self.update_leaderboard()
                self.status_var.set(f"Deleted {name} with score {score}")
                self.save_data()  # Auto-save when deleting
            else:
                messagebox.showerror("Error", "Failed to delete player")
    
    def reset_leaderboard(self):
        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the entire leaderboard?")
        
        if confirm:
            self.leaderboard.reset()
            self.update_leaderboard()
            self.status_var.set("Leaderboard has been reset")
            self.save_data()  # Auto-save when resetting
    
    def view_player_stats(self):
        player_name = self.player_var.get()
        
        if not player_name:
            messagebox.showinfo("Information", "Please select a player")
            return
        
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        history = self.leaderboard.get_player_history(player_name)
        
        if not history:
            self.best_score_var.set("Best Score: -")
            self.avg_score_var.set("Average Score: -")
            self.total_games_var.set("Total Games: 0")
            return
        
        history.sort(key=lambda x: x[1], reverse=True)
        
        for score, timestamp in history:
            self.stats_tree.insert("", "end", values=(timestamp, score))
        
        scores = [score for score, _ in history]
        best_score = max(scores)
        avg_score = sum(scores) / len(scores)
        total_games = len(scores)
        
        self.best_score_var.set(f"Best Score: {best_score}")
        self.avg_score_var.set(f"Average Score: {avg_score:.1f}")
        self.total_games_var.set(f"Total Games: {total_games}")
    
    def search_players(self):
        search_term = self.search_var.get().strip()
        
        if not search_term:
            messagebox.showinfo("Information", "Please enter a search term")
            return
        
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)
        
        results = self.leaderboard.search_player(search_term)
        
        if not results:
            messagebox.showinfo("Search Results", f"No players found matching '{search_term}'")
            return
        
        for score, name, timestamp in results:
            self.search_tree.insert("", "end", values=(name, score, timestamp))
    
    def save_data(self):
        self.leaderboard.save_to_file()
        self.status_var.set("Leaderboard saved successfully")
    
    def load_data(self):
        success = self.leaderboard.load_from_file()
        
        if success:
            self.update_leaderboard()
            self.status_var.set("Leaderboard loaded successfully")
        else:
            messagebox.showerror("Error", "Failed to load leaderboard data")
    
    def change_theme(self, theme_name):
        self.style.theme_use(theme_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = LeaderboardApp(root)
    
    def on_closing():
        if messagebox.askyesno("Save before exit", "Do you want to save data before exiting?"):
            app.save_data()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()