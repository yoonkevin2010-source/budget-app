import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

# Variables
transactions = []
categories = ["Salary", "Food", "Transportation", "Entertainment", "Other"]
budget_limits = {}


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


def load_budget_limits():
    global budget_limits
    try:
        with open("budget_limits.json", "r", encoding="utf-8") as file:
            budget_limits = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        budget_limits = {category: 0 for category in categories}
        save_budget_limits()


def save_budget_limits():
    with open("budget_limits.json", "w", encoding="utf-8") as file:
        json.dump(budget_limits, file, ensure_ascii=False, indent=4)


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
    current_month = datetime.now().strftime("%Y-%m")

    limit = budget_limits.get(category, 0)

    current_expense = 0
    for transaction in transactions:
        if (transaction["type"] == "Expense" and
                transaction["category"] == category and
                current_month in transaction["date"]):
            current_expense += transaction["amount"]

    if limit > 0 and (current_expense + amount) > limit:
        return f"Budget limit exceeded! {category}: ${limit:,} limit, already spent ${current_expense:,}, trying to add ${amount:,}"

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
load_budget_limits()

root = tk.Tk()
root.title("Budget App")
root.geometry("400x380")

title_label = tk.Label(root, text="=== Budget App ===", font=("Arial", 16, "bold"))
title_label.pack(pady=10)


def show_transactions_window():
    trans_window = tk.Toplevel(root)
    trans_window.title("Transaction History")
    trans_window.geometry("500x400")

    columns = ("No.", "Date", "Type", "Category", "Amount")
    tree = ttk.Treeview(trans_window, columns=columns, height=15)

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("No.", anchor=tk.CENTER, width=40)
    tree.column("Date", anchor=tk.CENTER, width=100)
    tree.column("Type", anchor=tk.CENTER, width=60)
    tree.column("Category", anchor=tk.CENTER, width=80)
    tree.column("Amount", anchor=tk.E, width=100)

    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("No.", text="No.", anchor=tk.CENTER)
    tree.heading("Date", text="Date", anchor=tk.CENTER)
    tree.heading("Type", text="Type", anchor=tk.CENTER)
    tree.heading("Category", text="Category", anchor=tk.CENTER)
    tree.heading("Amount", text="Amount", anchor=tk.CENTER)

    for i, transaction in enumerate(transactions, 1):
        tree.insert(parent='', index='end', iid=i - 1,
                    values=(i, transaction["date"], transaction["type"],
                            transaction["category"], f"${transaction['amount']:,}"))

    tree.pack(pady=10, fill=tk.BOTH, expand=True)

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


def show_add_income_window():
    income_window = tk.Toplevel(root)
    income_window.title("Record Income")
    income_window.geometry("300x250")

    tk.Label(income_window, text="Amount:").pack(pady=5)
    amount_entry = tk.Entry(income_window, width=20)
    amount_entry.pack(pady=5)

    tk.Label(income_window, text="Category:").pack(pady=5)
    category_combo = ttk.Combobox(income_window, values=categories, width=18)
    category_combo.pack(pady=5)

    tk.Label(income_window, text="Date (Example: 2025-01-15):").pack(pady=5)
    date_entry = tk.Entry(income_window, width=20)
    date_entry.pack(pady=5)

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

            if "Budget limit exceeded" in result:
                messagebox.showerror("Budget Exceeded", result)
                return

            messagebox.showinfo("Success", result)
            expense_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter amount as a number.")

    save_btn = tk.Button(expense_window, text="Save", command=save_expense, width=15)
    save_btn.pack(pady=20)


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


