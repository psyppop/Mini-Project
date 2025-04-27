from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from login_func import open_supervisor_page, open_investigator_page, open_facility_page, open_guest_page, open_admin_page, setup_database

class RoundedButton(Canvas):
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

class ForensicManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ForenSync")
        self.root.geometry("2560x1440")
        self.root.attributes("-fullscreen", True)
        
        # Setup database before creating the home page
        setup_database()
        self.create_home_page()

        # Bind keys for fullscreen toggle and quit
        self.root.bind("<Escape>", self.toggle_fullscreen)
        self.root.bind("<Control-q>", self.quit_application)

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        return "break"

    def quit_application(self, event=None):
        self.root.destroy()

    def create_home_page(self):
        # Clear the current window
        self.clear_window()

        # Create background and header
        self.create_background()
        self.create_header()

        # Main container for buttons
        main_frame = Frame(self.root, bg="#201E43")
        main_frame.place(relx=0.5, rely=0.5, anchor="center", width=800, height=500)

        # Title
        title_label = Label(main_frame, text="Select Role", 
                          font=("Segoe UI", 24, "bold"),
                          bg="#201E43", fg="#91DDCF")
        title_label.pack(pady=(0, 20))

        # Button container with scrollbar
        canvas = Canvas(main_frame, bg="#201E43", highlightthickness=0)
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="#201E43")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Create buttons with RoundedButton style
        buttons = [
            ("👤  ADMIN", lambda: open_admin_page(self)),
            ("👨‍💼  SUPERVISOR", lambda: open_supervisor_page(self)),
            ("🔍  INVESTIGATOR", lambda: open_investigator_page(self)),
            ("👥  FACILITATOR", lambda: open_facility_page(self)),
            ("👤  GUEST", lambda: open_guest_page(self))
        ]

        # Create a frame to center the buttons
        center_frame = Frame(scrollable_frame, bg="#201E43")
        center_frame.pack(expand=True, fill="both")

        for text, command in buttons:
            btn = RoundedButton(
                center_frame,
                text=text,
                btnbackground="#4A6FA5",
                btnforeground="#FFFFFF",
                clicked=command,
                height=55,
                width=350,
                font_size=15
            )
            btn.pack(pady=12)
            btn.draw_button()

        # Center the scrollable frame in the canvas
        canvas.create_window((400, 0), window=scrollable_frame, anchor="n", width=800)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_background(self):
        img_path1 = "bg.png"  # Using relative path
        try:
            img1 = Image.open(img_path1)
            img1 = img1.resize((2560, 1440), Image.Resampling.LANCZOS)
            self.photo1 = ImageTk.PhotoImage(img1)

            img_label1 = Label(self.root, image=self.photo1)
            img_label1.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print(f"Background image {img_path1} not found. Using default background color.")
            self.root.configure(bg="#201E43")  # Using the same color as the header

    def create_header(self):
        header_frame = Frame(self.root, bg="#201E43", padx=10, pady=20)
        header_frame.pack(fill=X)

        img_path = "F_resized1.png"  # Using relative path
        try:
            img = Image.open(img_path)
            img = img.resize((400, 120), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            img_label = Label(header_frame, image=photo, bg="#201E43")
            img_label.image = photo
            img_label.pack(side=LEFT, padx=5)
        except FileNotFoundError:
            print(f"Logo image {img_path} not found. Using text header instead.")
            title_label = Label(header_frame, text="ForenSync", font=("Arial", 24, "bold"), fg="white", bg="#201E43")
            title_label.pack(side=LEFT, padx=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_username_placeholder(self, event):
        if self.username_entry.get() == "Username":
            self.username_entry.delete(0, END)

    def restore_username_placeholder(self, event):
        if self.username_entry.get() == "":
            self.username_entry.insert(0, "Username")

    def clear_password_placeholder(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, END)
            self.password_entry.config(show="*")

    def restore_password_placeholder(self, event):
        if self.password_entry.get() == "":
            self.password_entry.insert(0, "Password")

    def open_dashboard(self, user_type):
        self.clear_window()
        # Logic to open the dashboard for the respective user
        Label(self.root, text=f"Welcome to {user_type} Dashboard", font=("Arial", 20)).pack()

def main():
    try:
        root = Tk()
        app = ForensicManagementApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror("Error", f"Failed to start application: {e}")

if __name__ == "__main__":
    main()