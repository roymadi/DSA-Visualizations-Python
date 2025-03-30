import tkinter as tk
from tkinter import ttk, messagebox
import time

class BitwiseBlitz:
    def __init__(self, root):
        self.root = root
        self.root.title("Bitwise Blitz")
        self.root.geometry("500x400")
        self.root.configure(bg="#2c3e50")

        self.level = 1
        self.score = 0
        self.start_time = None

        self.style = ttk.Style()
        self.style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Helvetica", 14))
        self.style.configure("TButton", background="#3498db", foreground="black", font=("Helvetica", 14))

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.root, text="Welcome to Bitwise Blitz!", style="TLabel")
        self.label.pack(pady=20)

        self.question_label = ttk.Label(self.root, text="", style="TLabel")
        self.question_label.pack(pady=10)

        self.answer_entry = ttk.Entry(self.root, font=("Helvetica", 14))
        self.answer_entry.pack(pady=10)

        self.submit_button = ttk.Button(self.root, text="Submit", command=self.check_answer, style="TButton")
        self.submit_button.pack(pady=10)

        self.hint_button = ttk.Button(self.root, text="Hint", command=self.show_hint, style="TButton")
        self.hint_button.pack(pady=10)

        self.timer_label = ttk.Label(self.root, text="Time: 0s", style="TLabel")
        self.timer_label.pack(pady=10)

        self.next_level()

    def next_level(self):
        self.start_time = time.time()
        self.update_timer()

        questions = [
            ("What is 5 & 3?", 5 & 3, "AND operation: Compares each bit, returns 1 if both bits are 1."),
            ("What is 5 | 3?", 5 | 3, "OR operation: Compares each bit, returns 1 if either bit is 1."),
            ("What is 5 ^ 3?", 5 ^ 3, "XOR operation: Compares each bit, returns 1 if bits are different."),
            ("What is ~3?", ~3, "NOT operation: Inverts all the bits."),
            ("What is 5 << 1?", 5 << 1, "Left Shift: Shifts bits to the left, fills with 0 on the right."),
            ("What is 5 >> 1?", 5 >> 1, "Right Shift: Shifts bits to the right, fills with 0 on the left."),
            ("What is 5 & ~3?", 5 & ~3, "Combination: AND operation with NOT."),
            ("What is 5 | (3 ^ 2)?", 5 | (3 ^ 2), "Combination: OR operation with XOR.")
        ]

        if self.level <= len(questions):
            question, answer, hint = questions[self.level - 1]
            self.question_label.config(text=question)
            self.correct_answer = answer
            self.hint = hint
            self.answer_entry.delete(0, tk.END)
            self.fade_in()
            print(f"Level {self.level}: {question} Answer: {answer}")
        else:
            self.show_final_score()

    def check_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.correct_answer:
                self.score += 1
                messagebox.showinfo("Correct", "Great job!")
                self.level += 1
                self.fade_out(self.next_level)
            else:
                skip = messagebox.askyesno("Incorrect", "Wrong answer. Do you want to skip this question?")
                if skip:
                    self.level += 1
                    self.fade_out(self.next_level)
                else:
                    messagebox.showinfo("Try Again", "Give it another shot!")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter an integer.")

    def show_hint(self):
        messagebox.showinfo("Hint", self.hint)

    def fade_in(self):
        alpha = 0
        self.question_label.lift()
        self.question_label.configure(foreground=f'#{int(255*alpha):02x}{int(255*alpha):02x}{int(255*alpha):02x}')
        self.root.after(50, self.fade_in_step, alpha)

    def fade_in_step(self, alpha):
        if alpha < 1:
            alpha += 0.1
            self.question_label.configure(foreground=f'#{int(255*alpha):02x}{int(255*alpha):02x}{int(255*alpha):02x}')
            self.root.after(50, self.fade_in_step, alpha)

    def fade_out(self, callback):
        alpha = 1
        self.question_label.lift()
        self.question_label.configure(foreground=f'#{int(255*alpha):02x}{int(255*alpha):02x}{int(255*alpha):02x}')
        self.root.after(50, self.fade_out_step, alpha, callback)

    def fade_out_step(self, alpha, callback):
        if alpha > 0:
            alpha = max(0, alpha - 0.1)
            self.question_label.configure(foreground=f'#{int(255*alpha):02x}{int(255*alpha):02x}{int(255*alpha):02x}')
            self.root.after(50, self.fade_out_step, alpha, callback)
        else:
            callback()

    def update_timer(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.root.after(1000, self.update_timer)

    def show_final_score(self):
        messagebox.showinfo("Game Over", f"Congratulations! You completed all levels.\nYour final score: {self.score}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = BitwiseBlitz(root)
    root.mainloop()