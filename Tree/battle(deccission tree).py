import tkinter as tk
from tkinter import ttk
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

# Features: [Player Health, Enemy Health, Distance to Enemy]
# Labels: 0 = Retreat, 1 = Defend, 2 = Attack
X = np.array([
    [10, 50, 100],  
    [80, 20, 50],  
    [50, 50, 10],  
    [30, 70, 80], 
    [90, 10, 20], 
    [90, 70, 70], 
    [70, 170, 70], 
    [155, 170, 220],
    [190, 170, 70], 
    [590, 470, 20],  
    [160, 160, 170], 
    [20, 80, 90],   
    [60, 40, 30],   
    [100, 100, 100], 
    [200, 50, 10], 
    [50, 200, 150], 
    [10, 10, 10],  
    [150, 150, 50], 
    [80, 120, 100], 
    [40, 60, 20],   
    [200, 200, 200],
    [30, 90, 60],   
    [70, 30, 40],  
    [100, 50, 80],  
    [50, 100, 120], 
])

y = np.array([0, 2, 1, 0, 2, 2, 0, 0, 2, 2, 1, 0, 1, 1, 2, 0, 1, 1, 1, 1, 0, 0, 2, 1, 0])


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)


y_pred = clf.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")


def visualize_tree():
    plt.figure(figsize=(10, 6))
    tree.plot_tree(clf, filled=True, feature_names=["Player Health", "Enemy Health", "Distance"], class_names=["Retreat", "Defend", "Attack"])
    plt.show()


class DecisionTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Decision Maker")
        self.root.geometry("400x300")
        self.root.configure(bg="#2E3440")


        self.style = ttk.Style()
        self.style.configure("TLabel", background="#2E3440", foreground="#D8DEE9", font=("Arial", 12))
        self.style.configure("TButton", background="#4C566A", foreground="black", font=("Arial", 12))  # Set text color to black
        self.style.configure("TEntry", font=("Arial", 12))


        ttk.Label(root, text="Player Health:").grid(row=0, column=0, padx=10, pady=10)
        self.player_health = ttk.Entry(root)
        self.player_health.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(root, text="Enemy Health:").grid(row=1, column=0, padx=10, pady=10)
        self.enemy_health = ttk.Entry(root)
        self.enemy_health.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(root, text="Distance to Enemy:").grid(row=2, column=0, padx=10, pady=10)
        self.distance = ttk.Entry(root)
        self.distance.grid(row=2, column=1, padx=10, pady=10)

        self.decision_button = ttk.Button(root, text="Make Decision", command=self.make_decision)
        self.decision_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.result_label = ttk.Label(root, text="Decision: ", font=("Arial", 14, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)


        self.visualize_button = ttk.Button(root, text="Visualize Decision Tree", command=visualize_tree)
        self.visualize_button.grid(row=5, column=0, columnspan=2, pady=10)

    def make_decision(self):
        try:
            player_health = float(self.player_health.get())
            enemy_health = float(self.enemy_health.get())
            distance = float(self.distance.get())

            decision = clf.predict([[player_health, enemy_health, distance]])

            decisions = ["Retreat", "Defend", "Attack"]
            result = decisions[decision[0]]

            self.result_label.config(text=f"Decision: {result}")
        except ValueError:
            self.result_label.config(text="Invalid input! Please enter numbers.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DecisionTreeApp(root)
    root.mainloop()