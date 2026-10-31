
import tkinter as tk
from tkinter import ttk
import datetime

expenses = []

# Window
window = tk.Tk()
window.title("Your Wallet")
window.geometry("950x650")
window.configure(bg="#F5F3FA")


# Load Expenses
try:
    with open("expenses.txt", "r") as file:
        data = file.read()
        lines = data.splitlines()

        for line in lines:
            parts = line.split(" - ")

            if len(parts) == 3:
                expenses.append([ int(parts[0]), parts[1], parts[2]])

except FileNotFoundError:
    print("No expenses found")



# Functions
def save_expenses():
    with open("expenses.txt", "w") as file:
        for expense, category, time in expenses:
            file.write( str(expense) + " - " + category + " - " + str(time) + "\n")

def update_total():
    total = 0

    for expense, category, time in expenses:
        total += int(expense)

    total_label.config(text=str(total) + " SAR")
    count_label.config(text=str(len(expenses)))


def view_expense():
    for item in table.get_children():
        table.delete(item)

    for i, (expense, category, time) in enumerate(expenses):
        table.insert("", tk.END, iid=str(i), values=(expense, category, time))

    update_total()


def clear_entries():
    entry_expense.delete(0, tk.END)
    entry_category.delete(0, tk.END)


def add_expense():
    try:
        expense = int(entry_expense.get())

        if expense <= 0:
            status_label.config( text="Expense must be greater than zero")
            return

        category = entry_category.get().strip()

        if not category:
            status_label.config( text="Category cannot be empty")
            return

        time = datetime.date.today()

        expenses.append([ expense, category, time])

        save_expenses()
        clear_entries()
        view_expense()

        status_label.config( text="Expense added successfully ✓" )

    except ValueError:
        status_label.config( text="Please enter a valid amount" )


def delete_expense():
    selected = table.selection()

    if not selected:
        status_label.config( text="Please select an expense first")
        return

    index = int(selected[0])

    expenses.pop(index)

    save_expenses()
    view_expense()

    status_label.config( text="Expense deleted successfully ✓")


def edit_expense():
    selected = table.selection()

    if not selected:
        status_label.config( text="Please select an expense first")
        return

    try:
        expense = int(entry_expense.get())

        if expense <= 0:
            status_label.config( text="Expense must be greater than zero" )
            return

        category = entry_category.get().strip()

        if not category:
            status_label.config( text="Category cannot be empty")
            return

        index = int(selected[0])

        time = expenses[index][2]

        expenses[index] = [ expense, category, time]

        save_expenses()
        clear_entries()
        view_expense()

        status_label.config(text="Expense updated successfully ✓")

    except ValueError:
        status_label.config(text="Please enter a valid amount")


def show_total():
    total = 0

    for expense, category, time in expenses:
        total += int(expense)

    total_label.config(text=str(total) + " SAR")
    status_label.config(text="Total updated ✓")


def show_average():
    if not expenses:
        status_label.config(text="No expenses found")
        return

    total = 0

    for expense, category, time in expenses:
        total += int(expense)
    average = total / len(expenses)
    status_label.config( text="Average: " + str(round(average, 2)) + " SAR")


def search_category():
    search = entry_category.get().strip().lower()

    for item in table.get_children():
        table.delete(item)

    for i, (expense, category, time) in enumerate(expenses):
        if search in category.lower():
            table.insert("", tk.END, iid=str(i), values=(expense, category, time))

    status_label.config(text="Search results displayed")


def set_budget():
    try:
        budget = int(entry_expense.get())

        if budget <= 0:
            status_label.config(text="Enter a valid budget" )
            return

        total = 0

        for expense, category, time in expenses:
            total += int(expense)

        remaining = budget - total

        status_label.config( text="Budget: " + str(budget) + " SAR | Remaining: " + str(remaining) + " SAR")

    except ValueError:
        status_label.config( text="Enter a valid budget")


# Header
header = tk.Frame(
    window,
    bg="#6C4AB6",
    height=100)

header.pack(fill="x")
header.pack_propagate(False)

title = tk.Label(
    header,
    text="Your Wallet",
    font=("Arial", 28, "bold"),
    bg="#6C4AB6",
    fg="white"
)

title.pack(anchor="w", padx=35, pady=(18, 0))

subtitle = tk.Label(
    header,
    text="Manage your expenses with ease",
    font=("Arial", 11),
    bg="#6C4AB6",
    fg="#E8DFFF"
)

subtitle.pack(anchor="w", padx=38)


# Dashboard
dashboard = tk.Frame(
    window,
    bg="#F5F3FA"
)
dashboard.pack(fill="x", padx=30, pady=20)


