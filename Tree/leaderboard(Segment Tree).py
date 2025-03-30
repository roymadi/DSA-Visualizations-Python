import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import math
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class SegmentTree:
    def __init__(self, size):
        self.size = size

        self.height = math.ceil(math.log2(size)) + 1

        self.max_size = 2 * (2 ** self.height) - 1

        self.tree = [0] * self.max_size
        self.data = [0] * size
    
    def build(self, arr):
 
        self.data = arr.copy()
        self._build_recursive(0, 0, self.size - 1)
    
    def _build_recursive(self, node, start, end):

        if start == end:
            self.tree[node] = self.data[start]
            return self.tree[node]
        
        mid = (start + end) // 2
        left_val = self._build_recursive(2 * node + 1, start, mid)
        right_val = self._build_recursive(2 * node + 2, mid + 1, end)
  
        self.tree[node] = max(left_val, right_val)
        return self.tree[node]
    
    def update(self, index, value):

        self.data[index] = value
        self._update_recursive(0, 0, self.size - 1, index, value)
    
    def _update_recursive(self, node, start, end, index, value):

        if index < start or index > end:
            return

        if start == end:
            self.tree[node] = value
            return
        
        mid = (start + end) // 2

        if index <= mid:
            self._update_recursive(2 * node + 1, start, mid, index, value)
        else:
            self._update_recursive(2 * node + 2, mid + 1, end, index, value)

        self.tree[node] = max(self.tree[2 * node + 1], self.tree[2 * node + 2])
    
    def query_max(self, query_start, query_end):
        if query_start < 0 or query_end >= self.size or query_start > query_end:
            raise ValueError("Invalid query range")
        
        return self._query_max_recursive(0, 0, self.size - 1, query_start, query_end)
    
    def _query_max_recursive(self, node, start, end, query_start, query_end):

        if query_end < start or query_start > end:
            return float('-inf')
 
        if query_start <= start and query_end >= end:
            return self.tree[node]

        mid = (start + end) // 2
        left_max = self._query_max_recursive(2 * node + 1, start, mid, query_start, query_end)
        right_max = self._query_max_recursive(2 * node + 2, mid + 1, end, query_start, query_end)
        
        return max(left_max, right_max)
    
    def get_rank(self, index):
        score = self.data[index]
        count = 0
        for i in range(self.size):
            if self.data[i] > score:
                count += 1
        return count + 1

class Player:
    def __init__(self, name, score=0, id=None):
        self.id = id if id is not None else random.randint(1000, 9999)
        self.name = name
        self.score = score
        self.history = [(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), score)]
    
    def update_score(self, new_score):
        self.score = new_score
        self.history.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), new_score))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "score": self.score,
            "history": self.history
        }
    
    @classmethod
    def from_dict(cls, data):
        player = cls(data["name"], data["score"], data["id"])
        player.history = data["history"]
        return player

