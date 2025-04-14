import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox

# --- MySQL Connection ---
def fetch_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # Replace with your actual password
            database="forensic_reports"
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT firnumber, dateofreport, investigatingOfficerName,
                   physicalEvidence, digitalEvidence, documentaryEvidence, findingsObservations
            FROM reports
        """)
        rows = cursor.fetchall()

        data = []
        for row in rows:
            fir = row[0] if row[0] else "--"
            date = row[1] if row[1] else "--"
            officer = row[2] if row[2] else "--"
            physical = row[3] if row[3] else "--"
            digital = row[4] if row[4] else "--"
            documentary = row[5] if row[5] else "--"
            findings = row[6] if row[6] else "--"

            # Status based on whether all evidence fields are filled
            status = "Analyzed" if all([row[3], row[4], row[5], row[6]]) else "Pending"

            data.append((fir, date, officer, physical, digital, documentary, findings, status))

        conn.close()
        return data

    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return []

# --- GUI Setup ---
root = tk.Tk()
root.title("Facilitator Dashboard")
root.geometry("1300x500")  # Wider to fit more columns
root.configure(bg="#e6f2ff")

title = tk.Label(root, text="🔍 Evidence Management", font=("Arial", 20, "bold"), bg="#e6f2ff", fg="#003366")
title.pack(pady=15)

# Frame for table
table_frame = tk.Frame(root, bg="#e6f2ff")
table_frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

# Scrollbars
scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

# Updated Columns
columns = (
    "FIR Number", "Date of Report", "Investigating Officer",
    "Physical Evidence", "Digital Evidence", "Documentary Evidence",
    "Findings / Observations", "Status"
)

tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                    yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, height=15)

scroll_y.config(command=tree.yview)
scroll_x.config(command=tree.xview)

scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=160)

tree.pack(fill=tk.BOTH, expand=True)

# --- Load Data ---
data = fetch_data()
for row in data:
    tree.insert("", tk.END, values=row)

root.mainloop()
