import customtkinter as ctk
from collections import defaultdict, Counter
import heapq
import math


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def fractional_knapsack(weights, values, capacity):
    items = list(zip(values, weights))
    items.sort(key=lambda x: x[0] / x[1], reverse=True)

    total_value = 0
    for value, weight in items:
        if capacity >= weight:
            total_value += value
            capacity -= weight
        else:
            total_value += (value / weight) * capacity
            break

    return total_value


def activity_selection(start_times, end_times):
    activities = list(zip(start_times, end_times))
    activities.sort(key=lambda x: x[1])  

    selected = []
    last_end = -1
    for start, end in activities:
        if start >= last_end:
            selected.append((start, end))
            last_end = end

    return selected


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    heap = [HuffmanNode(char, f) for char, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def build_huffman_codes(node, prefix="", code=None):
    if code is None:
        code = {}
    if node:
        if node.char is not None:
            code[node.char] = prefix
        build_huffman_codes(node.left, prefix + "0", code)
        build_huffman_codes(node.right, prefix + "1", code)
    return code

def huffman_coding(text):
    root = build_huffman_tree(text)
    codes = build_huffman_codes(root)
    encoded_text = "".join([codes[char] for char in text])
    return codes, encoded_text, root

def huffman_decoding(encoded_text, root):
    decoded_text = []
    current = root
    for bit in encoded_text:
        if bit == '0':
            current = current.left
        else:
            current = current.right
        if current.char is not None:
            decoded_text.append(current.char)
            current = root
    return "".join(decoded_text)


def coin_change_greedy(coins, amount):
    coins.sort(reverse=True)
    result = []
    for coin in coins:
        while amount >= coin:
            result.append(coin)
            amount -= coin
    return result if amount == 0 else []


def job_sequencing(jobs):
    jobs.sort(key=lambda x: x[2], reverse=True)  
    max_deadline = max(job[1] for job in jobs)
    schedule = [None] * (max_deadline + 1)
    total_profit = 0

    for job in jobs:
        for i in range(job[1], 0, -1):
            if schedule[i] is None:
                schedule[i] = job[0]
                total_profit += job[2]
                break

    return schedule[1:], total_profit


def prim_mst(graph):
    mst = []
    visited = set()
    start_node = list(graph.keys())[0]
    visited.add(start_node)
    edges = [
        (cost, start_node, neighbor)
        for neighbor, cost in graph[start_node]
    ]
    heapq.heapify(edges)

    while edges:
        cost, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, cost))
            for neighbor, cost2 in graph[v]:
                if neighbor not in visited:
                    heapq.heappush(edges, (cost2, v, neighbor))

    return mst


class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 1 for node in nodes}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                if self.rank[root1] == self.rank[root2]:
                    self.rank[root2] += 1

def kruskal_mst(graph):
    edges = []
    for u in graph:
        for v, cost in graph[u]:
            edges.append((cost, u, v))
    edges.sort()

    nodes = set(graph.keys())
    uf = UnionFind(nodes)
    mst = []

    for cost, u, v in edges:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            mst.append((u, v, cost))

    return mst


def water_connection_problem(pipes, houses):
    connections = []
    for house in houses:
        if house not in pipes:
            connections.append((house, house, 0))  
        else:
            next_house, diameter = pipes[house]
            connections.append((house, next_house, diameter))
    return connections


def min_swaps_bracket_balancing(s):
    swaps = 0
    balance = 0
    for char in s:
        if char == '[':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            swaps += 1
            balance += 2
    return swaps


