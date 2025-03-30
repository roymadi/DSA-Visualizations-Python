import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create graph (City Map)
G = nx.Graph()
cities = ['A', 'B', 'C', 'D', 'E', 'F']
edges = [
    ('A', 'B', 4), ('A', 'C', 2),
    ('B', 'C', 5), ('B', 'D', 10),
    ('C', 'D', 3), ('C', 'E', 8),
    ('D', 'E', 6), ('D', 'F', 2),
    ('E', 'F', 7)
]

for city in cities:
    G.add_node(city)
for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

def find_shortest_path():
    start = start_var.get()
    end = end_var.get()
    if start == end:
        messagebox.showwarning("Error", "Start and Destination must be different!")
        return
    try:
        path = nx.dijkstra_path(G, start, end, weight='weight')
        cost = nx.dijkstra_path_length(G, start, end, weight='weight')
        result_var.set(f"Path: {' → '.join(path)} (Cost: {cost})")
        draw_graph(path)
    except nx.NetworkXNoPath:
        messagebox.showerror("No Path", "No available path between selected cities!")

def draw_graph(path=[]):
    plt.clf()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=12)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    canvas.draw()

root = tk.Tk()
root.title("City Navigation Game")
root.geometry("600x500")

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(frame, text="Select Start City:").grid(row=0, column=0)
ttk.Label(frame, text="Select Destination:").grid(row=1, column=0)

start_var = tk.StringVar()
end_var = tk.StringVar()
result_var = tk.StringVar()

city_menu = ttk.Combobox(frame, textvariable=start_var, values=cities, state="readonly")
city_menu.grid(row=0, column=1)

dest_menu = ttk.Combobox(frame, textvariable=end_var, values=cities, state="readonly")
dest_menu.grid(row=1, column=1)

find_btn = ttk.Button(frame, text="Find Shortest Path", command=find_shortest_path)
find_btn.grid(row=2, column=0, columnspan=2, pady=10)

result_label = ttk.Label(frame, textvariable=result_var, font=("Arial", 12))
result_label.grid(row=3, column=0, columnspan=2)

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)
draw_graph()

root.mainloop()
