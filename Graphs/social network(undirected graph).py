import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from matplotlib.figure import Figure
import numpy as np

class SocialNetworkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Social Network Simulator")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f2f5")
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Helvetica', 10), background='#1877f2', foreground='white')
        self.style.configure('TFrame', background='#f0f2f5')
        self.style.configure('TLabel', background='#f0f2f5', font=('Helvetica', 10))
        
        self.graph = nx.Graph()

        self.selected_person = None
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        selection_frame = ttk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(selection_frame, text="Select Person:").pack(side=tk.LEFT, padx=5)
        self.person_selector = ttk.Combobox(selection_frame, state="readonly")
        self.person_selector.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.person_selector.bind("<<ComboboxSelected>>", self.on_person_selected)
        
        self.btn_clear_selection = ttk.Button(selection_frame, text="Clear Selection", command=self.clear_selection)
        self.btn_clear_selection.pack(side=tk.LEFT, padx=5)
        
        friends_frame = ttk.LabelFrame(main_frame, text="Friends")
        friends_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)
        
        self.friends_listbox = tk.Listbox(friends_frame, width=20, height=15, bg="white")
        self.friends_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        graph_frame = ttk.Frame(main_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.fig.patch.set_facecolor('#f0f2f5')
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.canvas.mpl_connect('button_press_event', self.on_graph_click)
        
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        btn_add_person = ttk.Button(control_frame, text="Add Person", command=self.add_person)
        btn_add_person.pack(side=tk.LEFT, padx=5)
        
        btn_add_friendship = ttk.Button(control_frame, text="Add Friendship", command=self.add_friendship)
        btn_add_friendship.pack(side=tk.LEFT, padx=5)
        
        btn_remove_person = ttk.Button(control_frame, text="Remove Person", command=self.remove_person)
        btn_remove_person.pack(side=tk.LEFT, padx=5)
        
        btn_generate_random = ttk.Button(control_frame, text="Generate Random Network", command=self.generate_random_network)
        btn_generate_random.pack(side=tk.LEFT, padx=5)
        
        btn_analyze = ttk.Button(control_frame, text="Analyze Network", command=self.analyze_network)
        btn_analyze.pack(side=tk.LEFT, padx=5)
        
        self.lbl_nodes = ttk.Label(stats_frame, text="People: 0")
        self.lbl_nodes.pack(side=tk.LEFT, padx=10)
        
        self.lbl_edges = ttk.Label(stats_frame, text="Friendships: 0")
        self.lbl_edges.pack(side=tk.LEFT, padx=10)
        
        self.lbl_density = ttk.Label(stats_frame, text="Network Density: 0")
        self.lbl_density.pack(side=tk.LEFT, padx=10)
        
        self.lbl_communities = ttk.Label(stats_frame, text="Communities: 0")
        self.lbl_communities.pack(side=tk.LEFT, padx=10)
        
        self.node_positions = {}
        
        self.generate_random_network(size=10)
    
    def add_person(self):
        name = simpledialog.askstring("Add Person", "Enter person's name:")
        if name and name not in self.graph.nodes:
            self.graph.add_node(name)
            self.update_graph()
            self.update_stats()
            self.update_person_selector()
        elif name in self.graph.nodes:
            messagebox.showwarning("Warning", f"Person '{name}' already exists!")
    
    def remove_person(self):
        if not self.graph.nodes:
            messagebox.showinfo("Info", "No people to remove!")
            return
            
        name = simpledialog.askstring("Remove Person", "Enter person's name:")
        if name and name in self.graph.nodes:
            if name == self.selected_person:
                self.selected_person = None
            
            self.graph.remove_node(name)
            self.update_graph()
            self.update_stats()
            self.update_person_selector()
        else:
            messagebox.showwarning("Warning", f"Person '{name}' not found!")
    
    def add_friendship(self):
        if len(self.graph.nodes) < 2:
            messagebox.showinfo("Info", "Need at least 2 people to create a friendship!")
            return
            
        person1 = simpledialog.askstring("Add Friendship", "Enter first person's name:")
        if person1 and person1 in self.graph.nodes:
            person2 = simpledialog.askstring("Add Friendship", "Enter second person's name:")
            if person2 and person2 in self.graph.nodes:
                if person1 != person2:
                    if not self.graph.has_edge(person1, person2):
                        self.graph.add_edge(person1, person2)
                        self.update_graph()
                        self.update_stats()
                        self.update_friends_list()
                    else:
                        messagebox.showinfo("Info", f"{person1} and {person2} are already friends!")
                else:
                    messagebox.showwarning("Warning", "Cannot create friendship with self!")
            else:
                messagebox.showwarning("Warning", f"Person '{person2}' not found!")
        else:
            messagebox.showwarning("Warning", f"Person '{person1}' not found!")
    
    def generate_random_network(self, size=None):
        if size is None:
            size = simpledialog.askinteger("Random Network", "Enter number of people:", minvalue=2, maxvalue=50)
        
        if size:
            self.graph = nx.gnp_random_graph(size, 0.3)
            
            name_mapping = {}
            names = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Helen", "Igor", 
                     "Julia", "Kevin", "Laura", "Mike", "Nina", "Oscar", "Pam", "Quincy", "Rachel",
                     "Sam", "Tina", "Ursula", "Victor", "Wendy", "Xander", "Yvonne", "Zach"]
            
            for i in range(size):
                if i < len(names):
                    name = names[i]
                else:
                    name = f"Person_{i+1}"
                name_mapping[i] = name
            
            self.graph = nx.relabel_nodes(self.graph, name_mapping)
            self.selected_person = None
            self.update_graph()
            self.update_stats()
            self.update_person_selector()
    
    def analyze_network(self):
        if len(self.graph.nodes) == 0:
            messagebox.showinfo("Info", "No network to analyze!")
            return
            
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Network Analysis")
        analysis_window.geometry("600x400")
        
        degree_centrality = nx.degree_centrality(self.graph)
        betweenness_centrality = nx.betweenness_centrality(self.graph)
        closeness_centrality = nx.closeness_centrality(self.graph)
        
        sorted_by_popularity = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
        
        tree = ttk.Treeview(analysis_window, columns=("Person", "Degree", "Betweenness", "Closeness"))
        tree.heading("Person", text="Person")
        tree.heading("Degree", text="Popularity")
        tree.heading("Betweenness", text="Influence")
        tree.heading("Closeness", text="Reach")
        tree.column("#0", width=0, stretch=tk.NO)
        
        for person, degree in sorted_by_popularity:
            tree.insert("", tk.END, values=(
                person, 
                f"{degree:.3f}", 
                f"{betweenness_centrality[person]:.3f}", 
                f"{closeness_centrality[person]:.3f}"
            ))
            
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        explanation_frame = ttk.Frame(analysis_window)
        explanation_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(explanation_frame, text="Popularity: How many connections a person has").pack(anchor=tk.W)
        ttk.Label(explanation_frame, text="Influence: How often a person is on the shortest path between others").pack(anchor=tk.W)
        ttk.Label(explanation_frame, text="Reach: How quickly a person can reach everyone in the network").pack(anchor=tk.W)
    
    def update_graph(self):
        self.ax.clear()
        
        if not self.graph.nodes:
            self.canvas.draw()
            return
        
        pos = nx.spring_layout(self.graph)
        self.node_positions = pos
        
        degrees = dict(self.graph.degree())
        
        node_colors = []
        node_sizes = []
        edge_colors = []
        edge_widths = []
        
        selected_neighbors = set()
        
        if self.selected_person and self.selected_person in self.graph.nodes:
            selected_neighbors = set(self.graph.neighbors(self.selected_person))
            
            for node in self.graph.nodes:
                if node == self.selected_person:
                    node_colors.append('#e41a1c')
                    node_sizes.append(500)
                elif node in selected_neighbors:
                    node_colors.append('#ff7f00')
                    node_sizes.append(400)
                else:
                    node_colors.append('#a6cee3')
                    node_sizes.append(300)
                    
            for u, v in self.graph.edges:
                if u == self.selected_person or v == self.selected_person:
                    edge_colors.append('#ff7f00')
                    edge_widths.append(2.5)
                else:
                    edge_colors.append('#cccccc')
                    edge_widths.append(1.0)
        else:
            if len(self.graph.nodes) > 1:
                centrality = nx.betweenness_centrality(self.graph)
                node_colors = [plt.cm.viridis(centrality[node] * 0.8 + 0.2) for node in self.graph.nodes]
            else:
                node_colors = ['#4267B2']  
                
            node_sizes = [300 + 100 * degrees[node] for node in self.graph.nodes]
            edge_colors = ['#dfe3ee'] * len(self.graph.edges)
            edge_widths = [1.5] * len(self.graph.edges)
        
        nx.draw_networkx_nodes(self.graph, pos, ax=self.ax, node_size=node_sizes, 
                               node_color=node_colors, alpha=0.9, edgecolors='white')
        
        nx.draw_networkx_edges(self.graph, pos, ax=self.ax, width=edge_widths, 
                              alpha=0.7, edge_color=edge_colors)
        
        if self.selected_person:
            label_colors = {}
            for node in self.graph.nodes:
                if node == self.selected_person:
                    label_colors[node] = 'white'
                elif node in selected_neighbors:
                    label_colors[node] = 'white'
                else:
                    label_colors[node] = 'black'
                    
            for node, (x, y) in pos.items():
                self.ax.text(x, y, node, fontsize=10, fontweight='bold', 
                          ha='center', va='center', color=label_colors[node])
        else:
            nx.draw_networkx_labels(self.graph, pos, ax=self.ax, font_size=10, 
                                  font_weight='bold', font_color='white')
        
        self.ax.set_facecolor('#f0f2f5')
        self.ax.axis('off')
        self.canvas.draw()
    
    def update_stats(self):
        num_nodes = len(self.graph.nodes)
        num_edges = len(self.graph.edges)
        
        self.lbl_nodes.config(text=f"People: {num_nodes}")
        self.lbl_edges.config(text=f"Friendships: {num_edges}")
        
        if num_nodes > 1:
            density = nx.density(self.graph)
            self.lbl_density.config(text=f"Network Density: {density:.3f}")
        else:
            self.lbl_density.config(text="Network Density: N/A")
        
        if num_nodes > 0:
            communities = nx.algorithms.community.greedy_modularity_communities(self.graph)
            self.lbl_communities.config(text=f"Communities: {len(communities)}")
        else:
            self.lbl_communities.config(text="Communities: 0")
    
    def update_person_selector(self):
        people = sorted(list(self.graph.nodes))
        self.person_selector['values'] = people
        
        if self.selected_person not in self.graph.nodes:
            self.selected_person = None
        
        if self.selected_person:
            self.person_selector.set(self.selected_person)
        else:
            self.person_selector.set('')
    
    def on_person_selected(self, event):
        selected = self.person_selector.get()
        if selected:
            self.selected_person = selected
            self.update_graph()
            self.update_friends_list()
    
    def clear_selection(self):
        self.selected_person = None
        self.person_selector.set('')
        self.friends_listbox.delete(0, tk.END)
        self.update_graph()
    
    def update_friends_list(self):
        self.friends_listbox.delete(0, tk.END)
        
        if self.selected_person and self.selected_person in self.graph.nodes:
            friends = sorted(list(self.graph.neighbors(self.selected_person)))
            
            if friends:
                for friend in friends:
                    self.friends_listbox.insert(tk.END, friend)
            else:
                self.friends_listbox.insert(tk.END, "No friends yet")
    
    def on_graph_click(self, event):
        if event.inaxes != self.ax:
            return
            
        min_dist = float('inf')
        closest_node = None
        
        for node, (x, y) in self.node_positions.items():
            dist = (x - event.xdata)**2 + (y - event.ydata)**2
            if dist < min_dist:
                min_dist = dist
                closest_node = node
        
        threshold = 0.03
        if min_dist < threshold and closest_node:
            self.selected_person = closest_node
            self.person_selector.set(closest_node)
            self.update_graph()
            self.update_friends_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialNetworkSimulator(root)
    root.mainloop()