def fitting_shelves(wall_length, shelf1, shelf2):
    min_waste = wall_length
    best_config = (0, 0, wall_length)
    for i in range(wall_length // shelf1 + 1):
        remaining = wall_length - i * shelf1
        j = remaining // shelf2
        waste = remaining - j * shelf2
        if waste < min_waste:
            min_waste = waste
            best_config = (i, j, waste)
    return best_config


def assign_mice_to_holes(mice, holes):
    mice.sort()
    holes.sort()
    max_distance = 0
    for i in range(len(mice)):
        max_distance = max(max_distance, abs(mice[i] - holes[i]))
    return max_distance


class GreedyAlgorithmsGame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Greedy Algorithms Game")
        self.geometry("1200x800")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        self.tab1 = self.tabview.add("Fractional Knapsack")
        self.tab2 = self.tabview.add("Activity Selection")
        self.tab3 = self.tabview.add("Huffman Coding")
        self.tab4 = self.tabview.add("Coin Change")
        self.tab5 = self.tabview.add("Job Sequencing")
        self.tab6 = self.tabview.add("Prim's Algorithm")
        self.tab7 = self.tabview.add("Kruskal's Algorithm")
        self.tab9 = self.tabview.add("Water Connection")
        self.tab10 = self.tabview.add("Bracket Balancing")
        self.tab11 = self.tabview.add("Fitting Shelves")
        self.tab12 = self.tabview.add("Mice to Holes")

        self.setup_fractional_knapsack_tab()
        self.setup_activity_selection_tab()
        self.setup_huffman_coding_tab()
        self.setup_coin_change_tab()
        self.setup_job_sequencing_tab()
        self.setup_prims_tab()
        self.setup_kruskals_tab()
        self.setup_water_connection_tab()
        self.setup_bracket_balancing_tab()
        self.setup_fitting_shelves_tab()
        self.setup_mice_to_holes_tab()

    def create_two_column_layout(self, tab):

        frame = ctk.CTkFrame(tab)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        left_column = ctk.CTkFrame(frame)
        left_column.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        right_column = ctk.CTkFrame(frame)
        right_column.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        return left_column, right_column

    def setup_fractional_knapsack_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab1)

        weights_label = ctk.CTkLabel(left_column, text="Weights (comma-separated):")
        weights_label.pack(pady=5)
        self.weights_entry = ctk.CTkEntry(left_column, width=300)
        self.weights_entry.pack(pady=5)

        values_label = ctk.CTkLabel(left_column, text="Values (comma-separated):")
        values_label.pack(pady=5)
        self.values_entry = ctk.CTkEntry(left_column, width=300)
        self.values_entry.pack(pady=5)

        capacity_label = ctk.CTkLabel(left_column, text="Capacity:")
        capacity_label.pack(pady=5)
        self.capacity_entry = ctk.CTkEntry(left_column, width=300)
        self.capacity_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_fractional_knapsack)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_fractional_knapsack)
        solve_button.pack(pady=10)

        self.fractional_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.fractional_result_label.pack(pady=10)

    def sample_fractional_knapsack(self):
        self.weights_entry.delete(0, "end")
        self.values_entry.delete(0, "end")
        self.capacity_entry.delete(0, "end")
        self.weights_entry.insert(0, "10,20,30")
        self.values_entry.insert(0, "60,100,120")
        self.capacity_entry.insert(0, "50")

    def solve_fractional_knapsack(self):
        try:
            weights = list(map(int, self.weights_entry.get().split(',')))
            values = list(map(int, self.values_entry.get().split(',')))
            capacity = int(self.capacity_entry.get())

            if len(weights) != len(values):
                self.fractional_result_label.configure(text="Number of weights and values must be equal.", text_color="red")
                return

            result = fractional_knapsack(weights, values, capacity)
            self.fractional_result_label.configure(text=f"Maximum value: {result:.2f}", text_color="green")
        except ValueError:
            self.fractional_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

    def setup_activity_selection_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab2)

        start_label = ctk.CTkLabel(left_column, text="Start Times (comma-separated):")
        start_label.pack(pady=5)
        self.start_entry = ctk.CTkEntry(left_column, width=300)
        self.start_entry.pack(pady=5)

        end_label = ctk.CTkLabel(left_column, text="End Times (comma-separated):")
        end_label.pack(pady=5)
        self.end_entry = ctk.CTkEntry(left_column, width=300)
        self.end_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_activity_selection)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_activity_selection)
        solve_button.pack(pady=10)

        self.activity_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.activity_result_label.pack(pady=10)

    def sample_activity_selection(self):
        self.start_entry.delete(0, "end")
        self.end_entry.delete(0, "end")
        self.start_entry.insert(0, "1,3,0,5,8,5")
        self.end_entry.insert(0, "2,4,6,7,9,9")

    def solve_activity_selection(self):
        try:
            start_times = list(map(int, self.start_entry.get().split(',')))
            end_times = list(map(int, self.end_entry.get().split(',')))

            if len(start_times) != len(end_times):
                self.activity_result_label.configure(text="Number of start and end times must be equal.", text_color="red")
                return

            result = activity_selection(start_times, end_times)
            self.activity_result_label.configure(text=f"Selected Activities: {result}", text_color="green")
        except ValueError:
            self.activity_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")
            
    
    def setup_huffman_coding_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab3)

        text_label = ctk.CTkLabel(left_column, text="Enter text:")
        text_label.pack(pady=5)
        self.text_entry = ctk.CTkEntry(left_column, width=300)
        self.text_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_huffman_coding)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Encode", command=self.solve_huffman_coding)
        solve_button.pack(pady=10)

        encoded_label = ctk.CTkLabel(left_column, text="Encoded text:")
        encoded_label.pack(pady=5)
        self.encoded_entry = ctk.CTkEntry(left_column, width=300)
        self.encoded_entry.pack(pady=5)

        decode_button = ctk.CTkButton(left_column, text="Decode", command=self.solve_huffman_decoding)
        decode_button.pack(pady=10)

        self.huffman_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.huffman_result_label.pack(pady=10)

    def sample_huffman_coding(self):
        self.text_entry.delete(0, "end")
        self.text_entry.insert(0, "hello world")

    def solve_huffman_coding(self):
        try:
            text = self.text_entry.get()
            if not text:
                self.huffman_result_label.configure(text="Input cannot be empty.", text_color="red")
                return

            codes, encoded_text, root = huffman_coding(text)
            self.encoded_entry.delete(0, "end")
            self.encoded_entry.insert(0, encoded_text)
            self.huffman_result_label.configure(text=f"Codes: {codes}\nEncoded Text: {encoded_text}", text_color="green")
        except Exception as e:
            self.huffman_result_label.configure(text=f"Error: {str(e)}", text_color="red")

    def solve_huffman_decoding(self):
        try:
            encoded_text = self.encoded_entry.get()
            if not encoded_text:
                self.huffman_result_label.configure(text="Encoded text cannot be empty.", text_color="red")
                return

            text = self.text_entry.get()
            _, _, root = huffman_coding(text)
            decoded_text = huffman_decoding(encoded_text, root)
            self.huffman_result_label.configure(text=f"Decoded Text: {decoded_text}", text_color="green")
        except Exception as e:
            self.huffman_result_label.configure(text=f"Error: {str(e)}", text_color="red")



    def setup_coin_change_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab4)

        coins_label = ctk.CTkLabel(left_column, text="Coin denominations (comma-separated):")
        coins_label.pack(pady=5)
        self.coins_entry = ctk.CTkEntry(left_column, width=300)
        self.coins_entry.pack(pady=5)

        amount_label = ctk.CTkLabel(left_column, text="Target amount:")
        amount_label.pack(pady=5)
        self.amount_entry = ctk.CTkEntry(left_column, width=300)
        self.amount_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_coin_change)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_coin_change)
        solve_button.pack(pady=10)

        self.coin_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.coin_result_label.pack(pady=10)

    def sample_coin_change(self):
        self.coins_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.coins_entry.insert(0, "1,2,5")
        self.amount_entry.insert(0, "11")

    def solve_coin_change(self):
        try:
            coins = list(map(int, self.coins_entry.get().split(',')))
            amount = int(self.amount_entry.get())

            result = coin_change_greedy(coins, amount)
            if not result:
                self.coin_result_label.configure(text="Cannot make the amount with the given coins.", text_color="red")
            else:
                self.coin_result_label.configure(text=f"Coins used: {result}", text_color="green")
        except ValueError:
            self.coin_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

    def setup_job_sequencing_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab5)

        jobs_label = ctk.CTkLabel(left_column, text="Jobs (ID, Deadline, Profit) e.g., 1,2,100:")
        jobs_label.pack(pady=5)
        self.jobs_entry = ctk.CTkEntry(left_column, width=300)
        self.jobs_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_job_sequencing)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_job_sequencing)
        solve_button.pack(pady=10)

        self.job_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.job_result_label.pack(pady=10)

    def sample_job_sequencing(self):
        self.jobs_entry.delete(0, "end")
        self.jobs_entry.insert(0, "1,2,100;2,1,19;3,2,27;4,1,25;5,3,15")

    def solve_job_sequencing(self):
        try:
            jobs_input = self.jobs_entry.get().strip()
            if not jobs_input:
                self.job_result_label.configure(text="Input cannot be empty.", text_color="red")
                return

            jobs = []
            for job_str in jobs_input.split(';'):
                job_data = list(map(int, job_str.split(',')))
                if len(job_data) != 3:
                    self.job_result_label.configure(text="Each job must have 3 values (ID, Deadline, Profit).", text_color="red")
                    return
                jobs.append(job_data)

            schedule, total_profit = job_sequencing(jobs)
            self.job_result_label.configure(text=f"Scheduled Jobs: {schedule}\nTotal Profit: {total_profit}", text_color="green")
        except ValueError:
            self.job_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

    def setup_prims_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab6)

        graph_label = ctk.CTkLabel(left_column, text="Graph (u,v,cost; u,v,cost; ...):")
        graph_label.pack(pady=5)
        self.graph_entry = ctk.CTkEntry(left_column, width=300)
        self.graph_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_prims)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_prims)
        solve_button.pack(pady=10)

        self.prims_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.prims_result_label.pack(pady=10)

    def sample_prims(self):
        self.graph_entry.delete(0, "end")
        self.graph_entry.insert(0, "0,1,2;1,2,3;2,3,4;3,4,5")

    def solve_prims(self):
        try:
            graph_input = self.graph_entry.get().strip()
            if not graph_input:
                self.prims_result_label.configure(text="Input cannot be empty.", text_color="red")
                return

            graph = defaultdict(list)
            for edge_str in graph_input.split(';'):
                u, v, cost = map(int, edge_str.split(','))
                graph[u].append((v, cost))
                graph[v].append((u, cost))

            mst = prim_mst(graph)
            self.prims_result_label.configure(text=f"MST: {mst}", text_color="green")
        except ValueError:
            self.prims_result_label.configure(text="Invalid input! Please enter edges in the format u,v,cost.", text_color="red")

    def setup_kruskals_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab7)

        graph_label = ctk.CTkLabel(left_column, text="Graph (u,v,cost; u,v,cost; ...):")
        graph_label.pack(pady=5)
        self.kruskal_graph_entry = ctk.CTkEntry(left_column, width=300)
        self.kruskal_graph_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_kruskals)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_kruskals)
        solve_button.pack(pady=10)

        self.kruskal_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.kruskal_result_label.pack(pady=10)

    def sample_kruskals(self):
        self.kruskal_graph_entry.delete(0, "end")
        self.kruskal_graph_entry.insert(0, "0,1,2;1,2,3;2,3,4;3,4,5")

    def solve_kruskals(self):
        try:
            graph_input = self.kruskal_graph_entry.get().strip()
            if not graph_input:
                self.kruskal_result_label.configure(text="Input cannot be empty.", text_color="red")
                return

            graph = defaultdict(list)
            for edge_str in graph_input.split(';'):
                u, v, cost = map(int, edge_str.split(','))
                graph[u].append((v, cost))
                graph[v].append((u, cost))

            mst = kruskal_mst(graph)
            self.kruskal_result_label.configure(text=f"MST: {mst}", text_color="green")
        except ValueError:
            self.kruskal_result_label.configure(text="Invalid input! Please enter edges in the format u,v,cost.", text_color="red")


    def setup_water_connection_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab9)

        pipes_label = ctk.CTkLabel(left_column, text="Pipes (house1,house2,diameter; ...):")
        pipes_label.pack(pady=5)
        self.pipes_entry = ctk.CTkEntry(left_column, width=300)
        self.pipes_entry.pack(pady=5)

        houses_label = ctk.CTkLabel(left_column, text="Houses (comma-separated):")
        houses_label.pack(pady=5)
        self.houses_entry = ctk.CTkEntry(left_column, width=300)
        self.houses_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_water_connection)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_water_connection)
        solve_button.pack(pady=10)

        self.water_connection_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.water_connection_result_label.pack(pady=10)

    def sample_water_connection(self):
        self.pipes_entry.delete(0, "end")
        self.houses_entry.delete(0, "end")
        self.pipes_entry.insert(0, "1,2,5;2,3,10;3,4,15")
        self.houses_entry.insert(0, "1,2,3,4")

    def solve_water_connection(self):
        try:
            pipes_input = self.pipes_entry.get().strip()
            houses_input = self.houses_entry.get().strip()

            if not pipes_input or not houses_input:
                self.water_connection_result_label.configure(text="Input cannot be empty.", text_color="red")
                return

            pipes = {}
            for pipe_str in pipes_input.split(';'):
                house1, house2, diameter = map(int, pipe_str.split(','))
                pipes[house1] = (house2, diameter)

            houses = list(map(int, houses_input.split(',')))
            connections = water_connection_problem(pipes, houses)
            self.water_connection_result_label.configure(text=f"Connections: {connections}", text_color="green")
        except ValueError:
            self.water_connection_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

    def setup_bracket_balancing_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab10)

        brackets_label = ctk.CTkLabel(left_column, text="Enter bracket sequence:")
        brackets_label.pack(pady=5)
        self.brackets_entry = ctk.CTkEntry(left_column, width=300)
        self.brackets_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_bracket_balancing)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_bracket_balancing)
        solve_button.pack(pady=10)

        self.bracket_balancing_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.bracket_balancing_result_label.pack(pady=10)

    def sample_bracket_balancing(self):
        self.brackets_entry.delete(0, "end")
        self.brackets_entry.insert(0, "[]][][")

    def solve_bracket_balancing(self):
        try:
            brackets = self.brackets_entry.get().strip()
            if not brackets:
                self.bracket_balancing_result_label.configure(text="Input cannot be empty.", text_color="red")
                return

            swaps = min_swaps_bracket_balancing(brackets)
            self.bracket_balancing_result_label.configure(text=f"Minimum swaps: {swaps}", text_color="green")
        except Exception as e:
            self.bracket_balancing_result_label.configure(text=f"Error: {str(e)}", text_color="red")

    def setup_fitting_shelves_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab11)

        wall_label = ctk.CTkLabel(left_column, text="Wall length:")
        wall_label.pack(pady=5)
        self.wall_entry = ctk.CTkEntry(left_column, width=300)
        self.wall_entry.pack(pady=5)

        shelf1_label = ctk.CTkLabel(left_column, text="Shelf 1 length:")
        shelf1_label.pack(pady=5)
        self.shelf1_entry = ctk.CTkEntry(left_column, width=300)
        self.shelf1_entry.pack(pady=5)

        shelf2_label = ctk.CTkLabel(left_column, text="Shelf 2 length:")
        shelf2_label.pack(pady=5)
        self.shelf2_entry = ctk.CTkEntry(left_column, width=300)
        self.shelf2_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_fitting_shelves)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_fitting_shelves)
        solve_button.pack(pady=10)

        self.fitting_shelves_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.fitting_shelves_result_label.pack(pady=10)

    def sample_fitting_shelves(self):
        self.wall_entry.delete(0, "end")
        self.shelf1_entry.delete(0, "end")
        self.shelf2_entry.delete(0, "end")
        self.wall_entry.insert(0, "24")
        self.shelf1_entry.insert(0, "5")
        self.shelf2_entry.insert(0, "3")

    def solve_fitting_shelves(self):
        try:
            wall_length = int(self.wall_entry.get())
            shelf1 = int(self.shelf1_entry.get())
            shelf2 = int(self.shelf2_entry.get())

            result = fitting_shelves(wall_length, shelf1, shelf2)
            self.fitting_shelves_result_label.configure(text=f"Optimal configuration: {result}", text_color="green")
        except ValueError:
            self.fitting_shelves_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

    def setup_mice_to_holes_tab(self):
        left_column, right_column = self.create_two_column_layout(self.tab12)

        mice_label = ctk.CTkLabel(left_column, text="Mice positions (comma-separated):")
        mice_label.pack(pady=5)
        self.mice_entry = ctk.CTkEntry(left_column, width=300)
        self.mice_entry.pack(pady=5)

        holes_label = ctk.CTkLabel(left_column, text="Holes positions (comma-separated):")
        holes_label.pack(pady=5)
        self.holes_entry = ctk.CTkEntry(left_column, width=300)
        self.holes_entry.pack(pady=5)

        sample_input_button = ctk.CTkButton(left_column, text="Sample Input", command=self.sample_mice_to_holes)
        sample_input_button.pack(pady=10)

        solve_button = ctk.CTkButton(left_column, text="Solve", command=self.solve_mice_to_holes)
        solve_button.pack(pady=10)

        self.mice_to_holes_result_label = ctk.CTkLabel(right_column, text="Result will appear here", text_color="white")
        self.mice_to_holes_result_label.pack(pady=10)

    def sample_mice_to_holes(self):
        self.mice_entry.delete(0, "end")
        self.holes_entry.delete(0, "end")
        self.mice_entry.insert(0, "4,2,0")
        self.holes_entry.insert(0, "1,3,5")

    def solve_mice_to_holes(self):
        try:
            mice = list(map(int, self.mice_entry.get().split(',')))
            holes = list(map(int, self.holes_entry.get().split(',')))

            if len(mice) != len(holes):
                self.mice_to_holes_result_label.configure(text="Number of mice and holes must be equal.", text_color="red")
                return

            max_distance = assign_mice_to_holes(mice, holes)
            self.mice_to_holes_result_label.configure(text=f"Maximum distance: {max_distance}", text_color="green")
        except ValueError:
            self.mice_to_holes_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")


if __name__ == "__main__":
    app = GreedyAlgorithmsGame()
    app.mainloop()