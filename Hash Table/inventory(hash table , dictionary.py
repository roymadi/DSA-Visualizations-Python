import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

class InventorySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Player Inventory System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2c3e50")
        
        self.inventory = {}
        
        self.data_file = "inventory_data.json"
        self.load_data()
        
        self.categories = ["Weapons", "Armor", "Potions", "Materials", "Artifacts", "Miscellaneous"]
        
        self.create_widgets()
        
        self.refresh_inventory_view()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    self.inventory = json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Corrupted inventory data file. Starting with empty inventory.")
                self.inventory = {}
    
    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.inventory, file, indent=4)
    
    def create_widgets(self):
        self.left_frame = tk.Frame(self.root, bg="#34495e", width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.right_frame = tk.Frame(self.root, bg="#34495e")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            self.left_frame, 
            text="Player Inventory", 
            font=("Helvetica", 18, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Add buttons for inventory management
        self.create_button("Add Item", self.add_item_dialog)
        self.create_button("Remove Item", self.remove_item_dialog)
        self.create_button("Edit Item", self.edit_item_dialog)
        self.create_button("Search", self.search_dialog)
        
        # Category filter
        filter_frame = tk.Frame(self.left_frame, bg="#34495e")
        filter_frame.pack(fill=tk.X, pady=10, padx=10)
        
        filter_label = tk.Label(
            filter_frame, 
            text="Filter by Category:", 
            font=("Helvetica", 12),
            bg="#34495e",
            fg="white"
        )
        filter_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.category_var = tk.StringVar()
        self.category_var.set("All")
        
        category_combobox = ttk.Combobox(
            filter_frame, 
            textvariable=self.category_var, 
            values=["All"] + self.categories,
            state="readonly",
            font=("Helvetica", 12)
        )
        category_combobox.pack(fill=tk.X, pady=5)
        category_combobox.bind("<<ComboboxSelected>>", self.filter_by_category)
        
        # Stats frame
        stats_frame = tk.Frame(self.left_frame, bg="#2c3e50", padx=10, pady=10)
        stats_frame.pack(fill=tk.X, pady=10, padx=10)
        
        stats_label = tk.Label(
            stats_frame, 
            text="Inventory Stats", 
            font=("Helvetica", 14, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        stats_label.pack(anchor=tk.W, pady=5)
        
        self.total_items_label = tk.Label(
            stats_frame, 
            text="Total Items: 0", 
            font=("Helvetica", 12),
            bg="#2c3e50",
            fg="white",
            anchor=tk.W
        )
        self.total_items_label.pack(fill=tk.X, pady=2)
        
        self.total_value_label = tk.Label(
            stats_frame, 
            text="Total Value: 0", 
            font=("Helvetica", 12),
            bg="#2c3e50",
            fg="white",
            anchor=tk.W
        )
        self.total_value_label.pack(fill=tk.X, pady=2)
        
        # Create inventory view (Treeview)
        self.create_inventory_view()
    
    def create_button(self, text, command):
        """Helper function to create styled buttons"""
        button = tk.Button(
            self.left_frame,
            text=text,
            font=("Helvetica", 12),
            bg="#3498db",
            fg="white",
            pady=8,
            borderwidth=0,
            command=command
        )
        button.pack(fill=tk.X, padx=20, pady=5)
        
        button.bind("<Enter>", lambda e, btn=button: btn.config(bg="#2980b9"))
        button.bind("<Leave>", lambda e, btn=button: btn.config(bg="#3498db"))
    
    def create_inventory_view(self):
        tree_frame = tk.Frame(self.right_frame, bg="#34495e")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        heading_label = tk.Label(
            tree_frame, 
            text="Inventory Items", 
            font=("Helvetica", 16, "bold"),
            bg="#34495e",
            fg="white"
        )
        heading_label.pack(pady=(0, 10), anchor=tk.W)
        
        y_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        x_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                        background="#ecf0f1",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#ecf0f1",
                        font=("Helvetica", 10))
        style.map('Treeview', background=[('selected', '#3498db')])
        
        self.inventory_tree = ttk.Treeview(
            tree_frame, 
            columns=("ID", "Name", "Category", "Quantity", "Value", "Description"),
            show="headings",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set
        )
        
        y_scrollbar.config(command=self.inventory_tree.yview)
        x_scrollbar.config(command=self.inventory_tree.xview)
        
        self.inventory_tree.heading("ID", text="ID")
        self.inventory_tree.heading("Name", text="Name")
        self.inventory_tree.heading("Category", text="Category")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.heading("Value", text="Value")
        self.inventory_tree.heading("Description", text="Description")
        
        self.inventory_tree.column("ID", width=50, anchor=tk.CENTER)
        self.inventory_tree.column("Name", width=150, anchor=tk.W)
        self.inventory_tree.column("Category", width=100, anchor=tk.W)
        self.inventory_tree.column("Quantity", width=70, anchor=tk.CENTER)
        self.inventory_tree.column("Value", width=70, anchor=tk.CENTER)
        self.inventory_tree.column("Description", width=300, anchor=tk.W)
        
        self.inventory_tree.pack(fill=tk.BOTH, expand=True)
        
        self.inventory_tree.bind("<Double-1>", self.show_item_details)
    
    def refresh_inventory_view(self, filter_category=None):
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        total_items = 0
        total_value = 0
        
        for item_id, item_data in self.inventory.items():  
            if filter_category and filter_category != "All" and item_data["category"] != filter_category:
                continue
                
            quantity = item_data.get("quantity", 0)
            value = item_data.get("value", 0)
            
            total_items += quantity
            total_value += quantity * value
            
            self.inventory_tree.insert(
                "", 
                tk.END, 
                values=(
                    item_id,
                    item_data.get("name", "Unknown"),
                    item_data.get("category", "Miscellaneous"),
                    quantity,
                    value,
                    item_data.get("description", "")
                )
            )
       
        self.total_items_label.config(text=f"Total Items: {total_items}")
        self.total_value_label.config(text=f"Total Value: {total_value}")
    
    def add_item_dialog(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Item")
        add_window.geometry("400x450")
        add_window.configure(bg="#34495e")
        add_window.transient(self.root)
        add_window.grab_set()
        
        title_label = tk.Label(
            add_window, 
            text="Add New Item", 
            font=("Helvetica", 16, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack(pady=15)
        
        form_frame = tk.Frame(add_window, bg="#34495e", padx=20, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text="Item ID:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        item_id_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        item_id_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        tk.Label(form_frame, text="Name:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        name_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        name_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        tk.Label(form_frame, text="Category:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(form_frame, textvariable=category_var, values=self.categories, state="readonly", font=("Helvetica", 12))
        category_combobox.grid(row=2, column=1, sticky=tk.EW, pady=5)
        category_var.set(self.categories[0])
        
        tk.Label(form_frame, text="Quantity:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        quantity_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        quantity_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
        quantity_entry.insert(0, "1")
        
        tk.Label(form_frame, text="Value:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=4, column=0, sticky=tk.W, pady=5)
        value_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        value_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)
        value_entry.insert(0, "0")
        
        tk.Label(form_frame, text="Description:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=5, column=0, sticky=tk.NW, pady=5)
        description_text = tk.Text(form_frame, height=4, width=25, font=("Helvetica", 12))
        description_text.grid(row=5, column=1, sticky=tk.EW, pady=5)
        
        form_frame.columnconfigure(1, weight=1)
        
        def add_item():
            try:
                item_id = item_id_entry.get().strip()
                name = name_entry.get().strip()
                category = category_var.get()
                quantity = int(quantity_entry.get())
                value = float(value_entry.get())
                description = description_text.get("1.0", tk.END).strip()
                
                if not item_id or not name:
                    messagebox.showerror("Error", "Item ID and Name are required!")
                    return
                
                if item_id in self.inventory:
                    messagebox.showerror("Error", f"Item ID '{item_id}' already exists!")
                    return
                
                self.inventory[item_id] = {
                    "name": name,
                    "category": category,
                    "quantity": quantity,
                    "value": value,
                    "description": description
                }
                
                self.save_data()
                self.refresh_inventory_view(self.category_var.get())
                
                messagebox.showinfo("Success", f"Item '{name}' added to inventory!")
                add_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", "Quantity and Value must be numbers!")
        
        button_frame = tk.Frame(add_window, bg="#34495e", pady=10)
        button_frame.pack(fill=tk.X)
        
        add_button = tk.Button(
            button_frame,
            text="Add Item",
            font=("Helvetica", 12),
            bg="#2ecc71",
            fg="white",
            pady=8,
            command=add_item
        )
        add_button.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Helvetica", 12),
            bg="#e74c3c",
            fg="white",
            pady=8,
            command=add_window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
    
    def remove_item_dialog(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to remove!")
            return
        
        item_values = self.inventory_tree.item(selected_item[0], "values")
        item_id = item_values[0]
        item_name = item_values[1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove '{item_name}'?"):
            if item_id in self.inventory:  # Added check to ensure item exists
                del self.inventory[item_id]
                self.save_data()
                self.refresh_inventory_view(self.category_var.get())
                messagebox.showinfo("Success", f"Item '{item_name}' removed from inventory!")
            else:
                messagebox.showerror("Error", f"Item '{item_name}' not found in inventory!")
    
    def edit_item_dialog(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to edit!")
            return
        
        item_values = self.inventory_tree.item(selected_item[0], "values")
        item_id = item_values[0]
        
        if item_id not in self.inventory:
            messagebox.showerror("Error", "Item not found in inventory!")
            return
        
        item_data = self.inventory[item_id]
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Item")
        edit_window.geometry("400x450")
        edit_window.configure(bg="#34495e")
        edit_window.transient(self.root)
        edit_window.grab_set()
        
        title_label = tk.Label(
            edit_window, 
            text="Edit Item", 
            font=("Helvetica", 16, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack(pady=15)
        
        form_frame = tk.Frame(edit_window, bg="#34495e", padx=20, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(form_frame, text="Item ID:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Label(form_frame, text=item_id, bg="#34495e", fg="lightgray", font=("Helvetica", 12)).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        tk.Label(form_frame, text="Name:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        name_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        name_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)
        name_entry.insert(0, item_data.get("name", ""))
        
        tk.Label(form_frame, text="Category:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        category_var = tk.StringVar()
        category_combobox = ttk.Combobox(form_frame, textvariable=category_var, values=self.categories, state="readonly", font=("Helvetica", 12))
        category_combobox.grid(row=2, column=1, sticky=tk.EW, pady=5)
        category_var.set(item_data.get("category", self.categories[0]))
        
        tk.Label(form_frame, text="Quantity:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        quantity_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        quantity_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
        quantity_entry.insert(0, str(item_data.get("quantity", 1)))
        
        tk.Label(form_frame, text="Value:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=4, column=0, sticky=tk.W, pady=5)
        value_entry = tk.Entry(form_frame, font=("Helvetica", 12))
        value_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)
        value_entry.insert(0, str(item_data.get("value", 0)))
        
        tk.Label(form_frame, text="Description:", bg="#34495e", fg="white", font=("Helvetica", 12)).grid(row=5, column=0, sticky=tk.NW, pady=5)
        description_text = tk.Text(form_frame, height=4, width=25, font=("Helvetica", 12))
        description_text.grid(row=5, column=1, sticky=tk.EW, pady=5)
        description_text.insert("1.0", item_data.get("description", ""))
        
        form_frame.columnconfigure(1, weight=1)
        
        def update_item():
            try:
                name = name_entry.get().strip()
                category = category_var.get()
                quantity = int(quantity_entry.get())
                value = float(value_entry.get())
                description = description_text.get("1.0", tk.END).strip()
                
                if not name:
                    messagebox.showerror("Error", "Item Name is required!")
                    return
                
                self.inventory[item_id] = {
                    "name": name,
                    "category": category,
                    "quantity": quantity,
                    "value": value,
                    "description": description
                }
                
                self.save_data()
                self.refresh_inventory_view(self.category_var.get())
                
                messagebox.showinfo("Success", f"Item '{name}' updated!")
                edit_window.destroy()
                
            except ValueError as e:
                messagebox.showerror("Error", "Quantity and Value must be numbers!")
        
        button_frame = tk.Frame(edit_window, bg="#34495e", pady=10)
        button_frame.pack(fill=tk.X)
        
        update_button = tk.Button(
            button_frame,
            text="Update Item",
            font=("Helvetica", 12),
            bg="#2ecc71",
            fg="white",
            pady=8,
            command=update_item
        )
        update_button.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Helvetica", 12),
            bg="#e74c3c",
            fg="white",
            pady=8,
            command=edit_window.destroy
        )
        cancel_button.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)
    
    def search_dialog(self):
        search_term = simpledialog.askstring("Search", "Enter search term:", parent=self.root)
        if not search_term:
            return
        
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        found = False
        for item_id, item_data in self.inventory.items(): 
            if (search_term.lower() in item_id.lower() or 
                search_term.lower() in item_data.get("name", "").lower() or 
                search_term.lower() in item_data.get("description", "").lower()):
                
                self.inventory_tree.insert(
                    "", 
                    tk.END, 
                    values=(
                        item_id,
                        item_data.get("name", "Unknown"),
                        item_data.get("category", "Miscellaneous"),
                        item_data.get("quantity", 0),
                        item_data.get("value", 0),
                        item_data.get("description", "")
                    )
                )
                found = True
        
        if not found:
            messagebox.showinfo("Search Results", "No items found matching your search.")
            self.refresh_inventory_view(self.category_var.get())
    
    def filter_by_category(self, event=None):
        selected_category = self.category_var.get()
        self.refresh_inventory_view(selected_category)
    
    def show_item_details(self, event):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            return
        
        item_values = self.inventory_tree.item(selected_item[0], "values")
        item_id = item_values[0]
        
        if item_id not in self.inventory:
            return
        
        item_data = self.inventory[item_id]
        
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"Item Details: {item_data.get('name', 'Unknown')}")
        detail_window.geometry("500x400")
        detail_window.configure(bg="#34495e")
        detail_window.transient(self.root)
        
        title_label = tk.Label(
            detail_window, 
            text=f"Item Details: {item_data.get('name', 'Unknown')}", 
            font=("Helvetica", 16, "bold"),
            bg="#34495e",
            fg="white"
        )
        title_label.pack(pady=15)
        
        details_frame = tk.Frame(detail_window, bg="#2c3e50", padx=20, pady=20)
        details_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        detail_labels = [
            ("Item ID", item_id),
            ("Name", item_data.get("name", "Unknown")),
            ("Category", item_data.get("category", "Miscellaneous")),
            ("Quantity", str(item_data.get("quantity", 0))),
            ("Value (each)", str(item_data.get("value", 0))),
            ("Total Value", str(item_data.get("quantity", 0) * item_data.get("value", 0))),
            ("Description", item_data.get("description", "No description available."))
        ]
        
        for i, (label, value) in enumerate(detail_labels):
            tk.Label(
                details_frame, 
                text=label + ":", 
                font=("Helvetica", 12, "bold"),
                bg="#2c3e50",
                fg="#3498db",
                anchor=tk.W
            ).grid(row=i, column=0, sticky=tk.W, pady=5)
            
            if label == "Description":
                desc_text = tk.Text(details_frame, height=4, width=30, font=("Helvetica", 12), wrap=tk.WORD)
                desc_text.grid(row=i, column=1, sticky=tk.EW, pady=5)
                desc_text.insert("1.0", value)
                desc_text.config(state=tk.DISABLED, bg="#34495e", fg="white")
            else:
                tk.Label(
                    details_frame, 
                    text=value, 
                    font=("Helvetica", 12),
                    bg="#2c3e50",
                    fg="white",
                    anchor=tk.W
                ).grid(row=i, column=1, sticky=tk.W, pady=5)
        
        details_frame.columnconfigure(1, weight=1)
        
        close_button = tk.Button(
            detail_window,
            text="Close",
            font=("Helvetica", 12),
            bg="#3498db",
            fg="white",
            pady=8,
            command=detail_window.destroy
        )
        close_button.pack(pady=15)

def main():
    root = tk.Tk()
    app = InventorySystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()