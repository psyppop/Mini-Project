from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from login_func import  open_supervisor_page, open_investigator_page, open_facility_page, open_guest_page

class ForensicManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ForenSync")
        self.root.geometry("2560x1440")
        self.root.attributes("-fullscreen", True)

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

        self.root.configure(bg="white")

        # Create background and header
        self.create_background()
        self.create_header()

        supervisor_button = Button(self.root, text="Supervisor", font=("Arial", 15), fg="#91DDCF", bg="#201E43",
                                   command=lambda: open_supervisor_page(self), height=2, width=10)
        supervisor_button.place(relx=0.4, rely=0.58, anchor="center")

        investigator_button = Button(self.root, text="Investigator", font=("Arial", 15), fg="#91DDCF", bg="#201E43",
                                     command=lambda: open_investigator_page(self), height=2, width=10)
        investigator_button.place(relx=0.2, rely=0.58, anchor="center")

        facility_button = Button(self.root, text="Facilitator", font=("Arial", 15), fg="#91DDCF", bg="#201E43",
                                 command=lambda: open_facility_page(self), height=2, width=10)
        facility_button.place(relx=0.6, rely=0.58, anchor="center")

        guest_button = Button(self.root, text="Guest", font=("Arial", 15), fg="#91DDCF", bg="#201E43",
                              command=lambda: open_guest_page(self), height=2, width=10)
        guest_button.place(relx=0.8, rely=0.58, anchor="center")      


    def create_background(self):
        img_path1 = r"C:\Users\Savio\Desktop\min proj\bg.png"
        img1 = Image.open(img_path1)
        img1 = img1.resize((2560, 1440), Image.Resampling.LANCZOS)
        self.photo1 = ImageTk.PhotoImage(img1)

        img_label1 = Label(self.root, image=self.photo1)
        img_label1.place(x=0, y=0, relwidth=1, relheight=1)

    def create_header(self):
        header_frame = Frame(self.root, bg="#201E43", padx=10, pady=20)
        header_frame.pack(fill=X)

        img_path = r"C:\Users\Savio\Desktop\min proj\F_resized1.png"
        img = Image.open(img_path)
        img = img.resize((400, 120), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        img_label = Label(header_frame, image=photo, bg="#201E43")
        img_label.image = photo
        img_label.pack(side=LEFT, padx=5)

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
    root = Tk()
    app = ForensicManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
