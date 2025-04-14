import tkinter as tk
from tkinter import ttk

# Dummy data
chain_data = [
    ("EVID001", "Investigator 1", "2025-04-10 10:30 AM", "Pending"),
    ("EVID001", "Investigator 2", "2025-04-11 09:45 AM", "Analyzed"),
    ("EVID002", "Investigator 2", "2025-04-12 01:15 PM", "Pending"),
    ("EVID003", "Investigator 1", "2025-04-13 03:00 PM", "Pending"),
]

# GUI setup
root = tk.Tk()
root.title("🧾 Chain of Custody Tracker")
root.geometry("800x400")
root.configure(bg="#f0f7ff")

title = tk.Label(root, text="🔒 Chain of Custody Tracker", font=("Arial", 20, "bold"), bg="#f0f7ff", fg="#003366")
title.pack(pady=15)

# Frame for table
frame = tk.Frame(root, bg="#f0f7ff")
frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

# Scrollbars
scroll_y = tk.Scrollbar(frame, orient=tk.VERTICAL)
scroll_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)

# Table
columns = ("Fir-Number", "Investigator", "Date & Time", "Action")
tree = ttk.Treeview(frame, columns=columns, show="headings",
                    yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=180)

tree.pack(fill=tk.BOTH, expand=True)

# Load dummy data
for entry in chain_data:
    tree.insert("", tk.END, values=entry)

root.mainloop()