class GameLeaderboard:
    def __init__(self):
        self.players = []
        self.segment_tree = None
        self.max_players = 1000
        self.load_data()
        self.build_segment_tree()
    
    def add_player(self, name, score=0):
        if len(self.players) >= self.max_players:
            return False, "Maximum player limit reached"
        
        for player in self.players:
            if player.name == name:
                return False, "Player with this name already exists"
        
        new_player = Player(name, score)
        self.players.append(new_player)
        self.build_segment_tree()
        self.save_data()
        return True, new_player
    
    def update_score(self, player_name, new_score):
        for i, player in enumerate(self.players):
            if player.name == player_name:
                player.update_score(new_score)
                if self.segment_tree:
                    self.segment_tree.update(i, new_score)
                self.save_data()
                return True, f"Updated {player_name}'s score to {new_score}"
        
        return False, f"Player {player_name} not found"
    
    def get_player_rank(self, player_name):
        for i, player in enumerate(self.players):
            if player.name == player_name:
                return self.segment_tree.get_rank(i)
        
        return -1
    
    def get_top_players(self, n=10):
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        return sorted_players[:min(n, len(sorted_players))]
    
    def get_max_score_in_range(self, start_rank, end_rank):
       
        if not self.players:
            return 0
            
        sorted_indices = [i for i, _ in sorted(enumerate(self.players), key=lambda x: self.players[x[0]].score, reverse=True)]
       
        start_rank = max(1, min(start_rank, len(self.players)))
        end_rank = max(start_rank, min(end_rank, len(self.players)))
 
        start_idx = sorted_indices[start_rank - 1]
        end_idx = sorted_indices[end_rank - 1]
        
        if start_idx > end_idx:
            start_idx, end_idx = end_idx, start_idx
            
        return self.segment_tree.query_max(start_idx, end_idx)
    
    def build_segment_tree(self):
        if not self.players:
            self.segment_tree = SegmentTree(1)
            return
            
        scores = [player.score for player in self.players]
        self.segment_tree = SegmentTree(len(scores))
        self.segment_tree.build(scores)
    
    def save_data(self):
        data = {"players": [player.to_dict() for player in self.players]}
        with open("leaderboard_data.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def load_data(self):
        if not os.path.exists("leaderboard_data.json"):
            self.players = []
            return
            
        try:
            with open("leaderboard_data.json", "r") as f:
                data = json.load(f)
                self.players = [Player.from_dict(player_data) for player_data in data.get("players", [])]
        except Exception as e:
            print(f"Error loading data: {e}")
            self.players = []

class LeaderboardUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Leaderboard")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        self.root.iconbitmap("", default="")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 11))
        self.style.configure("TButton", font=("Helvetica", 11), padding=5)
        self.style.configure("Heading.TLabel", font=("Helvetica", 16, "bold"))
        self.style.configure("Stats.TLabel", font=("Helvetica", 12), padding=10)
        
        self.leaderboard = GameLeaderboard()
        
        self.create_widgets()
        self.refresh_leaderboard()
    
    def create_widgets(self):
        main_container = ttk.Frame(self.root, padding=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        top_frame = ttk.Frame(main_container)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        title_label = ttk.Label(top_frame, text="Game Leaderboard", style="Heading.TLabel")
        title_label.pack(side=tk.LEFT, padx=5)
        
        self.stats_frame = ttk.Frame(top_frame)
        self.stats_frame.pack(side=tk.RIGHT, padx=5)
        
        self.total_players_label = ttk.Label(self.stats_frame, text="Total Players: 0", style="Stats.TLabel")
        self.total_players_label.pack(side=tk.LEFT, padx=10)
        
        self.highest_score_label = ttk.Label(self.stats_frame, text="Highest Score: 0", style="Stats.TLabel")
        self.highest_score_label.pack(side=tk.LEFT, padx=10)
        
        control_frame = ttk.Frame(main_container)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        add_button = ttk.Button(control_frame, text="Add Player", command=self.add_player)
        add_button.pack(side=tk.LEFT, padx=5)
        
        update_button = ttk.Button(control_frame, text="Update Score", command=self.update_score)
        update_button.pack(side=tk.LEFT, padx=5)
        
        refresh_button = ttk.Button(control_frame, text="Refresh", command=self.refresh_leaderboard)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        stats_button = ttk.Button(control_frame, text="View Player Stats", command=self.view_player_stats)
        stats_button.pack(side=tk.LEFT, padx=5)
        
        range_button = ttk.Button(control_frame, text="Query Range Max", command=self.query_range)
        range_button.pack(side=tk.LEFT, padx=5)
      
        search_frame = ttk.Frame(main_container)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search Player:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_player)
        
        filter_frame = ttk.Frame(main_container)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
    
        ttk.Label(filter_frame, text="Show Top:").pack(side=tk.LEFT, padx=5)
        self.limit_var = tk.StringVar(value="10")
        limit_options = ["10", "20", "50", "100", "All"]
        limit_dropdown = ttk.Combobox(filter_frame, textvariable=self.limit_var, values=limit_options, width=5)
        limit_dropdown.pack(side=tk.LEFT, padx=5)
        limit_dropdown.bind("<<ComboboxSelected>>", lambda e: self.refresh_leaderboard())
        
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.leaderboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.leaderboard_frame, text="Leaderboard")
        
        columns = ("Rank", "ID", "Name", "Score", "Last Updated")
        self.tree = ttk.Treeview(self.leaderboard_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            
        self.tree.column("Rank", width=60, anchor="center")
        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=200)
        self.tree.column("Score", width=100, anchor="center")
        self.tree.column("Last Updated", width=150)
        
        scrollbar = ttk.Scrollbar(self.leaderboard_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.chart_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.chart_frame, text="Charts")
        
        self.status_var = tk.StringVar()
        status_bar = ttk.Label(main_container, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X, padx=10, pady=5)
        
        self.create_charts()
    
    def create_charts(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        fig = plt.Figure(figsize=(10, 6), dpi=100)
        
        chart_frame_top = ttk.Frame(self.chart_frame)
        chart_frame_top.pack(fill=tk.BOTH, expand=True)
        
        ax1 = fig.add_subplot(121)
        top_players = self.leaderboard.get_top_players(10)
        
        if top_players:
            names = [player.name for player in top_players]
            scores = [player.score for player in top_players]
            
            display_names = [name[:10] + "..." if len(name) > 10 else name for name in names]
            
            bars = ax1.bar(display_names, scores, color='skyblue')
            ax1.set_title('Top 10 Players')
            ax1.set_ylabel('Score')
            ax1.set_xlabel('Player')
            
            for bar in bars:
                height = bar.get_height()
                ax1.annotate(f'{height}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
            
            plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
        else:
            ax1.text(0.5, 0.5, 'No player data available', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax1.transAxes)
        
        ax2 = fig.add_subplot(122)
        
        if self.leaderboard.players:
            ranges = [0, 100, 500, 1000, 5000, 10000, float('inf')]
            labels = ['0-99', '100-499', '500-999', '1000-4999', '5000-9999', '10000+']
            counts = [0] * len(labels)
            
            for player in self.leaderboard.players:
                for i, upper in enumerate(ranges[1:]):
                    if player.score < upper:
                        counts[i] += 1
                        break
            
            non_zero_labels = [label for label, count in zip(labels, counts) if count > 0]
            non_zero_counts = [count for count in counts if count > 0]
            
            if non_zero_counts:
                ax2.pie(non_zero_counts, labels=non_zero_labels, autopct='%1.1f%%',
                        shadow=True, startangle=90)
                ax2.set_title('Score Distribution')
            else:
                ax2.text(0.5, 0.5, 'No score distribution data', 
                        horizontalalignment='center', verticalalignment='center',
                        transform=ax2.transAxes)
        else:
            ax2.text(0.5, 0.5, 'No player data available', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax2.transAxes)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame_top)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def refresh_leaderboard(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        limit = self.limit_var.get()
        
        if limit == "All":
            players = self.leaderboard.players
        else:
            players = self.leaderboard.players[:int(limit)]
        
        sorted_players = sorted(players, key=lambda p: p.score, reverse=True)
        
        for i, player in enumerate(sorted_players):
            last_updated = player.history[-1][0] if player.history else "N/A"
            self.tree.insert("", tk.END, values=(i+1, player.id, player.name, player.score, last_updated))
        
        self.total_players_label.config(text=f"Total Players: {len(self.leaderboard.players)}")
        
        highest_score = max([player.score for player in self.leaderboard.players]) if self.leaderboard.players else 0
        self.highest_score_label.config(text=f"Highest Score: {highest_score}")
        
        self.create_charts()
        
        self.status_var.set(f"Leaderboard refreshed. Showing {min(len(sorted_players), len(self.leaderboard.players))} of {len(self.leaderboard.players)} players.")
    
    def add_player(self):
        player_name = simpledialog.askstring("Add Player", "Enter player name:")
        if not player_name:
            return
            
        initial_score = simpledialog.askinteger("Add Player", "Enter initial score:", minvalue=0, initialvalue=0)
        if initial_score is None:
            initial_score = 0
        
        success, result = self.leaderboard.add_player(player_name, initial_score)
        
        if success:
            self.status_var.set(f"Player {player_name} added successfully.")
        else:
            messagebox.showerror("Error", result)
            
        self.refresh_leaderboard()
    
    def update_score(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Select Player", "Please select a player to update.")
            return
            
        item = selected_items[0]
        player_name = self.tree.item(item, 'values')[2]
        
        new_score = simpledialog.askinteger("Update Score", f"Enter new score for {player_name}:", minvalue=0)
        if new_score is None:
            return
            
        success, message = self.leaderboard.update_score(player_name, new_score)
        
        if success:
            self.status_var.set(message)
        else:
            messagebox.showerror("Error", message)
            
        self.refresh_leaderboard()
    
    def search_player(self, event=None):
        search_text = self.search_var.get().lower()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not search_text:
            self.refresh_leaderboard()
            return
            
        filtered_players = [p for p in self.leaderboard.players if search_text in p.name.lower()]
        sorted_players = sorted(filtered_players, key=lambda p: p.score, reverse=True)
        
        for i, player in enumerate(sorted_players):
            last_updated = player.history[-1][0] if player.history else "N/A"
            self.tree.insert("", tk.END, values=(i+1, player.id, player.name, player.score, last_updated))
        
        self.status_var.set(f"Found {len(sorted_players)} players matching '{search_text}'")
    
    def view_player_stats(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Select Player", "Please select a player to view stats.")
            return
            
        item = selected_items[0]
        player_name = self.tree.item(item, 'values')[2]
        
        player = None
        for p in self.leaderboard.players:
            if p.name == player_name:
                player = p
                break
                
        if not player:
            messagebox.showerror("Error", "Player not found.")
            return
            
        stats_window = tk.Toplevel(self.root)
        stats_window.title(f"Stats for {player.name}")
        stats_window.geometry("600x400")
        stats_window.configure(bg="#f0f0f0")
        
        container = ttk.Frame(stats_window, padding=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        info_frame = ttk.Frame(container)
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text=f"Player: {player.name}", font=("Helvetica", 14, "bold")).pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"ID: {player.id}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Current Score: {player.score}").pack(anchor=tk.W)
        
        rank = self.leaderboard.get_player_rank(player.name)
        ttk.Label(info_frame, text=f"Current Rank: {rank}").pack(anchor=tk.W)
        
        fig = plt.Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        if len(player.history) > 1:
            dates = [h[0] for h in player.history]
            scores = [h[1] for h in player.history]
            
            display_dates = [d.split()[0] for d in dates]  
            
            ax.plot(display_dates, scores, marker='o')
            ax.set_title('Score History')
            ax.set_ylabel('Score')
            ax.set_xlabel('Date')
            
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, 'Not enough history data', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        history_frame = ttk.Frame(container)
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Label(history_frame, text="Score History:", font=("Helvetica", 12, "bold")).pack(anchor=tk.W)
       
        columns = ("Timestamp", "Score")
        history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=5)
        
        for col in columns:
            history_tree.heading(col, text=col)
           
        history_tree.column("Timestamp", width=200)
        history_tree.column("Score", width=100, anchor="center")
       
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=history_tree.yview)
        history_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        for timestamp, score in reversed(player.history):
            history_tree.insert("", tk.END, values=(timestamp, score))
    
    def query_range(self):
        if not self.leaderboard.players:
            messagebox.showinfo("No Players", "No players in the leaderboard.")
            return
         
        start_rank = simpledialog.askinteger("Query Range", "Enter start rank:", minvalue=1, maxvalue=len(self.leaderboard.players))
        if start_rank is None:
            return
            
        end_rank = simpledialog.askinteger("Query Range", "Enter end rank:", minvalue=start_rank, maxvalue=len(self.leaderboard.players))
        if end_rank is None:
            return
            
        max_score = self.leaderboard.get_max_score_in_range(start_rank, end_rank)
        
        messagebox.showinfo("Query Result", f"Maximum score between rank {start_rank} and {end_rank} is: {max_score}")

def main():
    root = tk.Tk()
    app = LeaderboardUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()