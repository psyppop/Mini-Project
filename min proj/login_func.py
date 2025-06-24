from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from dashboard import ForenSyncDashboard
from facilitator_dash import fac_dash
from supervisor_dash import ForenSyncDashboard2

def open_supervisor_page(app):
    create_login_form(app, "Supervisor")

def open_investigator_page(app):
    create_login_form(app, "Investigator")

def open_facility_page(app):
    create_login_form(app, "Facilitator")

def open_guest_page(app):
    create_login_form(app, "Guest")

def open_admin_page(app):
    create_login_form(app, "Admin")

def create_login_form(app, login_type):
    app.clear_window()
    app.create_background()
    app.create_header()

    login_frame = Frame(app.root, bg="#201E43", width=300, height=300)
    login_frame.place(relx=0.5, rely=0.6, anchor="center")
    login_frame.pack_propagate(False)

    login_label = Label(login_frame, bg="#201E43", fg="#91DDCF", font=("Arial", 16, "bold"), text=f"{login_type} Login")
    login_label.pack(padx=8, pady=30)

    app.username_entry = Entry(login_frame, bg="#91DDCF", fg="#201E43", font=("Arial", 12), width=16)
    app.username_entry.insert(0, "Username")
    app.username_entry.bind("<FocusIn>", app.clear_username_placeholder)
    app.username_entry.bind("<FocusOut>", app.restore_username_placeholder)
    app.username_entry.pack(pady=10)

    app.password_entry = Entry(login_frame, bg="#91DDCF", fg="#201E43", font=("Arial", 12), width=16)
    app.password_entry.insert(0, "Password")
    app.password_entry.bind("<FocusIn>", app.clear_password_placeholder)
    app.password_entry.bind("<FocusOut>", app.restore_password_placeholder)
    app.password_entry.pack(pady=10)

    button_frame = Frame(login_frame, bg="#201E43")
    button_frame.pack(pady=20)

    Button(button_frame, text="Login", fg="#91DDCF", font=("Arial", 12, "bold"), bg="#201E43",
           command=lambda: login(app, login_type)).grid(row=5, column=0, padx=10)

    Button(button_frame, text="Back", fg="#91DDCF", font=("Arial", 12, "bold"), bg="#201E43",
           command=app.create_home_page).grid(row=5, column=1, padx=10)

def login(app, login_type):
    username = app.username_entry.get()
    password = app.password_entry.get()
    login_type = login_type.lower()

    if username and password:
        conn = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="fms",
                auth_plugin='mysql_native_password'
            )
            cursor = conn.cursor()

            if login_type.lower() == "investigator":
                cursor.execute(
                    "SELECT * FROM investigator WHERE username = %s AND password = %s",
                    (username, password)
                )
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Login Successful", "Logged in Successfully!")
                    ForenSyncDashboard(app.root, username, "investigator")
                else:
                    messagebox.showerror("Login Error", "Invalid Username or Password.")
            
            elif login_type.lower() == "supervisor":
                cursor.execute(
                    "SELECT * FROM supervisor WHERE username = %s AND password = %s",
                    (username, password)
                )
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Login Successful", "Welcome Supervisor!")
                    ForenSyncDashboard2(app.root, username, "supervisor")
                else:
                    messagebox.showerror("Login Error", "Invalid Username or Password.")
            
            elif login_type.lower() == "admin":
                cursor.execute(
                    "SELECT * FROM admin WHERE username = %s AND password = %s",
                    (username, password)
                )
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Login Successful", "You've Succesfully Logged In!")
                    from dashboard import AdminDashboard
                    AdminDashboard(app.root, username)
                else:
                    messagebox.showerror("Login Error", "Invalid Username or Password.")

            elif login_type == "facilitator":
             cursor.execute(
             "SELECT * FROM facilitator WHERE username = %s AND password = %s",
             (username, password)
             )
             user = cursor.fetchone()

             if user:
              messagebox.showinfo("Login Successful", "Welcome Facilitator!")
              app.root.destroy()
              root = Tk()
              from facilitator_dash import ForenSyncFacilitatorDashboard
              dashboard = ForenSyncFacilitatorDashboard(root, username, "facilitator")
              root.mainloop()
             else:
              messagebox.showerror("Login Error", "Invalid Username or Password.")

            elif login_type == "guest":
                cursor.execute(
                    "SELECT * FROM guest WHERE username = %s AND password = %s",
                    (username, password)
                )
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Login Successful", "Welcome Guest!")
                    app.root.destroy()  # Close the current window
                    from guest_dash import start_guest_dashboard
                    start_guest_dashboard(username, "guest")  # Start the guest dashboard
                else:
                    messagebox.showerror("Login Error", "Invalid Username or Password.")
                    
        except Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields.")

# Placeholder functions for other dashboards
def open_investigator_dashboard(self):
    pass

def open_supervisor_dashboard(self):
    pass

def open_facility_dashboard(self):
    pass

def open_guest_dashboard(self):
    pass

def open_admin_dashboard(self):
    pass

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

        # Create admin table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Create supervisor table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS supervisor (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Create investigator table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS investigator (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Create facilitator table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facilitator (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Create guest table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guest (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        # Add default admin user if not exists
        cursor.execute("SELECT * FROM admin WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute(
                "INSERT INTO admin (username, password) VALUES (%s, %s)",
                ("admin", "admin123")
            )

        conn.commit()
        
        
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error setting up database: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Call setup_database at the start of your application
setup_database()

'''def create_home_page(self):
    # Clear the current window
    self.clear_window()

    self.root.configure(bg="white")

    # Create background and header
    self.create_background()
    self.create_header()

    # Create buttons for different roles
    button_frame = Frame(self.root, bg="#201E43", padx=40, pady=40)
    button_frame.place(relx=0.5, rely=0.5, anchor="center")

    title_label = Label(button_frame, text="Role", font=("Arial", 24, "bold"), 
                      fg="#91DDCF", bg="#201E43")
    title_label.pack(pady=(0, 30))

    # Define button styles
    button_style = {
        "font": ("Arial", 14, "bold"),
        "width": 15,
        "fg": "#91DDCF",
        "bg": "#201E43",
        "pady": 10
    }

    # Create buttons for different roles
    supervisor_btn = Button(button_frame, text="Supervisor", 
                          command=lambda: open_supervisor_page(self), **button_style)
    supervisor_btn.pack(pady=10)

    investigator_btn = Button(button_frame, text="Investigator", 
                            command=lambda: open_investigator_page(self), **button_style)
    investigator_btn.pack(pady=10)

    facility_btn = Button(button_frame, text="Facilitator", 
                        command=lambda: open_facility_page(self), **button_style)
    facility_btn.pack(pady=10)

    guest_btn = Button(button_frame, text="Guest", 
                     command=lambda: open_guest_page(self), **button_style)
    guest_btn.pack(pady=10)'''