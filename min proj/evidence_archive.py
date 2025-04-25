import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

def main_archive(): 
 def fetch_filtered_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootsavio321",
            database="reports"
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT firnumber, dateofreport, investigatingOfficerName,
                   physicalEvidence, digitalEvidence, documentaryEvidence, findingsObservations
            FROM reports
        """)
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return []

    filtered_data = []
    fir_filter = fir_entry.get().strip()
    date_filter = date_entry.get().strip()
    investigator_filter = investigator_entry.get().strip().lower()
    evidence_type_filter = evidence_type_entry.get().strip().lower()

    for row in rows:
        fir, date, investigator, physical, digital, documentary, findings = row

        # Sanitize/normalize values
        fir = fir or "--"
        date = str(date) if date else "--"
        investigator = investigator or "--"
        physical = physical or "--"
        digital = digital or "--"
        documentary = documentary or "--"
        findings = findings or "--"

        # Check matches
        match = True
        if fir_filter and fir_filter != fir:
            match = False
        if date_filter and date_filter not in date:
            match = False
        if investigator_filter and investigator_filter not in investigator.lower():
            match = False
        if evidence_type_filter:
            all_types = [physical.lower(), digital.lower(), documentary.lower()]
            if not any(evidence_type_filter in ev for ev in all_types):
                match = False

        if match:
            filtered_data.append((fir, date, investigator, physical, digital, documentary, findings))

    return filtered_data

 # --- Load Data into Tree ---
 def load_data():
    for row in tree.get_children():
        tree.delete(row)

    data = fetch_filtered_data()
    for row in data:
        tree.insert("", tk.END, values=row)

 # --- UI Setup ---
 root = tk.Tk()
 root.title("🗂️ Evidence Archive")
 root.geometry("1200x600")
 root.configure(bg="#f0f8ff")

 title = tk.Label(root, text="📂 Evidence Archive - Facilitator View",
                 font=("Arial", 22, "bold"), bg="#f0f8ff", fg="#003366")
 title.pack(pady=10)

 # --- Filter Section ---
 filter_frame = tk.Frame(root, bg="#f0f8ff")
 filter_frame.pack(pady=5)

 tk.Label(filter_frame, text="FIR Number:", bg="#f0f8ff", font=("Arial", 10)).grid(row=0, column=0, padx=5)
 fir_entry = tk.Entry(filter_frame)
 fir_entry.grid(row=0, column=1, padx=5)

 tk.Label(filter_frame, text="Date (YYYY-MM-DD):", bg="#f0f8ff", font=("Arial", 10)).grid(row=0, column=2, padx=5)
 date_entry = tk.Entry(filter_frame)
 date_entry.grid(row=0, column=3, padx=5)

 tk.Label(filter_frame, text="Investigator Name:", bg="#f0f8ff", font=("Arial", 10)).grid(row=1, column=0, padx=5)
 investigator_entry = tk.Entry(filter_frame)
 investigator_entry.grid(row=1, column=1, padx=5)

 tk.Label(filter_frame, text="Evidence Type:", bg="#f0f8ff", font=("Arial", 10)).grid(row=1, column=2, padx=5)
 evidence_type_entry = tk.Entry(filter_frame)
 evidence_type_entry.grid(row=1, column=3, padx=5)

 search_btn = tk.Button(filter_frame, text="🔍 Search", command=load_data, bg="#007acc", fg="white", font=("Arial", 10, "bold"))
 search_btn.grid(row=0, column=4, rowspan=2, padx=10)

 # --- Table Section ---
 table_frame = tk.Frame(root)
 table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

 scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
 scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)

 columns = (
    "FIR Number", "Date of Report", "Investigator",
    "Physical Evidence", "Digital Evidence", "Documentary Evidence", "Findings"
 )
 tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                    yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

 scroll_y.config(command=tree.yview)
 scroll_x.config(command=tree.xview)
 scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
 scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

 for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=160)

 tree.pack(fill=tk.BOTH, expand=True)

 # --- Initial Load ---
 load_data()

 root.mainloop()

if __name__ == "__main__":
    main_archive()