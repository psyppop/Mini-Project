import tkinter as tk
from tkinter import ttk, messagebox, Label, Frame, Button, Tk, LEFT
from PIL import Image, ImageTk
import os
import tkinter.font as tkfont
from face_img import facemain, mainimg
from chat import mainchat
from case_m import Forensyncapp
from graph import graph

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
        self.set_background_image(r"C:\Users\Savio\Desktop\min proj\bg.png")
        
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

        img_path = r"C:\Users\Savio\Desktop\min proj\F_resized1.png"
        try:
            img = Image.open(img_path)
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

    def open_case_management(self):
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
            ("📷  FACIAL ANALYSIS", lambda: facemain(self.root))
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

def dash(username="Investigator", user_type="investigator"):
    root = Tk()
    ForenSyncDashboard(root, username, user_type)
    
    try:
        root.iconbitmap(r"C:\Users\Savio\Desktop\min proj\icon.ico")
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    dash()