def show_budget_limits_window():
    budget_window = tk.Toplevel(root)
    budget_window.title("Set Budget Limits")
    budget_window.geometry("300x250")

    tk.Label(budget_window, text="Category:").pack(pady=5)
    category_combo = ttk.Combobox(budget_window, values=categories, width=18)
    category_combo.pack(pady=5)

    tk.Label(budget_window, text="Monthly Limit ($):").pack(pady=5)
    limit_entry = tk.Entry(budget_window, width=20)
    limit_entry.pack(pady=5)

    def save_budget():
        try:
            category = category_combo.get()
            limit = int(limit_entry.get())

            if not category:
                messagebox.showerror("Error", "Please select a category.")
                return

            budget_limits[category] = limit
            save_budget_limits()
            messagebox.showinfo("Success", f"Budget limit set for {category}: ${limit:,}")
            budget_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Please enter amount as a number.")

    save_btn = tk.Button(budget_window, text="Save", command=save_budget, width=15)
    save_btn.pack(pady=20)


def show_view_budget_window():
    view_window = tk.Toplevel(root)
    view_window.title("View Budget Limits")
    view_window.geometry("600x400")

    columns = ("Category", "Monthly Limit", "This Month Expense", "Remaining")
    tree = ttk.Treeview(view_window, columns=columns, height=12)

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Category", anchor=tk.CENTER, width=120)
    tree.column("Monthly Limit", anchor=tk.CENTER, width=120)
    tree.column("This Month Expense", anchor=tk.CENTER, width=150)
    tree.column("Remaining", anchor=tk.CENTER, width=120)

    tree.heading("#0", text="", anchor=tk.W)
    tree.heading("Category", text="Category", anchor=tk.CENTER)
    tree.heading("Monthly Limit", text="Monthly Limit", anchor=tk.CENTER)
    tree.heading("This Month Expense", text="This Month Expense", anchor=tk.CENTER)
    tree.heading("Remaining", text="Remaining", anchor=tk.CENTER)

    current_month = datetime.now().strftime("%Y-%m")

    for category in categories:
        limit = budget_limits.get(category, 0)

        expense = 0
        for transaction in transactions:
            if (transaction["type"] == "Expense" and
                    transaction["category"] == category and
                    current_month in transaction["date"]):
                expense += transaction["amount"]

        remaining = limit - expense if limit > 0 else 0

        tree.insert(parent='', index='end',
                    values=(category, f"${limit:,}" if limit > 0 else "No limit",
                            f"${expense:,}", f"${remaining:,}" if limit > 0 else "N/A"))

    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def show_reset_window():
        reset_window = tk.Toplevel(view_window)
        reset_window.title("Reset Budget")
        reset_window.geometry("300x200")

        tk.Label(reset_window, text="Select Category to Reset:").pack(pady=10)
        reset_combo = ttk.Combobox(reset_window, values=categories, width=20)
        reset_combo.pack(pady=10)

        def reset_budget():
            category = reset_combo.get()
            if not category:
                messagebox.showerror("Error", "Please select a category.")
                return

            if messagebox.askyesno("Confirm", f"Are you sure you want to reset budget for {category}?"):
                budget_limits[category] = 0
                save_budget_limits()
                messagebox.showinfo("Success", f"Budget for {category} has been reset.")
                reset_window.destroy()
                view_window.destroy()

        reset_btn = tk.Button(reset_window, text="Reset", command=reset_budget, bg="orange", fg="white")
        reset_btn.pack(pady=20)

    reset_btn = tk.Button(view_window, text="Reset Budget", command=show_reset_window, bg="red", fg="white")
    reset_btn.pack(pady=10)



