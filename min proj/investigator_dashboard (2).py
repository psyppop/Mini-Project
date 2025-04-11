from tkinter import *
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os

from investigator1 import mainchat
from face_recog import facemain



class ForenSyncDashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Store the username for personalized greeting
        self.root.title("ForenSync - Investigator Dashboard")
        self.root.geometry("2560x1440")

        # Load and set the background image
        self.set_background_image(r"C:\Users\Savio\Documents\mini proj\bg.png")

        self.setup_styles()
        self.create_header()
        self.create_main_content() 

    def set_background_image(self, image_path):
        """Load and display the background image."""
        try:
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((2560, 1440), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(bg_image)  # Keep a reference to the image
            bg_label = Label(self.root, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            print("Background image loaded successfully!")
        except Exception as e:
            print(f"Error loading background image: {e}")
            

    def setup_styles(self):
        """Set up custom styles for the dashboard."""
        # Custom colors
        self.bg_color = '#201E43'  # Dark blue
        self.button_color = '#91DDCF'  # Mint green
        self.text_color = '#201E43'  # Dark blue for text

        # Custom font
        self.header_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=12)

    def create_header(self):
        """Create the header section with a logo and logout button."""
        header_frame = Frame(self.root, bg="#201E43", padx=10, pady=20)
        header_frame.place(x=0, y=0, relwidth=1)

        img_path = r"C:\Users\Savio\Documents\mini proj\F_resized1.png"
        try:
            img = Image.open(img_path)
            img = img.resize((400, 120), Image.Resampling.LANCZOS)
            self.header_image = ImageTk.PhotoImage(img)  # Keep a reference to the image
            print("Header image loaded successfully!")

            img_label = Label(header_frame, image=self.header_image, bg="#201E43")
            img_label.image = self.header_image  # Keep reference to prevent garbage collection
            img_label.grid(row=0, column=0, padx=5)
        except Exception as e:
            print(f"Error loading header image: {e}")
            

        # Logout Button using tk.Button
        logout_btn = Button(header_frame, text="Logout", bg=self.button_color, fg=self.text_color, font=self.button_font, command=self.logout)
        logout_btn.place(x=1050, y=30)

    def logout(self):
        """Logout and close the application."""
        self.root.destroy()  # Close the current Tkinter window
        os.system("python Main.py")

    def create_main_content(self):
        """Create the main content area with buttons."""
        main_frame = Frame(self.root, bg=self.bg_color)
        main_frame.place(x=370, y=200, width=500, height=400)

        # Personalized welcome message for each investigator
        welcome_label = Label(main_frame, text=f"Welcome, {self.username}", bg="#91DDCF", fg="#201E43", font=("Helvetica", 17), anchor="center")
        welcome_label.place(x=0, y=0, height=50, width=500)

        # Place buttons using tk.Button and configure colors
        btn1 = self.create_dashboard_button(main_frame, "🔍 Evidence\nManagement")
        btn1.place(x=45, y=80, width=200, height=60)

        btn2 = self.create_dashboard_button(main_frame, "👤 Offender Photo\nArchive")
        btn2.place(x=250, y=80, width=200, height=60)

        btn3 = self.create_dashboard_button(main_frame, "📁 Case\nManagement",command=lambda: mainrun(self.root))
        btn3.place(x=45, y=160, width=200, height=60)

        btn4 = self.create_dashboard_button(main_frame, "📊 Statistics")
        btn4.place(x=250, y=160, width=200, height=60)

        btn5 = self.create_dashboard_button(main_frame, "💬 Chat", command=lambda: mainchat(self))
        btn5.place(x=45, y=240, width=200, height=60)

        btn6 = self.create_dashboard_button(main_frame, "📋 Automated\nReports")
        btn6.place(x=250, y=240, width=200, height=60)

        btn7 = self.create_dashboard_button(main_frame, "🗄️ Case Record\nArchive")
        btn7.place(x=45, y=320, width=200, height=60)
        
        btn8 = self.create_dashboard_button(main_frame, "📷 Facial Analysis", command=lambda: facemain(self.root))
        btn8.place(x=250, y=320, width=200, height=60)

    def create_dashboard_button(self, parent, text, command=None):
        """Helper method to create styled dashboard buttons with optional command."""
        return Button(parent, text=text, bg=self.button_color, fg=self.text_color, font=self.button_font, padx=20, pady=10, command=command)


def main():
    root = Tk()
    app = ForenSyncDashboard(root, username="Investigator 1")
    root.mainloop()


if __name__ == "__main__":
    main()




from tkinter import *
from tkinter import ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os

class ForenSyncDashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Store the username for personalized greeting
        self.root.title("ForenSync - Investigator Dashboard")
        self.root.geometry("2560x1440")

        # Load and set the background image
        self.set_background_image(r"C:\Users\Savio\Documents\mini proj\bg.png")

        self.setup_styles()
        self.create_header()
        self.create_main_content() 

    def set_background_image(self, image_path):
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((2560, 1440), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)
        bg_label = Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def setup_styles(self):
        # Custom colors
        self.bg_color = '#201E43'  # Dark blue
        self.button_color = '#91DDCF'  # Mint green
        self.text_color = '#201E43'  # Dark blue for text

        # Custom font
        self.header_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=12)

    def create_header(self):
        header_frame = Frame(self.root, bg="#201E43", padx=10, pady=20)
        header_frame.place(x=0, y=0, relwidth=1)

        img_path = r"C:\Users\Savio\Documents\mini proj\F_resized1.png"
        img = Image.open(img_path)
        img = img.resize((400, 120), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        img_label = Label(header_frame, image=photo, bg="#201E43")
        img_label.image = photo
        img_label.grid(row=0, column=0, padx=5)

        title_label = Label(header_frame, font=self.header_font, bg=self.bg_color, fg=self.button_color)
        title_label.grid(row=0, column=1, padx=50)

        # Logout Button using tk.Button
        logout_btn = Button(header_frame, text="Logout", bg=self.button_color, fg=self.text_color, font=self.button_font, command=self.logout)
        logout_btn.place(x=1050, y=30)

    def logout(self):
        self.root.destroy()  # Close the current Tkinter window
        os.system("python Main.py")

    def create_main_content(self):
        main_frame = Frame(self.root, bg=self.bg_color)
        main_frame.place(x=370, y=200, width=500, height=400)

        # Personalized welcome message for each investigator
        welcome_label = Label(main_frame, text=f"Welcome, {self.username}", bg="#91DDCF", fg="#201E43", font=("Helvetica", 17), anchor="center")
        welcome_label.place(x=0, y=0, height=50, width=500)

        # Place buttons using tk.Button and configure colors
        btn1 = self.create_dashboard_button(main_frame, "🔍 Evidence\nManagement")
        btn1.place(x=45, y=80, width=200, height=60)

        btn2 = self.create_dashboard_button(main_frame, "👤 Offender Photo\nArchive")
        btn2.place(x=250, y=80, width=200, height=60)

        btn3 = self.create_dashboard_button(main_frame, "📁 Case\nManagement")
        btn3.place(x=45, y=160, width=200, height=60)

        btn4 = self.create_dashboard_button(main_frame, "📊 Statistics")
        btn4.place(x=250, y=160, width=200, height=60)

        btn5 = self.create_dashboard_button(main_frame, "💬 Chat")
        btn5.place(x=45, y=240, width=200, height=60)

        btn6 = self.create_dashboard_button(main_frame, "📋 Automated\nReports")
        btn6.place(x=250, y=240, width=200, height=60)

        btn7 = self.create_dashboard_button(main_frame, "🗄️ Case Record\nArchive")
        btn7.place(x=45, y=320, width=200, height=60)

        btn8 = self.create_dashboard_button(main_frame, "📷 Facial Analysis")
        btn8.place(x=250, y=320, width=200, height=60)

    def create_dashboard_button(self, parent, text):
        return Button(parent, text=text, bg=self.button_color, fg=self.text_color, font=self.button_font, padx=20, pady=10)
    
    def show_investigator_dashboard(self, username, cases):
        self.clear_window()
        self.create_background()
        self.create_header()

        # Display a welcome message
        welcome_label = Label(self.root, text=f"Welcome, {username}", font=("Arial", 20), fg="#91DDCF", bg="#201E43")
        welcome_label.pack(pady=10)

        # Display the investigator's cases
        case_frame = Frame(self.root, bg="#201E43")
        case_frame.pack(pady=20)

        Label(case_frame, text="Your Cases:", font=("Arial", 16), fg="#91DDCF", bg="#201E43").pack(pady=10)

        for case in cases:
            case_label = Label(case_frame, text=f"Case ID: {case[0]}, Description: {case[1]}", font=("Arial", 12),
                           fg="#91DDCF", bg="#201E43")
            case_label.pack(anchor="w", padx=20, pady=5)


def main():
    root = Tk()
    app = ForenSyncDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