# Total Card

total_card = tk.Frame(
    dashboard,
    bg="white",
    height=90
)

total_card.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)

tk.Label(
    total_card,
    text="TOTAL EXPENSES",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#777777"
).pack(anchor="w", padx=20, pady=(15, 0))

total_label = tk.Label(
    total_card,
    text="0 SAR",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#6C4AB6"
)

total_label.pack(anchor="w", padx=20)


# Count Card

count_card = tk.Frame(
    dashboard,
    bg="white",
    height=90
)

count_card.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(10, 0)
)

tk.Label(
    count_card,
    text="NUMBER OF EXPENSES",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#777777"
).pack(anchor="w", padx=20, pady=(15, 0))

count_label = tk.Label(
    count_card,
    text="0",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#6C4AB6"
)

count_label.pack(anchor="w", padx=20)


# Main Content
content = tk.Frame(
    window,
    bg="#F5F3FA"
)

content.pack(
    fill="both",
    expand=True,
    padx=30
)


# Input Section
input_frame = tk.Frame(
    content,
    bg="white"
)

input_frame.pack(
    side="left",
    fill="y",
    padx=(0, 15)
)

tk.Label(
    input_frame,
    text="Add Expense",
    font=("Arial", 18, "bold"),
    bg="white",
    fg="#333333"
).pack(anchor="w", padx=25, pady=(25, 20))


tk.Label(
    input_frame,
    text="Amount",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#555555"
).pack(anchor="w", padx=25)

entry_expense = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=22,
    relief="solid",
    bd=1
)

entry_expense.pack(
    padx=25,
    pady=(5, 15)
)


tk.Label(
    input_frame,
    text="Category",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#555555"
).pack(anchor="w", padx=25)

entry_category = tk.Entry(
    input_frame,
    font=("Arial", 12),
    width=22,
    relief="solid",
    bd=1
)

entry_category.pack(
    padx=25,
    pady=(5, 20)
)


# Buttons
tk.Button(
    input_frame,
    text="Add Expense",
    command=add_expense,
    bg="#6C4AB6",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    width=20,
    pady=8
).pack(pady=5)


tk.Button(
    input_frame,
    text="Edit Selected",
    command=edit_expense,
    bg="#8A6BC4",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    width=20,
    pady=8
).pack(pady=5)


tk.Button(
    input_frame,
    text="Delete Selected",
    command=delete_expense,
    bg="#D9534F",
    fg="white",
    font=("Arial", 11, "bold"),
    relief="flat",
    width=20,
    pady=8
).pack(pady=5)


tk.Button(
    input_frame,
    text="Search Category",
    command=search_category,
    bg="#EEEEEE",
    fg="#333333",
    font=("Arial", 11, "bold"),
    relief="flat",
    width=20,
    pady=8
).pack(pady=5)


tk.Button(
    input_frame,
    text="Show Average",
    command=show_average,
    bg="#EEEEEE",
    fg="#333333",
    font=("Arial", 11, "bold"),
    relief="flat",
    width=20,
    pady=8
).pack(pady=5)


tk.Button(
    input_frame,
    text="Set Budget",
    command=set_budget,
    bg="#EEEEEE",
    fg="#333333",
    font=("Arial", 11, "bold"),
    relief="flat",
    width=20,
    pady=8
).pack(pady=5)


# Table Section
table_frame = tk.Frame(
    content,
    bg="white"
)

table_frame.pack(
    side="right",
    fill="both",
    expand=True
)


tk.Label(
    table_frame,
    text="Your Expenses",
    font=("Arial", 18, "bold"),
    bg="white",
    fg="#333333"
).pack(anchor="w", padx=20, pady=(20, 10))


style = ttk.Style()

style.configure(
    "Treeview",
    rowheight=35,
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    font=("Arial", 10, "bold")
)


table = ttk.Treeview(
    table_frame,
    columns=("Amount", "Category", "Date"),
    show="headings"
)

table.heading(
    "Amount",
    text="Amount"
)

table.heading(
    "Category",
    text="Category"
)

table.heading(
    "Date",
    text="Date"
)

table.column(
    "Amount",
    width=100
)

table.column(
    "Category",
    width=140
)

table.column(
    "Date",
    width=110
)

table.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20)
)


# Status
status_label = tk.Label(
    window,
    text="Ready",
    font=("Arial", 10),
    bg="#F5F3FA",
    fg="#777777"
)

status_label.pack(
    pady=(0, 10)
)


# Start
view_expense()

window.mainloop()

