import customtkinter as ctk


def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]

def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]

def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

def lis(sequence):
    n = len(sequence)
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if sequence[i] > sequence[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

def mcm(dims):
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]

def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[m][n]

def longest_palindromic_subsequence(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]

def subset_sum(nums, target):
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True

    for i in range(1, n + 1):
        for j in range(target + 1):
            if nums[i - 1] <= j:
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - nums[i - 1]]
            else:
                dp[i][j] = dp[i - 1][j]

    return dp[n][target]

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


def solve_coin_change():
    try:
        coins = list(map(int, coin_entry.get().split(',')))
        amount = int(amount_entry.get())
        result = coin_change(coins, amount)

        if result == -1:
            coin_result_label.configure(text="It's not possible to make the amount with the given coins.", text_color="red")
        else:
            coin_result_label.configure(text=f"Minimum coins needed: {result}", text_color="green")
    except ValueError:
        coin_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

def solve_knapsack():
    try:
        weights = list(map(int, weights_entry.get().split(',')))
        values = list(map(int, values_entry.get().split(',')))
        capacity = int(capacity_entry.get())

        if len(weights) != len(values):
            knapsack_result_label.configure(text="Number of weights and values must be equal.", text_color="red")
            return

        result = knapsack(weights, values, capacity)
        knapsack_result_label.configure(text=f"Maximum value: {result}", text_color="green")
    except ValueError:
        knapsack_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

def solve_lcs():
    try:
        s1 = s1_entry.get()
        s2 = s2_entry.get()
        result = lcs(s1, s2)
        lcs_result_label.configure(text=f"Length of LCS: {result}", text_color="green")
    except Exception:
        lcs_result_label.configure(text="Invalid input!", text_color="red")

def solve_fibonacci():
    try:
        n = int(fibonacci_entry.get())
        result = fibonacci(n)
        fibonacci_result_label.configure(text=f"Fibonacci({n}) = {result}", text_color="green")
    except ValueError:
        fibonacci_result_label.configure(text="Invalid input! Please enter a number.", text_color="red")

def solve_lis():
    try:
        sequence = list(map(int, lis_entry.get().split(',')))
        result = lis(sequence)
        lis_result_label.configure(text=f"Length of LIS: {result}", text_color="green")
    except ValueError:
        lis_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

def solve_mcm():
    try:
        dims = list(map(int, mcm_entry.get().split(',')))
        result = mcm(dims)
        mcm_result_label.configure(text=f"Minimum cost: {result}", text_color="green")
    except ValueError:
        mcm_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

def solve_edit_distance():
    try:
        s1 = edit_s1_entry.get()
        s2 = edit_s2_entry.get()
        result = edit_distance(s1, s2)
        edit_result_label.configure(text=f"Edit Distance: {result}", text_color="green")
    except Exception:
        edit_result_label.configure(text="Invalid input!", text_color="red")

def solve_lps():
    try:
        s = lps_entry.get()
        result = longest_palindromic_subsequence(s)
        lps_result_label.configure(text=f"Length of LPS: {result}", text_color="green")
    except Exception:
        lps_result_label.configure(text="Invalid input!", text_color="red")

def solve_subset_sum():
    try:
        nums = list(map(int, subset_sum_entry.get().split(',')))
        target = int(subset_target_entry.get())
        result = subset_sum(nums, target)
        subset_sum_result_label.configure(text=f"Subset with sum {target} exists: {result}", text_color="green")
    except ValueError:
        subset_sum_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")

def solve_fractional_knapsack():
    try:
        weights = list(map(int, fractional_weights_entry.get().split(',')))
        values = list(map(int, fractional_values_entry.get().split(',')))
        capacity = int(fractional_capacity_entry.get())

        if len(weights) != len(values):
            fractional_result_label.configure(text="Number of weights and values must be equal.", text_color="red")
            return

        result = fractional_knapsack(weights, values, capacity)
        fractional_result_label.configure(text=f"Maximum value: {result:.2f}", text_color="green")
    except ValueError:
        fractional_result_label.configure(text="Invalid input! Please enter numbers only.", text_color="red")


app = ctk.CTk()
app.title("Puzzle Solver")
app.geometry("1000x800")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


tabview = ctk.CTkTabview(app)
tabview.pack(pady=10, padx=10, fill="both", expand=True)


