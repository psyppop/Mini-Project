from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from chat_dash_face import ForenSyncDashboard

def open_supervisor_page(app):
    create_login_form(app, "Supervisor")

def open_investigator_page(app):
    create_login_form(app, "Investigator")

def open_facility_page(app):
    create_login_form(app, "Facility")

def open_guest_page(app):
    create_login_form(app, "Guest")

def create_login_form(app, login_type):
    app.clear_window()
    app.create_background()
    app.create_header()

    login_frame = Frame(app.root, bg="#201E43", width=250, height=250)
    login_frame.place(relx=0.5, rely=0.6, anchor="center")
    login_frame.pack_propagate(False)

    login_label = Label(login_frame, bg="#201E43", fg="#91DDCF", font=("Arial", 16, "bold"), text=f"{login_type} Login")
    login_label.pack(padx=10, pady=27)

    app.username_entry = Entry(login_frame, bg="#91DDCF", fg="#201E43", font=("Arial", 12), width=15)
    app.username_entry.insert(0, "Username")
    app.username_entry.bind("<FocusIn>", app.clear_username_placeholder)
    app.username_entry.bind("<FocusOut>", app.restore_username_placeholder)
    app.username_entry.pack(pady=10)

    app.password_entry = Entry(login_frame, bg="#91DDCF", fg="#201E43", font=("Arial", 12), width=15)
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

    if username and password:
        conn = None
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="forensync"
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
                    ForenSyncDashboard(app.root, username, "supervisor")
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