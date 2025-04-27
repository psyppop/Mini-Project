import tkinter as tk
from tkinter import simpledialog, messagebox, LEFT, TOP, ttk
from PIL import Image, ImageTk
import mysql.connector
import pymysql
from tkinter import filedialog
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
import os
from tkinter import *
from PIL import Image
import webbrowser
from urllib.request import pathname2url



class Forensyncapp:
    def __init__(self, root):
        self.root = root
        self.evidence_list = []
        self.cases = []
        self.root.geometry("2560x1440")

        
        try:
            self.db_connection = mysql.connector.connect(
                host="127.0.0.1",  
                user="root",  
                password="rootsavio321",  
                database="forensync", 
                auth_plugin="mysql_native_password"
            )
            self.db_cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Error", f"Error: {err}")

        # Initialize the UI
        self.initialize_ui()



    def initialize_ui(self):
        self.root.title("ForenSync - Case Management")
        self.root.geometry("2560x1440")
        self.bg_color = "#201E43"
        self.root.config(bg=self.bg_color)
       

        
        try:
            self.img1 = Image.open(r"C:\Users\Savio\Desktop\min proj\bg.png").resize((2560, 1440), Image.Resampling.LANCZOS)
            self.photo1 = ImageTk.PhotoImage(self.img1)
            self.img_label1 = tk.Label(self.root, image=self.photo1)
            self.img_label1.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        
        try:
            self.edit_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\create-removebg-preview.png").resize((20, 20)))
            self.delete_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\delete-removebg-preview.png").resize((20, 20)))
            self.add_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\add.png").resize((40, 40)))
            self.search_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\search-removebg-preview.png").resize((30, 30)))
            self.create_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\create.png").resize((50, 50)))
            self.view_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\view-removebg-preview.png").resize((50, 50)))
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load icons: {e}")

        
        self.header_frame = tk.Frame(self.root, bg="#201E43", padx=10, pady=20)
        self.header_frame.pack(fill=tk.X)

        try:
            self.img = Image.open(r"C:\Users\Savio\Desktop\min proj\F_resized1.png").resize((400, 120), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.img)
            self.img_label = tk.Label(self.header_frame, image=self.photo, bg="#201E43")
            self.img_label.image = self.photo
            self.img_label.pack(side=tk.LEFT, padx=5)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load logo: {e}")

        
        self.listbox_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        self.listbox_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        
        self.title_frame = tk.Frame(self.listbox_frame, bg='#274E70', highlightbackground="black", highlightthickness=0)
        self.title_frame.pack(fill=tk.X)

        self.title_label = tk.Label(self.title_frame, text="YOUR CASES", font=("courier prime", 18), bg='#274E70', fg='#93dcd0', anchor='w')
        self.title_label.pack(side=tk.LEFT, padx=10)

        self.search_button = tk.Button(self.title_frame, image=self.search_icon, bg='#274E70', borderwidth=0, command=self.search_cases)
        self.search_button.pack(side=tk.RIGHT, padx=10)

        self.canvas = tk.Canvas(self.listbox_frame, bg='#CAE4DB')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.case_frame_container = tk.Frame(self.canvas, bg='#CAE4DB')     #CAE4DB
        self.canvas.create_window((0, 0), window=self.case_frame_container, anchor='nw')
        self.case_frame_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.add_button = tk.Button(self.listbox_frame, image=self.add_icon, bg='#CAE4DB', borderwidth=0, command=self.add_case)
        self.add_button.place(x=10, y=40)  

        

        self.fetch_cases()




    def fetch_cases(self):
        self.db_cursor.execute("SELECT title FROM cases")
        self.cases = [case[0] for case in self.db_cursor.fetchall()]  
        self.display_cases()

    def display_cases(self, case_list=None):
        
        for widget in self.case_frame_container.winfo_children():
            widget.destroy()

        case_list = case_list or self.cases

        
        for index, case in enumerate(case_list):
            case_frame = tk.Frame(self.case_frame_container, bg='#1b6c7e', padx=5, pady=5)
            case_frame.pack(fill=tk.X, pady=5)

            case_button = tk.Button(
                case_frame,
                text=f"{index + 1}. {case}",
                font=("Arial", 14),
                bg='#9acdcf',
                anchor='w',
                width=61,
                command=lambda case=case: self.open_case_options(case)  
            )
            case_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

            edit_button = tk.Button(case_frame, image=self.edit_icon, command=lambda idx=index: self.edit_case(idx), bg='#1b6c7e', borderwidth=0)
            edit_button.pack(side=tk.RIGHT, padx=5)

            delete_button = tk.Button(
                case_frame,
                image=self.delete_icon,
                command=lambda idx=index: self.delete_case(idx),  
                bg='#1b6c7e',
                borderwidth=0
            )
            delete_button.pack(side=tk.RIGHT)

        
        self.canvas.update_idletasks()
        self.add_button.place(x=10, y=self.case_frame_container.winfo_height() + 70)

    def add_case(self):
        messagebox.showerror("Access Denied", "Only investigators can create new cases.")
        return

    def edit_case(self, index):
        messagebox.showerror("Access Denied", "Only investigators can edit cases.")
        return

    def delete_case(self, index):
        messagebox.showerror("Access Denied", "Only investigators can delete cases.")
        return

    def open_case_options(self, case_title):
        self.listbox_frame.place_forget()  
        self.create_options_frame(case_title)

    def create_options_frame(self, case_title):
        options_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        options_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        
        title_frame = tk.Frame(options_frame, bg='#274E70')
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(title_frame, text=case_title, font=("Arial", 18), bg='#274E70', fg='#93dcd0', anchor='w')
        title_label.pack(side=tk.LEFT, padx=10)

       
        back_button = tk.Button(
            title_frame, text="Back", font=("Arial", 14), bg='#274E70', fg='white',
            command=lambda: self.switch_back(options_frame)
        )
        back_button.pack(side=tk.RIGHT, padx=0)

        
        def on_enter(event):
            event.widget.config(relief=tk.RAISED, bd=3, bg='#3A5F7D')  

        def on_leave(event):
            event.widget.config(relief=tk.FLAT, bd=1, bg='#274E70')  

    
        buttons = {
            " Report": {
                "x": 50, "y": 80, "width": 160, "height": 120,
                "icon": self.create_icon, "compound": "top",
                "command": self.open_report_frame  
            },
            "Evidence": {
                "x": 300, "y": 80, "width": 160, "height": 120,
                "icon": self.view_icon, "compound": "top",
                "command": self.open_evidence_frame  
            },
        }
        
        for action, geom in buttons.items():
            button = tk.Button(
                options_frame,
                text=action,
                font=("Arial", 14),
                bg='#274E70',
                fg='white',
                image=geom["icon"],
                compound=geom["compound"],
                command=geom["command"],  # Use command from dictionary
                relief=tk.FLAT,  # Default flat relief
                bd=1             # Default border width
            )
            button.place(x=geom["x"], y=geom["y"], width=geom["width"], height=geom["height"])

            # Bind hover effects
            button.bind("<Enter>", on_enter)  # When cursor enters the button
            button.bind("<Leave>", on_leave)  # When cursor leaves the button

    def open_report_frame(self):
     global report_frame, title_label, back_button

    # Hide the original list frame
     self.listbox_frame.place_forget()

    # Create the report frame
     report_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
     report_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

     # Title Frame
     title_frame = tk.Frame(report_frame, bg='#274E70')
     title_frame.place(relwidth=1, height=40)

     title_label = tk.Label(title_frame, text="Report Management", font=("courier prime", 18), bg='#274E70', fg='#93dcd0')
     title_label.pack(side=tk.LEFT, padx=10)

     # Back Button
     back_button = tk.Button(
        title_frame, text="Back", font=("Arial", 14), bg='#274E70', fg='white',
        command=lambda: self.switch_back(report_frame), anchor='center', height=2
     )
     back_button.place(relx=1, rely=0.5, anchor='e')

     # Define report sections
     section_positions = {
        "Create \nReport": {"x": 0.12, "y": 0.5, "height": 10, "width": 15},
        "Update \nReport": {"x": 0.37, "y": 0.5, "height": 10, "width": 15},
        "View \nReport": {"x": 0.62, "y": 0.5, "height": 10, "width": 15},
        "Delete \nReport": {"x": 0.87, "y": 0.5, "height": 10, "width": 15},
     }

     # Hover effects
     def on_enter(event):
        event.widget.config(relief=tk.RAISED, bd=3, bg='#3A5F7D')

     def on_leave(event):
        event.widget.config(relief=tk.FLAT, bd=1, bg='#274E70')

     # Function to handle report actions with role checks

     def handle_report_action(action):
      action = action.lower().strip()
      
      # Check if the action is not "view"
      if action != "view":
          messagebox.showerror("Access Denied", f"Only investigators can {action} reports.")
          return
          
      # Only proceed with view action
      base_dir = r"C:\Users\Savio\Desktop\min proj"
      file_name = "view.html"
      file_path = os.path.join(base_dir, file_name)
      
      if not os.path.exists(file_path):
          messagebox.showerror("Error", f"File not found: {file_path}")
          return

      brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"

      try:
          webbrowser.register('brave', None, webbrowser.BackgroundBrowser(brave_path))
          webbrowser.get('brave').open(f"file:///{file_path}")
      except Exception as e:
          messagebox.showerror("Error", f"Failed to open in Brave: {e}")
          webbrowser.open(f"file:///{file_path}")  # fallback to default
     # Create buttons
     for section, pos in section_positions.items():
        section_button = tk.Button(
            report_frame,
            text=section,
            font=("Arial", 14),
            bg='#274E70',
            fg='white',
            anchor='center',
            height=pos["height"],
            width=pos["width"],
            relief=tk.FLAT,
            bd=1,
            command=lambda s=section: handle_report_action(s.lower().split()[0])
        )
        section_button.place(relx=pos["x"], rely=pos["y"], anchor='center')
        
        # Bind hover effects
        section_button.bind("<Enter>", on_enter)
        section_button.bind("<Leave>", on_leave)

    def switch_back(self, frame):
        frame.place_forget()
        self.listbox_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)


    def open_evidence_frame(self):
        global evidence_frame, title_label, back_button

        # Hide the original list frame
        self.listbox_frame.place_forget()

        # Create or reuse the evidence_frame
        if 'evidence_frame' in globals() and evidence_frame.winfo_exists():
            evidence_frame.destroy()
        evidence_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        evidence_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        # Title for "Evidences"
        title_frame = tk.Frame(evidence_frame, bg='#274E70')
        title_frame.place(relwidth=1, height=40)

        title_label = tk.Label(title_frame, text="Evidences", font=("courier prime", 18), bg='#274E70', fg='#93dcd0')
        title_label.pack(side=tk.LEFT, padx=10)

        # Back Button positioned at the extreme right (points to main case list)
        back_button = tk.Button(
            title_frame, text="Back", font=("Arial", 14), bg='#274E70', fg='white',
            command=lambda: self.switch_back(evidence_frame), anchor='center', height=2
        )
        back_button.place(relx=1, rely=0.5, anchor='e')

        # Define evidence sections and their positions
        sec_positions = {
            "Add \nEvidence": {"x": 0.12, "y": 0.5, "height": 10, "width": 15},
            "View \nEvidence": {"x": 0.37, "y": 0.5, "height": 10, "width": 15},
            "Edit \nEvidence": {"x": 0.62, "y": 0.5, "height": 10, "width": 15},
            "Delete \nEvidence": {"x": 0.87, "y": 0.5, "height": 10, "width": 15},
        }

        # Define hover effect functions
        def on_enter(event):
            event.widget.config(relief=tk.RAISED, bd=3, bg='#3A5F7D')  # Apply 3D effect

        def on_leave(event):
            event.widget.config(relief=tk.FLAT, bd=1, bg='#274E70')  # Revert to original state

        # Create buttons dynamically
        for sec, pos in sec_positions.items():
            if sec == "Add \nEvidence":
                button = tk.Button(
                    evidence_frame, text=sec, font=("Arial", 14), bg='#274E70', fg='white',
                    anchor='center', height=pos["height"], width=pos["width"], command=self.add_evidence_options,
                    relief=tk.FLAT, bd=1  # Default flat relief and border width
                )
            elif sec == "View \nEvidence":
                button = tk.Button(
                    evidence_frame, text=sec, font=("Arial", 14), bg='#274E70', fg='white',
                    anchor='center', height=pos["height"], width=pos["width"], command=self.view_evidence,
                    relief=tk.FLAT, bd=1  # Default flat relief and border width
                )
            elif sec == "Edit \nEvidence":
                button = tk.Button(
                    evidence_frame, text=sec, font=("Arial", 14), bg='#274E70', fg='white',
                    anchor='center', height=pos["height"], width=pos["width"], command=self.edit_evidence,
                    relief=tk.FLAT, bd=1  # Default flat relief and border width
                )
            else:
                button = tk.Button(
                    evidence_frame, text=sec, font=("Arial", 14), bg='#274E70', fg='white',
                    anchor='center', height=pos["height"], width=pos["width"], command=self.delete_evidence,
                    relief=tk.FLAT, bd=1  # Default flat relief and border width
                )
            button.place(relx=pos["x"], rely=pos["y"], anchor='center')

            # Bind hover effects
            button.bind("<Enter>", on_enter)  # When cursor enters the button
            button.bind("<Leave>", on_leave)  # When cursor leaves the button

    def add_evidence_options(self):
        messagebox.showerror("Access Denied", "Only investigators can add evidence.")
        return

    def edit_evidence(self):
        messagebox.showerror("Access Denied", "Only investigators can edit evidence.")
        return

    def delete_evidence(self):
        messagebox.showerror("Access Denied", "Only investigators can delete evidence.")
        return

    def upload_file(self, evidence_type):
        messagebox.showerror("Access Denied", "Only investigators can upload evidence.")
        return

    def upload_new_file(self, preview_label):
        messagebox.showerror("Access Denied", "Only investigators can upload new files.")
        return

    def save_evidence_changes(self, index, name, category, preview_label):
        messagebox.showerror("Access Denied", "Only investigators can save evidence changes.")
        return

    def confirm_delete(self, selected_index):
        messagebox.showerror("Access Denied", "Only investigators can delete evidence.")
        return

    def view_evidence(self):
        global evidence_frame, title_label, back_button

        # Clear existing widgets
        for widget in evidence_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget != back_button:
                widget.destroy()

        # Create category frames
        categories = ["Physical \nEvidence", "Digital \nEvidence", "Document \nEvidence"]
        column_width = 0.32  # ~1/3 of the width for each column

        for col, category in enumerate(categories):
            # Category label frame
            cat_frame = tk.Frame(
                evidence_frame, bg='#274E70', highlightbackground="#93dcd0", highlightthickness=2
            )
            cat_frame.place(relx=col * column_width, rely=0.1, relwidth=column_width, height=45)

            # Category label
            tk.Label(
                cat_frame, text=category, bg='#274E70', fg='white', font=("Arial", 12, "bold")
            ).pack(pady=5)

            # Evidence display area (canvas for scrollable content)
            canvas = tk.Canvas(
                evidence_frame, bg='#CAE4DB', highlightbackground="#93dcd0", highlightthickness=2
            )
            canvas.place(relx=col * column_width, rely=0.2, relwidth=column_width, relheight=0.7)

            # Add scrollbar
            scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollbar.set)

            # Content frame (inside canvas)
            content_frame = tk.Frame(canvas, bg='#CAE4DB')
            canvas.create_window((0, 0), window=content_frame, anchor="nw")

            # Filter evidence by category
            category_evidence = [e for e in self.evidence_list if e[2] == category]

            for idx, (name, path, _) in enumerate(category_evidence):
                try:
                    # Load and resize image
                    img = Image.open(path)
                    img.thumbnail((120, 120))  # Slightly larger thumbnails
                    photo = ImageTk.PhotoImage(img)

                    # Create image label with a border
                    img_frame = tk.Frame(content_frame, bg='#274E70', padx=5, pady=5)
                    img_frame.grid(row=idx * 2, column=0, pady=5)

                    img_label = tk.Label(img_frame, image=photo, bg='#274E70')
                    img_label.image = photo  # Keep reference
                    img_label.pack()

                    # Create text label with better styling
                    tk.Label(
                        content_frame, text=name, wraplength=120, bg='#CAE4DB', fg='#274E70',
                        font=("Arial", 10, "bold")
                    ).grid(row=idx * 2 + 1, column=0, pady=(0, 10))

                except Exception as e:
                    # Handle non-image files
                    doc_frame = tk.Frame(content_frame, bg='#274E70', padx=5, pady=5)
                    doc_frame.grid(row=idx, column=0, pady=5)

                    tk.Label(
                        doc_frame, text=f"📄 {name}\n{path}", wraplength=120, bg='#274E70', fg='white',
                        font=("Arial", 10), justify="center"
                    ).pack()

            # Update scrollregion
            content_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        # Update title and back button
        title_label.config(text="Viewing Evidence")
        back_button.config(command=lambda: self.open_evidence_frame())

    def switch_back(self, current_frame):
        current_frame.place_forget()
        self.listbox_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

    def search_cases(self):
        search_term = simpledialog.askstring("Search", "Enter case title to search:")
        if search_term:
            filtered_cases = [case for case in self.cases if search_term.lower() in case.lower()]
            if filtered_cases:
                self.display_cases(filtered_cases)
            else:
                messagebox.showinfo("Search Results", "No cases found.")
        else:
            self.display_cases()


def main():
    root = tk.Tk()
    app = Forensyncapp(root)
    root.mainloop()


if __name__ == "__main__":
    main()