tab1 = tabview.add("Coin Change")
tab2 = tabview.add("0/1 Knapsack")
tab3 = tabview.add("LCS")
tab4 = tabview.add("Fibonacci")
tab5 = tabview.add("LIS")
tab6 = tabview.add("MCM")
tab7 = tabview.add("Edit Distance")
tab8 = tabview.add("LPS")
tab9 = tabview.add("Subset Sum")
tab10 = tabview.add("Fractional Knapsack")


coin_label = ctk.CTkLabel(tab1, text="Enter coin denominations (comma-separated):", font=("Arial", 14))
coin_label.pack(pady=5)

coin_entry = ctk.CTkEntry(tab1, width=300, font=("Arial", 14))
coin_entry.pack(pady=5)

amount_label = ctk.CTkLabel(tab1, text="Enter target amount:", font=("Arial", 14))
amount_label.pack(pady=5)

amount_entry = ctk.CTkEntry(tab1, width=300, font=("Arial", 14))
amount_entry.pack(pady=5)

coin_solve_button = ctk.CTkButton(tab1, text="Solve", command=solve_coin_change, font=("Arial", 14))
coin_solve_button.pack(pady=10)

coin_result_label = ctk.CTkLabel(tab1, text="", font=("Arial", 14))
coin_result_label.pack(pady=10)


weights_label = ctk.CTkLabel(tab2, text="Enter weights (comma-separated):", font=("Arial", 14))
weights_label.pack(pady=5)

weights_entry = ctk.CTkEntry(tab2, width=300, font=("Arial", 14))
weights_entry.pack(pady=5)

values_label = ctk.CTkLabel(tab2, text="Enter values (comma-separated):", font=("Arial", 14))
values_label.pack(pady=5)

values_entry = ctk.CTkEntry(tab2, width=300, font=("Arial", 14))
values_entry.pack(pady=5)

capacity_label = ctk.CTkLabel(tab2, text="Enter knapsack capacity:", font=("Arial", 14))
capacity_label.pack(pady=5)

capacity_entry = ctk.CTkEntry(tab2, width=300, font=("Arial", 14))
capacity_entry.pack(pady=5)

knapsack_solve_button = ctk.CTkButton(tab2, text="Solve", command=solve_knapsack, font=("Arial", 14))
knapsack_solve_button.pack(pady=10)

knapsack_result_label = ctk.CTkLabel(tab2, text="", font=("Arial", 14))
knapsack_result_label.pack(pady=10)


s1_label = ctk.CTkLabel(tab3, text="Enter first string:", font=("Arial", 14))
s1_label.pack(pady=5)

s1_entry = ctk.CTkEntry(tab3, width=300, font=("Arial", 14))
s1_entry.pack(pady=5)

s2_label = ctk.CTkLabel(tab3, text="Enter second string:", font=("Arial", 14))
s2_label.pack(pady=5)

s2_entry = ctk.CTkEntry(tab3, width=300, font=("Arial", 14))
s2_entry.pack(pady=5)

lcs_solve_button = ctk.CTkButton(tab3, text="Solve", command=solve_lcs, font=("Arial", 14))
lcs_solve_button.pack(pady=10)

lcs_result_label = ctk.CTkLabel(tab3, text="", font=("Arial", 14))
lcs_result_label.pack(pady=10)


fibonacci_label = ctk.CTkLabel(tab4, text="Enter n for Fibonacci(n):", font=("Arial", 14))
fibonacci_label.pack(pady=5)

fibonacci_entry = ctk.CTkEntry(tab4, width=300, font=("Arial", 14))
fibonacci_entry.pack(pady=5)

fibonacci_solve_button = ctk.CTkButton(tab4, text="Solve", command=solve_fibonacci, font=("Arial", 14))
fibonacci_solve_button.pack(pady=10)

fibonacci_result_label = ctk.CTkLabel(tab4, text="", font=("Arial", 14))
fibonacci_result_label.pack(pady=10)


lis_label = ctk.CTkLabel(tab5, text="Enter sequence (comma-separated):", font=("Arial", 14))
lis_label.pack(pady=5)

lis_entry = ctk.CTkEntry(tab5, width=300, font=("Arial", 14))
lis_entry.pack(pady=5)

lis_solve_button = ctk.CTkButton(tab5, text="Solve", command=solve_lis, font=("Arial", 14))
lis_solve_button.pack(pady=10)