def show_expense_analysis_window():
    analysis_window = tk.Toplevel(root)
    analysis_window.title("Expense Analysis")
    analysis_window.geometry("600x500")

    # 1단계: 데이터 준비
    current_month = datetime.now().strftime("%Y-%m")
    total_income = 0
    total_expense = 0
    category_expense = {cat: 0 for cat in categories}

    for transaction in transactions:
        if current_month in transaction["date"]:
            if transaction["type"] == "Income":
                total_income += transaction["amount"]
            elif transaction["type"] == "Expense":
                total_expense += transaction["amount"]
                category_expense[transaction["category"]] += transaction["amount"]



    filtered_labels = []
    filtered_sizes = []

    for category, amount in category_expense.items():
        if amount > 0:
            filtered_labels.append(category)
            filtered_sizes.append(amount)

    fig, ax = plt.subplots(figsize = (6, 5))
    ax.pie(filtered_sizes, labels=filtered_labels, autopct='%1.2f%%')
    plt.title(f"Expense by Category - {current_month}")
    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=analysis_window)
    canvas.get_tk_widget().pack()


def show_export_window():
    export_window = tk.Toplevel(root)
    export_window.title("Export Data")
    export_window.geometry("300x200")

    tk.Label(export_window, text="Export Budget Data to Excel").pack(pady=10)

    def export_to_excel():
        try:
            import pandas as pd


            df_transactions = pd.DataFrame(transactions)

            current_month = datetime.now().strftime("%Y-%m")

            total_income = 0
            total_expense = 0

            for transaction in transactions:
                if current_month in transaction["date"]:
                    if transaction["type"] == "Income":
                        total_income += transaction["amount"]
                    elif transaction["type"] == "Expense":
                        total_expense += transaction["amount"]

            balance = total_income - total_expense
            expense_ratio = (total_expense / total_income * 100) if total_income > 0 else 0

            statistics = {
                "Category": ["Total Income", "Total Expense", "Balance", "Expense Ratio (%)"],
                "Amount": [total_income, total_expense, balance, round(expense_ratio, 2)]
            }
            df_statistics = pd.DataFrame(statistics)






            with pd.ExcelWriter("budget_data.xlsx") as writer:
                df_transactions.to_excel(writer, sheet_name="Transactions")
                df_statistics.to_excel(writer, sheet_name="Statistics")




                worksheet = writer.sheets['Transactions']
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2) * 2  # 2배로
                    worksheet.column_dimensions[column_letter].width = adjusted_width

                from openpyxl.styles import numbers
                for row in worksheet.iter_rows(min_col=2, max_col=2, min_row=2):  # B 열, 2번 행부터
                    for cell in row:
                        cell.number_format = '$#,##0'

            messagebox.showinfo("Success", "Data exported to budget_data.xlsx")
        except Exception as e:
            messagebox.showerror("Error", str(e))




    export_btn = tk.Button(export_window, text="Export", command=export_to_excel)
    export_btn.pack(pady=20)



# Main buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

btn_income = tk.Button(button_frame, text="Record Income", width=15, command=show_add_income_window)
btn_income.grid(row=0, column=0, padx=5, pady=5)

btn_expense = tk.Button(button_frame, text="Record Expense", width=15, command=show_add_expense_window)
btn_expense.grid(row=1, column=0, padx=5, pady=5)

btn_stats = tk.Button(button_frame, text="Statistics", width=15, command=show_statistics_window)
btn_stats.grid(row=2, column=0, padx=5, pady=5)

btn_budget = tk.Button(button_frame, text="Set Budget Limits", width=15, command=show_budget_limits_window)
btn_budget.grid(row=3, column=0, padx=5, pady=5)

btn_view_budget = tk.Button(button_frame, text="View Budget Limits", width=15, command=show_view_budget_window)
btn_view_budget.grid(row=4, column=0, padx=5, pady=5)

btn_transactions = tk.Button(button_frame, text="View/Delete", width=15, command=show_transactions_window)
btn_transactions.grid(row=5, column=0, padx=5, pady=5)

btn_analysis = tk.Button(button_frame, text="Expense Analysis", width=15, command=show_expense_analysis_window)
btn_analysis.grid(row=6, column=0, padx=5, pady=5)

btn_export = tk.Button(button_frame, text="Export to Excel", width=15, command=show_export_window)
btn_export.grid(row=7, column=0, padx=5, pady=5)

root.mainloop()