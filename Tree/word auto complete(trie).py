import tkinter as tk
from tkinter import ttk, scrolledtext
import string
import os

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += 1
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def get_all_suggestions(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        suggestions = []
        self._dfs(node, prefix, suggestions)
        return sorted(suggestions, key=lambda x: (-x[1], x[0]))  
    
    def _dfs(self, node, prefix, suggestions):
        if node.is_end_of_word:
            suggestions.append((prefix, node.frequency))
        
        for char, child_node in node.children.items():
            self._dfs(child_node, prefix + char, suggestions)


class AutoCompleteApp:
    FILE_PATH = "words.txt"

    def __init__(self, root):
        self.root = root
        self.root.title("Word Game Auto-Complete")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        self.trie = Trie()
        self.load_dictionary()
        
        self.create_widgets()
        
    def load_dictionary(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as file:
                for word in file:
                    self.trie.insert(word.strip().lower())

    def save_word(self, word):
        with open(self.FILE_PATH, "a") as file:
            file.write(word + "\n")
    
    def create_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TButton", background="#4a7abc", foreground="white", font=("Helvetica", 12))
        style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 12))
        style.configure("Treeview", font=("Helvetica", 12))
        
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
       
        title_label = ttk.Label(main_frame, text="Word Game Auto-Complete", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=(0, 20))
        
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        input_label = ttk.Label(input_frame, text="Enter word prefix:")
        input_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var, font=("Helvetica", 12), width=30)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind("<KeyRelease>", self.update_suggestions)
        
        suggestions_frame = ttk.Frame(main_frame)
        suggestions_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        suggestions_label = ttk.Label(suggestions_frame, text="Suggestions:")
        suggestions_label.pack(anchor=tk.W, pady=(0, 5))
        
        columns = ("Word", "Frequency")
        self.suggestions_tree = ttk.Treeview(suggestions_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.suggestions_tree.heading(col, text=col)
            self.suggestions_tree.column(col, width=100)
        
        self.suggestions_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(suggestions_frame, orient=tk.VERTICAL, command=self.suggestions_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.suggestions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.suggestions_tree.bind("<<TreeviewSelect>>", self.on_suggestion_select)
        
        game_frame = ttk.Frame(main_frame)
        game_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        game_label = ttk.Label(game_frame, text="Game Area:")
        game_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.game_text = scrolledtext.ScrolledText(game_frame, wrap=tk.WORD, width=40, height=5, font=("Helvetica", 12))
        self.game_text.pack(fill=tk.BOTH, expand=True)
        
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        clear_button = ttk.Button(buttons_frame, text="Clear", command=self.clear_all)
        clear_button.pack(side=tk.RIGHT, padx=5)
        
        add_word_button = ttk.Button(buttons_frame, text="Add Word to Dictionary", command=self.add_word)
        add_word_button.pack(side=tk.RIGHT, padx=5)
        
        insert_button = ttk.Button(buttons_frame, text="Insert Selected Word", command=self.insert_selected_word)
        insert_button.pack(side=tk.RIGHT, padx=5)
    
    def update_suggestions(self, event=None):
        for item in self.suggestions_tree.get_children():
            self.suggestions_tree.delete(item)
        
        prefix = self.input_var.get().lower()
        if prefix:
            suggestions = self.trie.get_all_suggestions(prefix)
            for word, freq in suggestions:
                self.suggestions_tree.insert("", tk.END, values=(word, freq))
    
    def on_suggestion_select(self, event=None):
        selected_items = self.suggestions_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            word = self.suggestions_tree.item(selected_item, "values")[0]
            self.input_var.set(word)
    
    def insert_selected_word(self):
        selected_items = self.suggestions_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            word = self.suggestions_tree.item(selected_item, "values")[0]
            self.game_text.insert(tk.INSERT, word + " ")
            self.input_var.set("")
            self.update_suggestions()
            # Increase word frequency
            self.trie.insert(word)
    
    def add_word(self):
        word = self.input_var.get().lower()
        if word and all(c in string.ascii_lowercase for c in word):
            if not self.trie.search(word):  
                self.trie.insert(word)
                self.save_word(word) 
                self.game_text.insert(tk.END, f"Added '{word}' to dictionary\n")
                self.update_suggestions()
            self.input_var.set("")
    
    def clear_all(self):
        self.input_var.set("")
        self.game_text.delete(1.0, tk.END)
        self.update_suggestions()


if __name__ == "__main__":
    root = tk.Tk()
    app = AutoCompleteApp(root)
    root.mainloop()
