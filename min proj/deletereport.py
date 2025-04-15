import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class CaseDeletionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Police Investigation Report - Case Deletion Tool")
        self.root.attributes("-fullscreen", True)  # Fullscreen enabled
        
        # Exit fullscreen on Escape
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10), padding=5)
        self.style.configure('Header.TLabel', font=('Helvetica', 14, 'bold'))
        self.style.configure('Treeview', font=('Helvetica', 9), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
        self.style.map('TButton',
                      foreground=[('active', 'black'), ('disabled', 'gray')],
                      background=[('active', '#d9d9d9'), ('disabled', '#f0f0f0')])
        
        # Main layout
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(self.header_frame, text="POLICE INVESTIGATION REPORT", style='Header.TLabel').pack()
        ttk.Label(self.header_frame, text="Case Deletion Tool").pack()
        
        # Search section
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.search_frame, text="Search FIR Number:").pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(self.search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_btn = ttk.Button(self.search_frame, text="Search", command=self.search_cases)
        self.search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.show_all_btn = ttk.Button(self.search_frame, text="Show All", command=self.load_all_cases)
        self.show_all_btn.pack(side=tk.LEFT)
        
        # Treeview
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=('fir', 'title', 'station', 'date'), selectmode='browse')
        self.tree.heading('#0', text='ID')
        self.tree.heading('fir', text='FIR Number')
        self.tree.heading('title', text='Case Title')
        self.tree.heading('station', text='Police Station')
        self.tree.heading('date', text='Report Date')
        
        self.tree.column('#0', width=50, stretch=tk.NO)
        self.tree.column('fir', width=120)
        self.tree.column('title', width=250)
        self.tree.column('station', width=150)
        self.tree.column('date', width=100)
        
        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.delete_btn = ttk.Button(self.button_frame, text="Delete Selected Case", 
                                     command=self.delete_case, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.refresh_btn = ttk.Button(self.button_frame, text="Refresh", command=self.load_all_cases)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.exit_btn = ttk.Button(self.button_frame, text="Exit", command=root.quit)
        self.exit_btn.pack(side=tk.RIGHT)
        
        # Database connection
        self.connection = None
        self.connect_to_db()
        
        # Event binding
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        # Initial load
        self.load_all_cases()
    
    def connect_to_db(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='your_password',  # Change this
                database='reports'
            )
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{e}")
            self.root.quit()
    
    def load_all_cases(self):
        self.search_entry.delete(0, tk.END)
        self.populate_treeview()
    
    def search_cases(self):
        search_term = self.search_entry.get()
        if not search_term:
            self.load_all_cases()
            return
        
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT id, firNumber, caseTitle, policeStation, dateOfReport 
                FROM reports 
                WHERE firNumber LIKE %s
                ORDER BY dateOfReport DESC
            """
            cursor.execute(query, (f'%{search_term}%',))
            rows = cursor.fetchall()
            
            self.update_treeview(rows)
            
            if not rows:
                messagebox.showinfo("No Results", "No cases found matching the search term.")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to search cases:\n{e}")
    
    def populate_treeview(self):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT id, firNumber, caseTitle, policeStation, dateOfReport 
                FROM reports 
                ORDER BY dateOfReport DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            self.update_treeview(rows)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load cases:\n{e}")
    
    def update_treeview(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', 'end', iid=row[0], text=row[0], values=(row[1], row[2], row[3], row[4]))
    
    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.delete_btn.config(state=tk.DISABLED)
    
    def delete_case(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        case_id = selected_item[0]
        fir_number = self.tree.item(selected_item)['values'][0]
        
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete case:\nFIR Number: {fir_number}\n\nThis action cannot be undone!",
            icon='warning'
        )
        
        if not confirm:
            return
        
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM reports WHERE id = %s"
            cursor.execute(query, (case_id,))
            self.connection.commit()
            
            messagebox.showinfo("Success", f"Case {fir_number} has been permanently deleted.")
            self.load_all_cases()
            self.delete_btn.config(state=tk.DISABLED)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to delete case:\n{e}")
    
    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaseDeletionTool(root)
    root.mainloop()
