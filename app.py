import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import csv
import os
import matplotlib.pyplot as plt

# Read the CSV file and return its contents as a list of dictionaries.
def read_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Write data to a CSV file, creating it if it doesn't exist, and appending new rows.
def write_csv(file_path, fieldnames, data):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Generate a bar chart to analyze expenses by category.
def generate_expense_analysis():
    expenses = read_csv('expenses.csv')
    categories = set(expense['category'] for expense in expenses)
    category_expenses = {}

    for category in categories:
        total_amount = 0.0
        for expense in expenses:
            if expense['category'] == category and expense['amount']:
                try:
                    total_amount += float(expense['amount'])
                except ValueError:
                    pass  # Ignore non-float values
        category_expenses[category] = total_amount

    plt.figure(figsize=(10, 6))
    plt.bar(category_expenses.keys(), category_expenses.values(), color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Total Expense')
    plt.title('Expense Analysis')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Placeholder for a function to backup data, implementation not provided.
def backup_data():
    pass

# Create a window to add an expense entry.
def add_expense():
    global add_expense_window, date_entry, category_var, amount_entry, description_entry
    add_expense_window = tk.Toplevel(root)
    add_expense_window.title("Add Expense")
    add_expense_window.configure(bg="#FFE4C4")

    ttk.Label(add_expense_window, text="Date:").grid(row=0, column=0, padx=10, pady=10)
    date_entry = DateEntry(add_expense_window)
    date_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(add_expense_window, text="Category:").grid(row=1, column=0, padx=10, pady=10)
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(add_expense_window, textvariable=category_var, values=['Food', 'Transport', 'Utilities', 'Entertainment'])
    category_dropdown.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(add_expense_window, text="Amount:").grid(row=2, column=0, padx=10, pady=10)
    amount_entry = ttk.Entry(add_expense_window)
    amount_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(add_expense_window, text="Description:").grid(row=3, column=0, padx=10, pady=10)
    description_entry = ttk.Entry(add_expense_window)
    description_entry.grid(row=3, column=1, padx=10, pady=10)

    ttk.Button(add_expense_window, text="Save", command=save_expense, style="Brown.TButton").grid(row=4, columnspan=2, padx=10, pady=10)

# Save the entered expense data to the CSV file.
def save_expense():
    category = category_var.get()
    data = {
        'date': date_entry.get(),
        'category': category,
        'amount': amount_entry.get(),
        'description': description_entry.get()
    }
    write_csv('expenses.csv', ['date', 'category', 'amount', 'description'], data)
    if check_budget_exceeded(category):
        messagebox.showwarning("Budget Exceeded", f"Warning: The budget for '{category}' has been exceeded.")
    else:
        messagebox.showinfo("Success", "Expense added successfully")
    add_expense_window.destroy()

# Create a window to set a budget for a category.
def set_budget(category=None):
    global set_budget_window, budget_category_var, budget_amount_entry
    set_budget_window = tk.Toplevel(root)
    set_budget_window.title("Set Budget")
    set_budget_window.configure(bg="#FFE4C4")

    ttk.Label(set_budget_window, text="Category:").grid(row=0, column=0, padx=10, pady=10)
    budget_category_var = tk.StringVar(value=category)
    budget_category_dropdown = ttk.Combobox(set_budget_window, textvariable=budget_category_var, values=['Food', 'Transport', 'Utilities', 'Entertainment'])
    budget_category_dropdown.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(set_budget_window, text="Budget Amount:").grid(row=1, column=0, padx=10, pady=10)
    budget_amount_entry = ttk.Entry(set_budget_window)
    budget_amount_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Button(set_budget_window, text="Save", command=save_budget, style="Brown.TButton").grid(row=2, columnspan=2, padx=10, pady=10)

# Save the budget data to the CSV file.
def save_budget():
    data = {
        'category': budget_category_var.get(),
        'budget': budget_amount_entry.get()
    }
    write_csv('budget.csv', ['category', 'budget'], data)
    messagebox.showinfo("Success", "Budget set successfully")
    set_budget_window.destroy()

# Create a window to add an income entry.
def add_income():
    add_income_window = tk.Toplevel(root)
    add_income_window.title("Add Income")
    add_income_window.configure(bg="#FFE4C4")

    ttk.Label(add_income_window, text="Date:", background="#FFE4C4", foreground="black").grid(row=0, column=0, padx=10, pady=10)
    date_entry = DateEntry(add_income_window, background="#FFE4C4", foreground="black", borderwidth=2)
    date_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(add_income_window, text="Source:", background="#FFE4C4", foreground="black").grid(row=1, column=0, padx=10, pady=10)
    source_entry = ttk.Entry(add_income_window)
    source_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(add_income_window, text="Amount:", background="#FFE4C4", foreground="black").grid(row=2, column=0, padx=10, pady=10)
    amount_entry = ttk.Entry(add_income_window)
    amount_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(add_income_window, text="Description:", background="#FFE4C4", foreground="black").grid(row=3, column=0, padx=10, pady=10)
    description_entry = ttk.Entry(add_income_window)
    description_entry.grid(row=3, column=1, padx=10, pady=10)

    def save_income():
        data = {
            'date': date_entry.get(),
            'source': source_entry.get(),
            'amount': amount_entry.get(),
            'description': description_entry.get()
        }
        write_csv('income.csv', ['date', 'source', 'amount', 'description'], data)
        messagebox.showinfo("Success", "Income added successfully")
        add_income_window.destroy()

    ttk.Button(add_income_window, text="Save", command=save_income, style="Brown.TButton").grid(row=4, columnspan=2, padx=10, pady=10)

# Check if the budget for any category has been exceeded.
def check_budget_exceeded(category=None):
    expenses = read_csv('expenses.csv')
    budgets = read_csv('budget.csv')

    budget_dict = {}
    for budget in budgets:
        try:
            budget_dict[budget['category']] = float(budget['budget'])
        except ValueError as e:
            print(f"Error reading budget data: {e}")
            continue

    expense_dict = {}
    for expense in expenses:
        if not expense['amount']:
            continue
        if expense['category'] not in expense_dict:
            expense_dict[expense['category']] = 0.0
        expense_dict[expense['category']] += float(expense['amount'])

    if category:
        total_expense = expense_dict.get(category, 0.0)
        if category in budget_dict and total_expense > budget_dict[category]:
            return True
    else:
        for category, total_expense in expense_dict.items():
            if category in budget_dict and total_expense > budget_dict[category]:
                messagebox.showwarning("Budget Exceeded", f"Warning: The budget for '{category}' has been exceeded.")
    return False

# Generate a report showing all expenses and income.
def view_report():
    def generate_report():
        report_window = tk.Toplevel(root)
        report_window.title("Financial Report")
        report_window.configure(bg="#FFE4C4")

        expenses = read_csv('expenses.csv')
        income = read_csv('income.csv')

        ttk.Label(report_window, text="Expenses:", background="#FFE4C4", foreground="black", font=('Microsoft Himalaya', 18)).pack(padx=10, pady=10)
        for expense in expenses:
            ttk.Label(report_window, text=f"{expense['date']} - {expense['category']} - ₹{expense['amount']} - {expense['description']}",
                      background="#FFE4C4", foreground="black", font=('Microsoft Himalaya', 14)).pack(padx=10, pady=5)

        ttk.Label(report_window, text="Income:", background="#FFE4C4", foreground="black", font=('Microsoft Himalaya', 18)).pack(padx=10, pady=10)
        for inc in income:
            ttk.Label(report_window, text=f"{inc['date']} - {inc['source']} - ₹{inc['amount']} - {inc['description']}",
                      background="#FFE4C4", foreground="black", font=('Microsoft Himalaya', 14)).pack(padx=10, pady=5)

    generate_report()

# Create the main application window.
root = tk.Tk()
root.title("Personal Finance Tool")
root.configure(bg="#4B382A")

# Style configuration for buttons.
style = ttk.Style()
style.configure("Brown.TButton", foreground="black", background="#8b5a2b", font=('Microsoft Himalaya', 12))

# Create the menu bar and add menu items.
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Add Expense", command=add_expense)
file_menu.add_command(label="Add Income", command=add_income)
file_menu.add_command(label="Set Budget", command=set_budget)
file_menu.add_command(label="Expense Analysis", command=generate_expense_analysis)
file_menu.add_separator()
file_menu.add_command(label="View Report", command=view_report)
menu.add_cascade(label="File", menu=file_menu)

# Schedule backup data function to run every 60 seconds.
root.after(60000, backup_data)

# Start the Tkinter event loop.
root.mainloop()
