import tkinter as tk
import datetime

expenses =[]

window = tk.Tk()
try:
    with open("expenses.txt", "r") as file:
        data = file.read()
        lines = data.splitlines()
        for line in lines:
            expenses.append([int(line.split(" - ")[0]), line.split(" - ")[1], line.split(" - ")[2]])
except FileNotFoundError:
    print("No expenses found")

window.title("Your wallet")
window.geometry("600x500")

listbox = tk.Listbox(window)
listbox.pack()

tk.Label(window, text="Add Expense: ").pack()
entry_expense = tk.Entry(window)
entry_expense.pack()

tk.Label(window, text="What type of expense: ").pack()
entry_category = tk.Entry(window)
entry_category.pack()

def add_expense():
    try:
        expense = int(entry_expense.get())
        time = datetime.date.today()

        if expense <= 0:
            print("Expense must be greater than zero")
        else:
            print(expense)
            category = entry_category.get()
            if not category.strip():
                print("Category cannot be empty")
            else:
                category = category.strip()
                time = datetime.date.today()

                expenses.append([expense, category, time])

                with open("expenses.txt", "a") as file:
                    file.write(str(expense) + " - " + category + " - " + str(time) + "\n")
                    entry_expense.delete(0, tk.END)
                    entry_category.delete(0, tk.END)

    except ValueError:
        print("Please enter an integer")

def view_expense():
    listbox.delete(0, tk.END)

    for expense, category, time in expenses:
        listbox.insert(tk.END, str(expense) + " - " + category + " - " + str(time))

def show_total():
    total = 0

    for expense, category, time in expenses:
        total += int(expense)

    listbox.insert(tk.END, "total: " + str(total) + "SAR")

def delete_expense():
    selected = listbox.curselection()
    print(selected)

    if selected:
        index = selected[0]
        expenses.pop(index)

        with open("expenses.txt", "w") as file:
            for expense, category, time in expenses:
                file.write(str(expense) + " - " + category + " - " + str(time) + "\n")

        view_expense()
        print(index)


title = tk.Label(window, text="Your wallet")
title.pack()

button = tk.Button(window, text="Add Expense",command=add_expense ,bg="purple", fg="white")
button.pack()

button = tk.Button(window, text="View Expenses",command=view_expense ,bg="pink", fg="white")
button.pack()

button = tk.Button(window, text="Show Total",command=show_total , bg="green", fg="white")
button.pack()

button = tk.Button(window, text="Delete Expense",command=delete_expense , bg="green", fg="white")
button.pack()

window.mainloop()
