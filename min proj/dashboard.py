import tkinter as tk
from tkinter import ttk, messagebox, Label, Frame, Button, Tk, LEFT, Toplevel, StringVar, BooleanVar, Checkbutton, LabelFrame, END, BOTH, Canvas, Scrollbar, FLAT
from PIL import Image, ImageTk
import os
import tkinter.font as tkfont
from face_img import facemain, mainimg
from finalchat import mainchat
from case_m import Forensyncapp
from graph import graph
import mysql.connector

class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", radius=25, btnforeground="#000000", btnbackground="#ffffff", 
                 clicked=None, font_size=14, *args, **kwargs):
        super(RoundedButton, self).__init__(master, *args, **kwargs)
        self.config(bg=self.master["bg"], highlightthickness=0)
        self.btnbackground = btnbackground
        self.btnforeground = btnforeground
        self.clicked = clicked
        self.radius = radius
        self.font_size = font_size
        self.text = text
        
        self.rect_id = None
        self.text_id = None
        
        self.bind("<Configure>", self.draw_button)
        self.bind("<ButtonPress-1>", self.bpress)
        self.bind("<ButtonRelease-1>", self.brelease)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def draw_button(self, event=None):
        width = self.winfo_width()
        height = self.winfo_height()
        
        if width <= 1 or height <= 1:
            return
            
        self.delete("all")
        self.rect_id = self.create_round_rect(0, 0, width, height, radius=self.radius, fill=self.btnbackground)
        self.text_id = self.create_text(width/2, height/2, 
                                      text=self.text, 
                                      fill=self.btnforeground, 
                                      font=("Segoe UI", self.font_size, "bold"),
                                      tags="text")
        
    def create_round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                 x1+radius, y1,
                 x2-radius, y1,
                 x2-radius, y1,
                 x2, y1,
                 x2, y1+radius,
                 x2, y1+radius,
                 x2, y2-radius,
                 x2, y2-radius,
                 x2, y2,
                 x2-radius, y2,
                 x2-radius, y2,
                 x1+radius, y2,
                 x1+radius, y2,
                 x1, y2,
                 x1, y2-radius,
                 x1, y2-radius,
                 x1, y1+radius,
                 x1, y1+radius,
                 x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)
    
    def bpress(self, event):
        if self.rect_id:
            self.itemconfig(self.rect_id, fill=self.btnbackground)
        if self.clicked:
            self.clicked()
            
    def brelease(self, event):
        if self.rect_id:
            self.itemconfig(self.rect_id, fill=self.btnbackground)
        
    def on_enter(self, event):
        if self.rect_id:
            self.itemconfig(self.rect_id, fill="#7FB2E5")
        
    def on_leave(self, event):
        if self.rect_id:
            self.itemconfig(self.rect_id, fill=self.btnbackground)

