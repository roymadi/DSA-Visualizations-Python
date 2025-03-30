import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.root.geometry("500x600")
        self.grid = [[ctk.StringVar() for _ in range(9)] for _ in range(9)]
        self.create_widgets()

    def create_widgets(self):
        self.grid_frame = ctk.CTkFrame(self.root)
        self.grid_frame.pack(pady=20)

        for i in range(9):
            for j in range(9):
                entry = ctk.CTkEntry(
                    self.grid_frame,
                    textvariable=self.grid[i][j],
                    width=40,
                    height=40,
                    font=("Arial", 16),
                    justify="center",
                )
                entry.grid(row=i, column=j, padx=2, pady=2)

        self.button_frame = ctk.CTkFrame(self.root)
        self.button_frame.pack(pady=10)

        self.solve_button = ctk.CTkButton(
            self.button_frame, text="Solve", command=self.solve, font=("Arial", 14)
        )
        self.solve_button.pack(side=ctk.LEFT, padx=10)

        self.clear_button = ctk.CTkButton(
            self.button_frame, text="Clear", command=self.clear, font=("Arial", 14)
        )
        self.clear_button.pack(side=ctk.LEFT, padx=10)

        self.generate_button = ctk.CTkButton(
            self.button_frame, text="Generate", command=self.generate_sudoku, font=("Arial", 14)
        )
        self.generate_button.pack(side=ctk.LEFT, padx=10)

        self.status_label = ctk.CTkLabel(self.root, text="", font=("Arial", 14))
        self.status_label.pack(pady=10)

    def solve(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                value = self.grid[i][j].get()
                if value.isdigit() and 1 <= int(value) <= 9:
                    board[i][j] = int(value)
                else:
                    board[i][j] = 0

        if not self.is_valid_board(board):
            self.status_label.configure(text="Invalid Sudoku Puzzle!", text_color="red")
            return

        if self.solve_sudoku(board):
            for i in range(9):
                for j in range(9):
                    self.grid[i][j].set(str(board[i][j]))
            self.status_label.configure(text="Solved!", text_color="green")
        else:
            self.status_label.configure(text="No Solution Exists!", text_color="red")

    def clear(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].set("")
        self.status_label.configure(text="", text_color="black")

    def generate_sudoku(self):
        board = self.generate_valid_sudoku()
        for i in range(9):
            for j in range(9):
                self.grid[i][j].set(str(board[i][j]) if board[i][j] != 0 else "")
        self.status_label.configure(text="New Sudoku Generated!", text_color="blue")

    def generate_valid_sudoku(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku(board) 

        empty_cells = random.randint(40, 50)  
        for _ in range(empty_cells):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            board[row][col] = 0

        return board

    def is_valid_board(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    if not self.is_valid(board, i, j, board[i][j]):
                        return False
        return True

    def solve_sudoku(self, board):
        empty = self.find_empty(board)
        if not empty:
            return True  
        row, col = empty

        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for num in numbers:
            if self.is_valid(board, row, col, num):
                board[row][col] = num

                if self.solve_sudoku(board):
                    return True

                board[row][col] = 0

        return False 

    def find_empty(self, board):

        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, board, row, col, num):
       
        for i in range(9):
            if board[row][i] == num and i != col: 
                return False
            if board[i][col] == num and i != row:  
                return False


        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[box_row + i][box_col + j] == num and (box_row + i != row or box_col + j != col):
                    return False

        return True



if __name__ == "__main__":
    root = ctk.CTk()
    app = SudokuSolver(root)
    root.mainloop()