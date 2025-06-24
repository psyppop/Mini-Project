import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

def setup_database():
    try:
        # Connect to MySQL server
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootsavio321",
            auth_plugin='mysql_native_password'
        )
        cursor = conn.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS fms")
        cursor.execute("USE fms")

        # Create cases table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                case_id INT AUTO_INCREMENT PRIMARY KEY,
                investigator_id INT,
                description TEXT,
                status VARCHAR(50),
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                title VARCHAR(255) NOT NULL
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        
    except Error as e:
        print(f"Error setting up database: {e}")

class CaseDeletionTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Police Investigation Report - Case Deletion Tool")
        self.root.attributes("-fullscreen", True)
        
        # Exit fullscreen on Escape
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2A3B5F')  # Light blue background
        self.style.configure('TLabel', background='#2A3B5F', foreground='#AFCBE3', font=('Segoe UI', 10))  # Slightly lighter blue text
        self.style.configure('TButton', font=('Segoe UI', 10), padding=5)
        self.style.configure('Header.TLabel', background='#2A3B5F', foreground='#AFCBE3', font=('Segoe UI', 14, 'bold'))  # Slightly lighter blue for headers
        self.style.configure('Treeview', font=('Segoe UI', 9), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'), background='#2A3B5F', foreground='#AFCBE3')  # Consistent with headers

        # Main layout
        self.main_frame = ttk.Frame(root, style='TFrame')  # Updated to use the light blue background
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.header_frame = ttk.Frame(self.main_frame, style='TFrame')  # Updated to use the light blue background
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(self.header_frame, text="POLICE INVESTIGATION REPORT", style='Header.TLabel').pack()
        ttk.Label(self.header_frame, text="Case Deletion Tool", style='Header.TLabel').pack()
        
        # Search section
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.search_frame, text="Search Case ID:").pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(self.search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        self.search_btn = ttk.Button(self.search_frame, text="Search", command=self.search_cases)
        self.search_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.show_all_btn = ttk.Button(self.search_frame, text="Show All", command=self.load_all_cases)
        self.show_all_btn.pack(side=tk.LEFT)
        
        # Treeview
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.tree = ttk.Treeview(self.tree_frame, columns=('case_id', 'title', 'status', 'created_date'), selectmode='browse')
        self.tree.heading('#0', text='ID')
        self.tree.heading('case_id', text='Case ID')
        self.tree.heading('title', text='Title')
        self.tree.heading('status', text='Status')
        self.tree.heading('created_date', text='Created Date')
        
        self.tree.column('#0', width=50, stretch=tk.NO)
        self.tree.column('case_id', width=100)
        self.tree.column('title', width=300)
        self.tree.column('status', width=100)
        self.tree.column('created_date', width=150)
        
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
        
        self.exit_btn = ttk.Button(self.button_frame, text="Exit", command=self.exit_application)
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
                password='rootsavio321',
                database='fms'
            )
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to database:\n{e}")
            self.root.quit()

    def load_all_cases(self):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT case_id, title, status, created_date 
                FROM cases 
                ORDER BY created_date DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            
            self.update_treeview(rows)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load cases:\n{e}")

    def search_cases(self):
        search_term = self.search_entry.get()
        if not search_term:
            self.load_all_cases()
            return
        
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT case_id, title, status, created_date 
                FROM cases 
                WHERE case_id LIKE %s OR title LIKE %s
                ORDER BY created_date DESC
            """
            cursor.execute(query, (f'%{search_term}%', f'%{search_term}%'))
            rows = cursor.fetchall()
            
            self.update_treeview(rows)
            
            if not rows:
                messagebox.showinfo("No Results", "No cases found matching the search term.")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to search cases:\n{e}")

    def update_treeview(self, rows):
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', 'end', iid=row[0], text=row[0], values=(row[0], row[1], row[2], row[3]))

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
        
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to permanently delete case:\nCase ID: {case_id}\n\nThis action cannot be undone!",
            icon='warning'
        )
        
        if not confirm:
            return
        
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM cases WHERE case_id = %s"
            cursor.execute(query, (case_id,))
            self.connection.commit()
            
            messagebox.showinfo("Success", f"Case {case_id} has been permanently deleted.")
            self.load_all_cases()
            self.delete_btn.config(state=tk.DISABLED)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to delete case:\n{e}")

    def __del__(self):
        """Safely close database connection"""
        try:
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except Exception:
            pass  # Ignore any errors during cleanup

    def exit_application(self):
        """Close only the current window"""
        try:
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except Exception:
            pass
        self.root.destroy()  # Only destroy the current window instead of quitting

def main():
    setup_database()
    root = tk.Tk()
    app = CaseDeletionTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()