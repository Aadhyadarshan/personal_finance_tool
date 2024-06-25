import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import csv
import os

root = tk.Tk()
root.title("Personal Finance Tool")
root.configure(bg="#4B382A")

# Create StringVars here
category_var = tk.StringVar()
source_var = tk.StringVar()

def read_csv(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(file_path, fieldnames, data):
    file_exists = os.path.isfile(file_path)
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

def add_expense():
    add_expense_window = tk.Toplevel(root)
    add_expense_window.title("Add Expense")
    add_expense_window.configure(bg="#FFE4C4")

    ttk.Label(add_expense_window, text="Date:").grid(row=0, column=0, padx=10, pady=10)
    date_entry = DateEntry(add_expense_window)
    date_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(add_expense_window, text="Category:").grid(row=1, column=0, padx=10, pady=10)
    category_dropdown = ttk.Combobox(add_expense_window, textvariable=category_var, values=['Food', 'Transport', 'Utilities', 'Entertainment'])
    category_dropdown.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(add_expense_window, text="Amount:").grid(row=2, column=0, padx=10, pady=10)
    amount_entry = ttk.Entry(add_expense_window)
    amount_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(add_expense_window, text="Description:").grid(row=3, column=0, padx=10, pady=10)
    description_entry = ttk.Entry(add_expense_window)
    description_entry.grid(row=3, column=1, padx=10, pady=10)

    def save_expense():
        data = {
            'date': date_entry.get(),
            'category': category_var.get(),
            'amount': amount_entry.get(),
            'description': description_entry.get()
        }
        write_csv('expenses.csv', ['date', 'category', 'amount', 'description'], data)
        check_budget_exceeded()
        messagebox.showinfo("Success", "Expense added successfully")
        add_expense_window.destroy()

    ttk.Button(add_expense_window, text="Save", command=save_expense, style="Brown.TButton").grid(row=4, columnspan=2, padx=10, pady=10)

def add_income():
    add_income_window = tk.Toplevel(root)
    add_income_window.title("Add Income")
    add_income_window.configure(bg="#FFE4C4")

    ttk.Label(add_income_window, text="Date:").grid(row=0, column=0, padx=10, pady=10)
    date_entry = DateEntry(add_income_window)
    date_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(add_income_window, text="Source:").grid(row=1, column=0, padx=10, pady=10)
    source_entry = ttk.Entry(add_income_window, textvariable=source_var)
    source_entry.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(add_income_window, text="Amount:").grid(row=2, column=0, padx=10, pady=10)
    amount_entry = ttk.Entry(add_income_window)
    amount_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(add_income_window, text="Description:").grid(row=3, column=0, padx=10, pady=10)
    description_entry = ttk.Entry(add_income_window)
    description_entry.grid(row=3, column=1, padx=10, pady=10)

    def save_income():
        data = {
            'date': date_entry.get(),
            'ource': source_var.get(),
            'amount': amount_entry.get(),
            'description': description_entry.get()
        }
        write_csv('income.csv', ['date', 'ource', 'amount', 'description'], data)
        messagebox.showinfo("Success", "Income added successfully")
        add_income_window.destroy()

    ttk.Button(add_income_window, text="Save", command=save_income, style="Brown.TButton").grid(row=4, columnspan=2, padx=10, pady=10)

def check_budget_exceeded():
    expenses = read_csv('expenses.csv')
    budgets = read_csv('budget.csv')

    budget_dict = {}
    for budget in budgets:
        try:
            budget_dict[budget['category']] = float(budget['budget'])
        except KeyError as e:
            print(f"Error reading budget data: {e}")
            continue

    expense_dict = {}
    for expense in expenses:
        if not expense['amount']:
            # Skip empty amounts
            continue
        if expense['category'] not in expense_dict:
            expense_dict[expense['category']] = 0.0
        expense_dict[expense['category']] += float(expense['amount'])

    for category, total_expense in expense_dict.items():
        if category in budget_dict and total_expense > budget_dict[category]:
            messagebox.showwarning("Budget Exceeded", f"Warning: The budget for '{category}' has been exceeded.")

    return expense_dict

def view_report():
    def generate_report():
        report_window = tk.Toplevel(root)
        report_window.title("Financial Report")
        report_window.configure(bg="#FFE4C4")

        expenses = read_csv('expenses.csv')
        income = read_csv('income.csv')

        ttk.Label(report_window, text="Expenses:", background="#FFE4C4", foreground="black").pack(padx=10, pady=10)
        for expense in expenses:
            ttk.Label(report_window, text=f"{expense['date']} - {expense['category']} - ${expense['amount']} - {expense['description']}",
                      background="#FFE4C4", foreground="black").pack(padx=10, pady=5)

        ttk.Label(report_window, text="Income:", background="#FFE4C4", foreground="black").pack(padx=10, pady=10)
        for inc in income:
            ttk.Label(report_window, text=f"{inc['date']} - {inc['source']} - ${inc['amount']} - {inc['description']}",
                      background="#FFE4C4", foreground="black").pack(padx=10, pady=5)

    generate_report()

style = ttk.Style()
style.configure("Brown.TButton", foreground="black", background="#8b5a2b", font=('Papyrus', 10))

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Add Expense", command=add_expense)
file_menu.add_command(label="Add Income", command=add_income)
file_menu.add_separator()
file_menu.add_command(label="View Report", command=view_report)
menu.add_cascade(label="File", menu=file_menu)

root.mainloop()