lis_result_label = ctk.CTkLabel(tab5, text="", font=("Arial", 14))
lis_result_label.pack(pady=10)


mcm_label = ctk.CTkLabel(tab6, text="Enter dimensions (comma-separated):", font=("Arial", 14))
mcm_label.pack(pady=5)

mcm_entry = ctk.CTkEntry(tab6, width=300, font=("Arial", 14))
mcm_entry.pack(pady=5)

mcm_solve_button = ctk.CTkButton(tab6, text="Solve", command=solve_mcm, font=("Arial", 14))
mcm_solve_button.pack(pady=10)

mcm_result_label = ctk.CTkLabel(tab6, text="", font=("Arial", 14))
mcm_result_label.pack(pady=10)


edit_s1_label = ctk.CTkLabel(tab7, text="Enter first string:", font=("Arial", 14))
edit_s1_label.pack(pady=5)

edit_s1_entry = ctk.CTkEntry(tab7, width=300, font=("Arial", 14))
edit_s1_entry.pack(pady=5)

edit_s2_label = ctk.CTkLabel(tab7, text="Enter second string:", font=("Arial", 14))
edit_s2_label.pack(pady=5)

edit_s2_entry = ctk.CTkEntry(tab7, width=300, font=("Arial", 14))
edit_s2_entry.pack(pady=5)

edit_solve_button = ctk.CTkButton(tab7, text="Solve", command=solve_edit_distance, font=("Arial", 14))
edit_solve_button.pack(pady=10)

edit_result_label = ctk.CTkLabel(tab7, text="", font=("Arial", 14))
edit_result_label.pack(pady=10)


lps_label = ctk.CTkLabel(tab8, text="Enter a string:", font=("Arial", 14))
lps_label.pack(pady=5)

lps_entry = ctk.CTkEntry(tab8, width=300, font=("Arial", 14))
lps_entry.pack(pady=5)

lps_solve_button = ctk.CTkButton(tab8, text="Solve", command=solve_lps, font=("Arial", 14))
lps_solve_button.pack(pady=10)

lps_result_label = ctk.CTkLabel(tab8, text="", font=("Arial", 14))
lps_result_label.pack(pady=10)


subset_sum_label = ctk.CTkLabel(tab9, text="Enter numbers (comma-separated):", font=("Arial", 14))
subset_sum_label.pack(pady=5)

subset_sum_entry = ctk.CTkEntry(tab9, width=300, font=("Arial", 14))
subset_sum_entry.pack(pady=5)

subset_target_label = ctk.CTkLabel(tab9, text="Enter target sum:", font=("Arial", 14))
subset_target_label.pack(pady=5)

subset_target_entry = ctk.CTkEntry(tab9, width=300, font=("Arial", 14))
subset_target_entry.pack(pady=5)

subset_sum_solve_button = ctk.CTkButton(tab9, text="Solve", command=solve_subset_sum, font=("Arial", 14))
subset_sum_solve_button.pack(pady=10)

subset_sum_result_label = ctk.CTkLabel(tab9, text="", font=("Arial", 14))
subset_sum_result_label.pack(pady=10)


fractional_weights_label = ctk.CTkLabel(tab10, text="Enter weights (comma-separated):", font=("Arial", 14))
fractional_weights_label.pack(pady=5)

fractional_weights_entry = ctk.CTkEntry(tab10, width=300, font=("Arial", 14))
fractional_weights_entry.pack(pady=5)

fractional_values_label = ctk.CTkLabel(tab10, text="Enter values (comma-separated):", font=("Arial", 14))
fractional_values_label.pack(pady=5)

fractional_values_entry = ctk.CTkEntry(tab10, width=300, font=("Arial", 14))
fractional_values_entry.pack(pady=5)

fractional_capacity_label = ctk.CTkLabel(tab10, text="Enter knapsack capacity:", font=("Arial", 14))
fractional_capacity_label.pack(pady=5)

fractional_capacity_entry = ctk.CTkEntry(tab10, width=300, font=("Arial", 14))
fractional_capacity_entry.pack(pady=5)

fractional_solve_button = ctk.CTkButton(tab10, text="Solve", command=solve_fractional_knapsack, font=("Arial", 14))
fractional_solve_button.pack(pady=10)

fractional_result_label = ctk.CTkLabel(tab10, text="", font=("Arial", 14))
fractional_result_label.pack(pady=10)


app.mainloop()