class ForenSyncDashboard:
    def __init__(self, root, username, user_type="investigator"):
        self.root = root
        self.username = username
        self.user_type = user_type.lower()
        self.images = []
        
        # Configure the root window
        self.root.title("ForenSync Dashboard")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))
        
        # Set background image
        self.set_background_image("bg.png")
        
        # Setup styles and UI elements
        self.setup_styles()
        self.create_header()
        self.create_main_content()

    def set_background_image(self, image_path):
        try:
            bg_image = Image.open(image_path)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg_image)
            self.images.append(self.bg_image)
            bg_label = Label(self.root, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.root.configure(bg='#0F0E26')

    def setup_styles(self):
        self.bg_color = '#201E43'
        self.card_color = '#1A1A3A'
        self.primary_color = '#4A6FA5'
        self.accent_color = '#6D9DC5'
        self.text_color = '#FFFFFF'
        self.highlight_color = '#7FB2E5'
        
        self.header_font = tkfont.Font(family="Segoe UI", size=24, weight="bold")
        self.button_font_size = 16
        self.welcome_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)

    def create_header(self):
        header_frame = Frame(self.root, bg=self.bg_color, padx=30, pady=20)
        header_frame.place(x=0, y=0, relwidth=1, height=140)
        
        separator = Frame(self.root, bg=self.primary_color, height=2)
        separator.place(x=0, y=140, relwidth=1)

        try:
            img = Image.open("F_resized1.png")
            img = img.resize((380, 114), Image.Resampling.LANCZOS)
            self.header_image = ImageTk.PhotoImage(img)
            self.images.append(self.header_image)
            img_label = Label(header_frame, image=self.header_image, bg=self.bg_color)
            img_label.pack(side=LEFT, padx=20)
        except Exception as e:
            print(f"Error loading header image: {e}")
            header_label = Label(header_frame, text="ForenSync", font=self.header_font, bg=self.bg_color, fg=self.text_color)
            header_label.pack(side=LEFT, padx=20)

        logout_btn = Button(
            header_frame, 
            text="LOGOUT", 
            bg=self.bg_color,
            fg=self.text_color, 
            font=("Segoe UI", 14, "bold"),
            padx=20,
            pady=6,
            borderwidth=0,
            relief="flat",
            cursor="hand2",
            activebackground=self.bg_color,
            activeforeground=self.accent_color,
            command=self.logout
        )
        logout_btn.pack(side=tk.RIGHT, padx=30)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            root = Tk()
            from Main import ForensicManagementApp
            ForensicManagementApp(root)
            root.mainloop()

    def open_case_management(self):
        self.log_activity(self.username, "Accessed case management system")
        self.root.withdraw()
        case_management_window = tk.Toplevel(self.root)
        case_management_window.title("Case Management")
        case_management_window.geometry("1024x768")
        case_management_app = Forensyncapp(case_management_window)
        case_management_window.protocol("WM_DELETE_WINDOW", 
                                     lambda: self.on_case_management_close(case_management_window))

    def on_case_management_close(self, case_management_window):
        case_management_window.destroy()
        self.root.deiconify()

    def show_restricted_statistics(self):
        messagebox.showerror("Access Denied", "Statistics feature is only available to Supervisors")

    def show_statistics(self):
        if self.user_type == "supervisor":
            graph_instance = graph()
            graph_instance.generate_graph()
        else:
            self.show_restricted_statistics()

    def create_main_content(self):
        main_frame = Frame(self.root, bg=self.card_color)
        main_frame.place(x=100, y=180, relwidth=0.8, height=550, anchor='nw')
        
        welcome_panel = Frame(main_frame, bg=self.primary_color)
        welcome_panel.pack(fill='x', pady=(0, 20))
        
        welcome_label = Label(
            welcome_panel, 
            text=f"Welcome, {self.username} ({self.user_type.title()})",
            bg=self.primary_color, 
            fg=self.text_color, 
            font=self.welcome_font,
            padx=25,
            pady=12,
            anchor='w'
        )
        welcome_label.pack(fill='x')
        
        subtitle = Label(
            welcome_panel,
            text="DIGITAL FORENSICS DASHBOARD",
            bg=self.primary_color,
            fg=self.accent_color,
            font=self.subtitle_font,
            padx=25,
            anchor='w'
        )
        subtitle.pack(fill='x', pady=(0, 12))

        button_container = Frame(main_frame, bg=self.card_color, padx=25, pady=15)
        button_container.pack(fill='both', expand=True)

        buttons = [
            ("📁  CASE MANAGEMENT", self.open_case_management),
            ("📊  STATISTICS", self.show_statistics if self.user_type == "supervisor" else self.show_restricted_statistics),
            ("💬  CHAT", lambda: mainchat()),
            ("📷  FACIAL ANALYSIS", lambda: self.open_facial_analysis())
        ]
        
        for text, command in buttons:
            btn_frame = Frame(button_container, bg=self.card_color)
            btn_frame.pack(fill='x', pady=10)
            
            btn = RoundedButton(
                btn_frame,
                text=text,
                btnbackground=self.primary_color,
                btnforeground=self.text_color,
                clicked=command,
                height=70,
                font_size=self.button_font_size
            )
            btn.pack(fill='x')
            btn.draw_button()

    def open_facial_analysis(self):
        """Open facial analysis window while hiding the dashboard"""
        self.root.withdraw()  # Hide the dashboard
        face_window = Toplevel(self.root)
        face_window.protocol("WM_DELETE_WINDOW", lambda: self.on_face_window_close(face_window))
        facemain(face_window, self.root)  # Pass both windows to facemain

    def on_face_window_close(self, face_window):
        """Handle facial analysis window closing"""
        face_window.destroy()
        self.root.deiconify()  # Show the dashboard again

    def log_activity(self, username, action):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="fms"
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO activity_log (username, action)
                VALUES (%s, %s)
            """, (username, action))
            
            conn.commit()
            
        except mysql.connector.Error as err:
            print(f"Error logging activity: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def save_user(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="fms"
            )
            cursor = conn.cursor()
            
            # Insert into users table
            cursor.execute("""
                INSERT INTO users (name, username, password, role, is_active) 
                VALUES (%s, %s, %s, %s, %s)
            """, (self.name_entry.get(), self.username_entry.get(), self.password_entry.get(), 
                 self.role_var.get().lower(), self.active_var.get()))
            
            user_id = cursor.lastrowid
            
            # Insert into permissions table
            cursor.execute("""
                INSERT INTO permissions (user_id, can_view, can_upload, can_edit)
                VALUES (%s, %s, %s, %s)
            """, (user_id, self.can_view_var.get(), self.can_upload_var.get(), self.can_edit_var.get()))
            
            # Insert into role-specific table based on role
            role = self.role_var.get().lower()
            if role == "investigator":
                cursor.execute("""
                    INSERT INTO investigator (username, password)
                    VALUES (%s, %s)
                """, (self.username_entry.get(), self.password_entry.get()))
            elif role == "supervisor":
                cursor.execute("""
                    INSERT INTO supervisor (username, password)
                    VALUES (%s, %s)
                """, (self.username_entry.get(), self.password_entry.get()))
            elif role == "facilitator":
                cursor.execute("""
                    INSERT INTO facilitator (username, password)
                    VALUES (%s, %s)
                """, (self.username_entry.get(), self.password_entry.get()))
            elif role == "guest":
                cursor.execute("""
                    INSERT INTO guest (username, password)
                    VALUES (%s, %s)
                """, (self.username_entry.get(), self.password_entry.get()))
            
            # Log the activity
            self.log_activity(self.username, f"Created new {role} user: {self.username_entry.get()}")
            
            conn.commit()
            messagebox.showinfo("Success", "User created successfully!")
            self.window.destroy()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def toggle_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user")
            return
            
        user_id = self.tree.item(selected[0])['values'][0]
        username = self.tree.item(selected[0])['values'][2]
        current_status = self.tree.item(selected[0])['values'][4]
        new_status = "Inactive" if current_status == "Active" else "Active"
        
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="fms"
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users 
                SET is_active = %s 
                WHERE id = %s
            """, (new_status, user_id))
            
            # Log the activity
            self.log_activity(self.username, f"Changed status of user {username} to {new_status}")
            
            conn.commit()
            self.refresh_users()
            messagebox.showinfo("Success", "User status updated!")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def handle_login(self):
        role = self.role_var.get()
        username = self.username_entry.get()
        
        if role == "Select Role":
            messagebox.showerror("Error", "Please select a role")
            return
        
        # ... existing login code ...
        
        # Log the login activity
        self.log_activity(username, f"Logged in as {role}")
        
        self.clear_window()
        # ... rest of login code ...

    def face_recognition(self):
        self.log_activity(self.username, "Accessed face recognition system")
        facemain()

    def open_chat(self):
        self.log_activity(self.username, "Accessed chat system")
        mainchat()

    def upload_file(self, filename):
        self.log_activity(self.username, f"Uploaded file: {filename}")
        # ... existing upload code ...

    def update_permissions(self, target_username, permissions):
        permission_str = ", ".join([p for p, enabled in permissions.items() if enabled])
        self.log_activity(self.username, f"Updated permissions for {target_username}: {permission_str}")
        # ... existing permission update code ...

    def view_logs_window(self):
        logs_window = Toplevel(self.root)
        logs_window.title("Activity Logs")
        logs_window.geometry("800x600")
        logs_window.configure(bg=self.bg_color)
        
        # Create header
        header = Frame(logs_window, bg=self.primary_color, height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        Label(
            header,
            text="Activity Logs",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg=self.primary_color
        ).pack(side='left', padx=20)
        
        # Create main content area
        main_frame = Frame(logs_window, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create logs display area
        logs_frame = Frame(main_frame, bg=self.card_color)
        logs_frame.pack(fill='both', expand=True)
        
        # Create scrollable canvas
        canvas = Canvas(logs_frame, bg=self.card_color, highlightthickness=0)
        scrollbar = Scrollbar(logs_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=self.card_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        def refresh_logs():
            # Clear existing logs
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            # Get logs from database
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="rootsavio321",
                    database="fms"
                )
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, username, action, timestamp 
                    FROM activity_log 
                    ORDER BY timestamp DESC
                """)
                
                for row in cursor.fetchall():
                    log_frame = Frame(scrollable_frame, bg=self.card_color)
                    log_frame.pack(fill='x', pady=5, padx=10)
                    
                    # Create log entry
                    log_text = f"{row[1]} - {row[2]}"
                    timestamp = row[3].strftime('%Y-%m-%d %H:%M:%S')
                    
                    Label(
                        log_frame,
                        text=log_text,
                        font=("Segoe UI", 11),
                        fg="white",
                        bg=self.card_color,
                        anchor='w'
                    ).pack(fill='x')
                    
                    Label(
                        log_frame,
                        text=timestamp,
                        font=("Segoe UI", 9),
                        fg="#888888",
                        bg=self.card_color,
                        anchor='w'
                    ).pack(fill='x')
                    
                    # Add separator
                    Frame(
                        log_frame,
                        height=1,
                        bg="#333333"
                    ).pack(fill='x', pady=5)
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load logs: {str(e)}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()
        
        # Add refresh button
        refresh_btn = Button(
            main_frame,
            text="Refresh Logs",
            command=refresh_logs,
            font=("Segoe UI", 11),
            bg="#4CAF50",
            fg="white",
            relief=FLAT,
            padx=20,
            pady=5
        )
        refresh_btn.pack(pady=10)
        
        # Initial load of logs
        refresh_logs()
        
        # Configure window close behavior
        logs_window.protocol("WM_DELETE_WINDOW", lambda: self.on_logs_window_close(logs_window))
    
    def on_logs_window_close(self, logs_window):
        logs_window.destroy()

class AdminDashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.images = []
        
        # Configure the root window
        self.root.title("ForenSync Admin Dashboard")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))
        
        # Set background image
        self.set_background_image("bg.png")
        
        # Setup styles and UI elements
        self.setup_styles()
        self.create_header()
        self.create_main_content()

    def set_background_image(self, image_path):
        try:
            bg_image = Image.open(image_path)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg_image)
            self.images.append(self.bg_image)
            bg_label = Label(self.root, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.root.configure(bg='#0F0E26')

    def setup_styles(self):
        self.bg_color = '#201E43'
        self.card_color = '#1A1A3A'
        self.primary_color = '#4A6FA5'
        self.accent_color = '#6D9DC5'
        self.text_color = '#FFFFFF'
        self.highlight_color = '#7FB2E5'
        
        self.header_font = tkfont.Font(family="Segoe UI", size=24, weight="bold")
        self.button_font_size = 16
        self.welcome_font = tkfont.Font(family="Segoe UI", size=20, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)

    def create_header(self):
        header_frame = Frame(self.root, bg=self.bg_color, padx=30, pady=20)
        header_frame.place(x=0, y=0, relwidth=1, height=140)
        
        separator = Frame(self.root, bg=self.primary_color, height=2)
        separator.place(x=0, y=140, relwidth=1)

        try:
            img = Image.open("F_resized1.png")
            img = img.resize((380, 114), Image.Resampling.LANCZOS)
            self.header_image = ImageTk.PhotoImage(img)
            self.images.append(self.header_image)
            img_label = Label(header_frame, image=self.header_image, bg=self.bg_color)
            img_label.pack(side=LEFT, padx=20)
        except Exception as e:
            print(f"Error loading header image: {e}")
            header_label = Label(header_frame, text="ForenSync", font=self.header_font, bg=self.bg_color, fg=self.text_color)
            header_label.pack(side=LEFT, padx=20)

        logout_btn = Button(
            header_frame, 
            text="LOGOUT", 
            bg=self.bg_color,
            fg=self.text_color, 
            font=("Segoe UI", 14, "bold"),
            padx=20,
            pady=6,
            borderwidth=0,
            relief="flat",
            cursor="hand2",
            activebackground=self.bg_color,
            activeforeground=self.accent_color,
            command=self.logout
        )
        logout_btn.pack(side=tk.RIGHT, padx=30)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            os.system("python Main.py")

    def create_user_window(self):
        window = Toplevel(self.root)
        window.title("Create New User")
        window.geometry("500x600")
        window.configure(bg=self.bg_color)
        
        Label(window, text="Create New User", font=("Segoe UI", 20, "bold"), 
              bg=self.bg_color, fg=self.text_color).pack(pady=20)
        
        # Form Frame
        form_frame = Frame(window, bg=self.bg_color)
        form_frame.pack(padx=40, pady=20)
        
        # Name
        Label(form_frame, text="Name:", bg=self.bg_color, fg=self.text_color, 
              font=("Segoe UI", 12)).grid(row=0, column=0, sticky='w', pady=10)
        name_entry = tk.Entry(form_frame, font=("Segoe UI", 12))
        name_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Username
        Label(form_frame, text="Username:", bg=self.bg_color, fg=self.text_color, 
              font=("Segoe UI", 12)).grid(row=1, column=0, sticky='w', pady=10)
        username_entry = tk.Entry(form_frame, font=("Segoe UI", 12))
        username_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Password
        Label(form_frame, text="Password:", bg=self.bg_color, fg=self.text_color, 
              font=("Segoe UI", 12)).grid(row=2, column=0, sticky='w', pady=10)
        password_entry = tk.Entry(form_frame, font=("Segoe UI", 12), show="*")
        password_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Role
        Label(form_frame, text="Role:", bg=self.bg_color, fg=self.text_color, 
              font=("Segoe UI", 12)).grid(row=3, column=0, sticky='w', pady=10)
        roles = ["Investigator", "Supervisor", "Facilitator", "Guest", "Admin"]
        role_var = StringVar(window)
        role_var.set(roles[0])
        role_menu = ttk.Combobox(form_frame, textvariable=role_var, values=roles, 
                                font=("Segoe UI", 12), state="readonly")
        role_menu.grid(row=3, column=1, pady=10, padx=10)
        
        # Active Status
        active_var = BooleanVar(value=True)
        active_check = Checkbutton(form_frame, text="Active", variable=active_var, 
                                 bg=self.bg_color, fg=self.text_color, 
                                 selectcolor=self.primary_color,
                                 font=("Segoe UI", 12))
        active_check.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Permissions Frame
        perm_frame = LabelFrame(form_frame, text="Permissions", bg=self.bg_color, 
                              fg=self.text_color, font=("Segoe UI", 12))
        perm_frame.grid(row=5, column=0, columnspan=2, pady=20, sticky='ew')
        
        # Permission checkboxes
        can_view_var = BooleanVar(value=True)
        can_upload_var = BooleanVar(value=False)
        can_edit_var = BooleanVar(value=False)
        
        Checkbutton(perm_frame, text="Can View", variable=can_view_var, 
                   bg=self.bg_color, fg=self.text_color, 
                   selectcolor=self.primary_color,
                   font=("Segoe UI", 11)).pack(anchor='w', pady=5)
        Checkbutton(perm_frame, text="Can Upload", variable=can_upload_var, 
                   bg=self.bg_color, fg=self.text_color, 
                   selectcolor=self.primary_color,
                   font=("Segoe UI", 11)).pack(anchor='w', pady=5)
        Checkbutton(perm_frame, text="Can Edit", variable=can_edit_var, 
                   bg=self.bg_color, fg=self.text_color, 
                   selectcolor=self.primary_color,
                   font=("Segoe UI", 11)).pack(anchor='w', pady=5)
        
        def save_user():
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="rootsavio321",
                    database="fms"
                )
                cursor = conn.cursor()
                
                # Insert into users table
                cursor.execute("""
                    INSERT INTO users (name, username, password, role, is_active) 
                    VALUES (%s, %s, %s, %s, %s)
                """, (name_entry.get(), username_entry.get(), password_entry.get(), 
                     role_var.get().lower(), active_var.get()))
                
                user_id = cursor.lastrowid
                
                # Insert into permissions table
                cursor.execute("""
                    INSERT INTO permissions (user_id, can_view, can_upload, can_edit)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, can_view_var.get(), can_upload_var.get(), can_edit_var.get()))
                
                # Insert into role-specific table based on role
                role = role_var.get().lower()
                if role == "investigator":
                    cursor.execute("""
                        INSERT INTO investigator (username, password)
                        VALUES (%s, %s)
                    """, (username_entry.get(), password_entry.get()))
                elif role == "supervisor":
                    cursor.execute("""
                        INSERT INTO supervisor (username, password)
                        VALUES (%s, %s)
                    """, (username_entry.get(), password_entry.get()))
                elif role == "facilitator":
                    cursor.execute("""
                        INSERT INTO facilitator (username, password)
                        VALUES (%s, %s)
                    """, (username_entry.get(), password_entry.get()))
                elif role == "guest":
                    cursor.execute("""
                        INSERT INTO guest (username, password)
                        VALUES (%s, %s)
                    """, (username_entry.get(), password_entry.get()))
                
                # Log the activity
                self.log_activity(self.username, f"Created new {role} user: {username_entry.get()}")
                
                conn.commit()
                messagebox.showinfo("Success", "User created successfully!")
                window.destroy()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()
        
        # Save Button
        Button(window, text="Save", command=save_user, 
               bg=self.primary_color, fg=self.text_color,
               font=("Segoe UI", 12, "bold"), padx=30).pack(pady=20)

    def manage_users_window(self):
        window = Toplevel(self.root)
        window.title("Manage Users")
        window.geometry("1000x600")
        window.configure(bg=self.bg_color)
        
        Label(window, text="Manage Users", font=("Segoe UI", 20, "bold"), 
              bg=self.bg_color, fg=self.text_color).pack(pady=20)
        
        # Create Treeview
        columns = ("ID", "Name", "Username", "Role", "Status")
        tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
        
        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        tree.pack(padx=20, pady=10, fill=BOTH, expand=True)
        
        # Buttons Frame
        btn_frame = Frame(window, bg=self.bg_color)
        btn_frame.pack(pady=20)
        
        def refresh_users():
            for item in tree.get_children():
                tree.delete(item)
                
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="rootsavio321",
                    database="fms"
                )
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, name, username, role, is_active 
                    FROM users
                    ORDER BY id
                """)
                
                for row in cursor.fetchall():
                    status = "Active" if row[4] else "Inactive"
                    tree.insert("", END, values=(row[0], row[1], row[2], row[3], status))
                    
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()
        
        def toggle_status():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a user")
                return
                
            user_id = tree.item(selected[0])['values'][0]
            username = tree.item(selected[0])['values'][2]
            current_status = tree.item(selected[0])['values'][4]
            new_status = "Inactive" if current_status == "Active" else "Active"
            
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="rootsavio321",
                    database="fms"
                )
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE users 
                    SET is_active = %s 
                    WHERE id = %s
                """, (new_status, user_id))
                
                # Log the activity
                self.log_activity(self.username, f"Changed status of user {username} to {new_status}")
                
                conn.commit()
                refresh_users()
                messagebox.showinfo("Success", "User status updated!")
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Database error: {err}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()
        
        Button(btn_frame, text="Refresh", command=refresh_users,
               bg=self.primary_color, fg=self.text_color,
               font=("Segoe UI", 11)).pack(side=LEFT, padx=10)
               
        Button(btn_frame, text="Toggle Status", command=toggle_status,
               bg=self.primary_color, fg=self.text_color,
               font=("Segoe UI", 11)).pack(side=LEFT, padx=10)
        
        refresh_users()  # Load users when window opens

    def view_logs_window(self):
        logs_window = Toplevel(self.root)
        logs_window.title("Activity Logs")
        logs_window.geometry("800x600")
        logs_window.configure(bg=self.bg_color)
        
        # Create header
        header = Frame(logs_window, bg=self.primary_color, height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        Label(
            header,
            text="Activity Logs",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg=self.primary_color
        ).pack(side='left', padx=20)
        
        # Create main content area
        main_frame = Frame(logs_window, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create logs display area
        logs_frame = Frame(main_frame, bg=self.card_color)
        logs_frame.pack(fill='both', expand=True)
        
        # Create scrollable canvas
        canvas = Canvas(logs_frame, bg=self.card_color, highlightthickness=0)
        scrollbar = Scrollbar(logs_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=self.card_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        def refresh_logs():
            # Clear existing logs
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            # Get logs from database
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="rootsavio321",
                    database="fms"
                )
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, username, action, timestamp 
                    FROM activity_log 
                    ORDER BY timestamp DESC
                """)
                
                for row in cursor.fetchall():
                    log_frame = Frame(scrollable_frame, bg=self.card_color)
                    log_frame.pack(fill='x', pady=5, padx=10)
                    
                    # Create log entry
                    log_text = f"{row[1]} - {row[2]}"
                    timestamp = row[3].strftime('%Y-%m-%d %H:%M:%S')
                    
                    Label(
                        log_frame,
                        text=log_text,
                        font=("Segoe UI", 11),
                        fg="white",
                        bg=self.card_color,
                        anchor='w'
                    ).pack(fill='x')
                    
                    Label(
                        log_frame,
                        text=timestamp,
                        font=("Segoe UI", 9),
                        fg="#888888",
                        bg=self.card_color,
                        anchor='w'
                    ).pack(fill='x')
                    
                    # Add separator
                    Frame(
                        log_frame,
                        height=1,
                        bg="#333333"
                    ).pack(fill='x', pady=5)
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load logs: {str(e)}")
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()
        
        # Add refresh button
        refresh_btn = Button(
            main_frame,
            text="Refresh Logs",
            command=refresh_logs,
            font=("Segoe UI", 11),
            bg="#4CAF50",
            fg="white",
            relief=FLAT,
            padx=20,
            pady=5
        )
        refresh_btn.pack(pady=10)
        
        # Initial load of logs
        refresh_logs()
        
        # Configure window close behavior
        logs_window.protocol("WM_DELETE_WINDOW", lambda: self.on_logs_window_close(logs_window))
    
    def on_logs_window_close(self, logs_window):
        logs_window.destroy()

    def create_main_content(self):
        main_frame = Frame(self.root, bg=self.card_color)
        main_frame.place(x=100, y=180, relwidth=0.8, height=550, anchor='nw')
        
        welcome_panel = Frame(main_frame, bg=self.primary_color)
        welcome_panel.pack(fill='x', pady=(0, 20))
        
        welcome_label = Label(
            welcome_panel, 
            text=f"Welcome, {self.username} (Administrator)",
            bg=self.primary_color, 
            fg=self.text_color, 
            font=self.welcome_font,
            padx=25,
            pady=12,
            anchor='w'
        )
        welcome_label.pack(fill='x')
        
        subtitle = Label(
            welcome_panel,
            text="ADMIN DASHBOARD",
            bg=self.primary_color,
            fg=self.accent_color,
            font=self.subtitle_font,
            padx=25,
            anchor='w'
        )
        subtitle.pack(fill='x', pady=(0, 12))

        button_container = Frame(main_frame, bg=self.card_color, padx=25, pady=15)
        button_container.pack(fill='both', expand=True)

        buttons = [
            ("👤  CREATE USER", self.create_user_window),
            ("👥  MANAGE USERS", self.manage_users_window),
            ("📋  VIEW LOGS", self.view_logs_window),
            ("💬  CHAT", lambda: mainchat())
        ]
        
        for text, command in buttons:
            btn_frame = Frame(button_container, bg=self.card_color)
            btn_frame.pack(fill='x', pady=10)
            
            btn = RoundedButton(
                btn_frame,
                text=text,
                btnbackground=self.primary_color,
                btnforeground=self.text_color,
                clicked=command,
                height=70,
                font_size=self.button_font_size
            )
            btn.pack(fill='x')
            btn.draw_button()

    def log_activity(self, username, action):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="fms"
            )
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO activity_log (username, action)
                VALUES (%s, %s)
            """, (username, action))
            
            conn.commit()
            
        except mysql.connector.Error as err:
            print(f"Error logging activity: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

def dash(username="Investigator", user_type="investigator"):
    root = Tk()
    ForenSyncDashboard(root, username, user_type)
    
    try:
        root.iconbitmap(r"C:\Users\Savio\Desktop\min proj\icon.ico")
    except:
        pass
    
    root.mainloop()

def dash(username="admin", user_type="admin"):
    root = Tk()
    AdminDashboard(root, username)
    
    try:
        root.iconbitmap(r"C:\Users\Savio\Desktop\min proj\icon.ico")
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    dash()