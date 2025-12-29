import tkinter as tk
from tkinter import messagebox, ttk
import json

# Variables
transactions = []
categories = ["Salary", "Food", "Transportation", "Entertainment", "Other"]


def load_data():
    global transactions
    try:
        with open("transactions.json", "r", encoding="utf-8") as file:
            transactions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        transactions = []


def save_data():
    with open("transactions.json", "w", encoding="utf-8") as file:
        json.dump(transactions, file, ensure_ascii=False, indent=4)


def add_income(amount, category, date):
    transaction = {
        "amount": amount,
        "category": category,
        "date": date,
        "type": "Income"
    }
    transactions.append(transaction)
    save_data()
    return "✓ Income recorded successfully."


def add_expense(amount, category, date):
    transaction = {
        "amount": amount,
        "category": category,
        "date": date,
        "type": "Expense"
    }
    transactions.append(transaction)
    save_data()
    return "✓ Expense recorded successfully."


# GUI Setup
load_data()

root = tk.Tk()
root.title("Budget App")
root.geometry("400x300")

title_label = tk.Label(root, text="=== Budget App ===", font=("Arial", 16, "bold"))
title_label.pack(pady=10)


def show_transactions_window():
    trans_window = tk.Toplevel(root)
    trans_window.title("Transaction History")
    trans_window.geometry("500x400")

    # Create Treeview
    columns = ("No.", "Date", "Type", "Category", "Amount")
    tree = ttk.Treeview(trans_window, columns=columns, height=15)

    # Column settings
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("No.", anchor=tk.CENTER, width=40)
    tree.column("Date", anchor=tk.CENTER, width=100)
    tree.column("Type", anchor=tk.CENTER, width=60)
    tree.column("Category", anchor=tk.CENTER, width=80)
    tree.column("Amount", anchor=tk.E, width=100)

    # Header settings
    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("No.", text="No.", anchor=tk.CENTER)
    tree.heading("Date", text="Date", anchor=tk.CENTER)
    tree.heading("Type", text="Type", anchor=tk.CENTER)
    tree.heading("Category", text="Category", anchor=tk.CENTER)
    tree.heading("Amount", text="Amount", anchor=tk.CENTER)

    # Fill data
    for i, transaction in enumerate(transactions, 1):
        tree.insert(parent='', index='end', iid=i-1,
                    values=(i, transaction["date"], transaction["type"],
                            transaction["category"], f"${transaction['amount']:,}"))

    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Delete button
    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a transaction to delete.")
            return

        indices = [int(item) for item in selected]
        indices.sort(reverse=True)

        for idx in indices:
            transactions.pop(idx)

        save_data()
        messagebox.showinfo("Success", "Transaction(s) deleted successfully.")
        trans_window.destroy()

    delete_btn = tk.Button(trans_window, text="Delete Selected", command=delete_selected, bg="red", fg="white")
    delete_btn.pack(pady=10)

# Income entry window
def show_add_income_window():
    income_window = tk.Toplevel(root)
    income_window.title("Record Income")
    income_window.geometry("300x250")

    # Amount input
    tk.Label(income_window, text="Amount:").pack(pady=5)
    amount_entry = tk.Entry(income_window, width=20)
    amount_entry.pack(pady=5)

    # Category selection
    tk.Label(income_window, text="Category:").pack(pady=5)
    category_combo = ttk.Combobox(income_window, values=categories, width=18)
    category_combo.pack(pady=5)

    # Date input
    tk.Label(income_window, text="Date (Example: 2025-01-15):").pack(pady=5)
    date_entry = tk.Entry(income_window, width=20)
    date_entry.pack(pady=5)

    # Save button
    def save_income():
        try:
            amount = int(amount_entry.get())
            category = category_combo.get()
            date = date_entry.get()

            if not category:
                messagebox.showerror("Error", "Please select a category.")
                return

            result = add_income(amount, category, date)
            messagebox.showinfo("Success", result)
            income_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter amount as a number.")

    save_btn = tk.Button(income_window, text="Save", command=save_income, width=15)
    save_btn.pack(pady=20)


# Expense entry window
def show_add_expense_window():
    expense_window = tk.Toplevel(root)
    expense_window.title("Record Expense")
    expense_window.geometry("300x250")

    tk.Label(expense_window, text="Amount:").pack(pady=5)
    amount_entry = tk.Entry(expense_window, width=20)
    amount_entry.pack(pady=5)

    tk.Label(expense_window, text="Category:").pack(pady=5)
    category_combo = ttk.Combobox(expense_window, values=categories, width=18)
    category_combo.pack(pady=5)

    tk.Label(expense_window, text="Date (Example: 2025-01-15):").pack(pady=5)
    date_entry = tk.Entry(expense_window, width=20)
    date_entry.pack(pady=5)

    def save_expense():
        try:
            amount = int(amount_entry.get())
            category = category_combo.get()
            date = date_entry.get()

            if not category:
                messagebox.showerror("Error", "Please select a category.")
                return

            result = add_expense(amount, category, date)
            messagebox.showinfo("Success", result)
            expense_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter amount as a number.")

    save_btn = tk.Button(expense_window, text="Save", command=save_expense, width=15)
    save_btn.pack(pady=20)


# Statistics window
def show_statistics_window():
    stats_window = tk.Toplevel(root)
    stats_window.title("Statistics")
    stats_window.geometry("300x200")

    total_income = 0
    total_expense = 0

    for transaction in transactions:
        if transaction["type"] == "Income":
            total_income += transaction["amount"]
        else:
            total_expense += transaction["amount"]

    stats_text = f"""
Total Income: ${total_income:,}
Total Expense: ${total_expense:,}
Balance: ${total_income - total_expense:,}
    """

    stats_label = tk.Label(stats_window, text=stats_text, font=("Arial", 12))
    stats_label.pack(pady=20)


# Main buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

btn_income = tk.Button(button_frame, text="Record Income", width=15, command=show_add_income_window)
btn_income.grid(row=0, column=0, padx=5, pady=5)

btn_expense = tk.Button(button_frame, text="Record Expense", width=15, command=show_add_expense_window)
btn_expense.grid(row=1, column=0, padx=5, pady=5)

btn_stats = tk.Button(button_frame, text="Statistics", width=15, command=show_statistics_window)
btn_stats.grid(row=2, column=0, padx=5, pady=5)

btn_transactions = tk.Button(button_frame, text="View/Delete", width=15, command=show_transactions_window)
btn_transactions.grid(row=3, column=0, padx=5, pady=5)

root.mainloop()