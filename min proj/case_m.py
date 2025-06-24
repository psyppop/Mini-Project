import tkinter as tk
from tkinter import ttk
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
                database="fms", 
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


        top_right_frame = tk.Frame(self.root, bg=self.bg_color)
        top_right_frame.place(relx=0.98, rely=0.02, anchor="ne")

        # Add BACK button (using a button instead of label for better visibility)
        back_button = tk.Button(
        top_right_frame,
        text="BACK",
        font=("Arial", 12, "bold"),
        fg="white",
        bg="#3A5F7D",  # Different color from background
        activebackground="#4A6F8D",  # Color when pressed
        relief=tk.RAISED,
        bd=2,
        cursor="hand2",
        command=self.root.destroy
        )
        back_button.pack(side=tk.RIGHT, padx=5)

        #    Close button (X)
        close_button = tk.Button(
        top_right_frame,
        text="X",
        command=self.root.destroy,
        bg="red",
        fg="white",
        font=("Arial", 10, "bold"),
        bd=2
        )
        close_button.pack(side=tk.RIGHT)

        # Make sure these buttons stay on top of everything
        top_right_frame.lift()

        
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
        case_title = simpledialog.askstring("Input", "Enter case title:")
        if not case_title:
            messagebox.showwarning("Input Error", "Case title cannot be empty.")
            return

        try:
            self.db_cursor.execute("INSERT INTO cases (title) VALUES (%s)", (case_title,))
            self.db_connection.commit()
            self.cases.append(case_title)
            self.display_cases()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to add case: {err}")

    def edit_case(self, index):
        old_title = self.cases[index]  
        new_title = simpledialog.askstring("Input", "Edit case title:", initialvalue=old_title)

        if new_title:
            self.cases[index] = new_title  
            
            self.db_cursor.execute("UPDATE cases SET title = %s WHERE title = %s", (new_title, old_title))
            self.db_connection.commit()

            self.display_cases()

    def delete_case(self, index):
        case_title = self.cases[index]  
        if messagebox.askyesno("Delete", "Are you sure you want to delete this case?"):
            
            del self.cases[index]

            
            self.db_cursor.execute("DELETE FROM cases WHERE title = %s", (case_title,))
            self.db_connection.commit()

            self.display_cases()  

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
      base_dir = r"C:\Users\Savio\Desktop\min proj"

      if action == "delete":
          # Import and run the del_report module
          import del_report
          del_report.main()
          return

      action_map = {
        "view": "view.html",
        "create": "create.html",
        "update": "update.html"
      }

      file_name = action_map.get(action)
      if not file_name:
        messagebox.showerror("Error", f"Invalid action: {action}")
        return
 
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
        global evidence_frame, title_label, back_button

        # Update the title
        title_label.config(text="Adding Evidences.....")

        # Hide existing buttons in the evidence_frame
        for widget in evidence_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget != back_button:
                widget.destroy()

        # Define hover effect functions
        def on_enter(event):
            event.widget.config(relief=tk.RAISED, bd=3, bg='#3A5F7D')  # Apply 3D effect

        def on_leave(event):
            event.widget.config(relief=tk.FLAT, bd=1, bg='#274E70')  # Revert to original state

        # Define new buttons for evidence types
        evidence_types = {
            "Physical \nEvidence": {"x": 0.17, "y": 0.5, "height": 10, "width": 15},
            "Digital \nEvidence": {"x": 0.50, "y": 0.5, "height": 10, "width": 15},
            "Document \nEvidence": {"x": 0.82, "y": 0.5, "height": 10, "width": 15},
        }

        # Add new buttons
        for evidence_type, pos in evidence_types.items():
            button = tk.Button(
                evidence_frame,
                text=evidence_type,
                font=("Arial", 14),
                bg='#274E70',
                fg='white',
                anchor='center',
                height=pos["height"],
                width=pos["width"],
                relief=tk.FLAT,  # Default flat relief
                bd=1,            # Default border width
                command=lambda et=evidence_type: self.upload_file(et)  # Pass evidence type to upload_file
            )
            button.place(relx=pos["x"], rely=pos["y"], anchor='center')

            # Bind hover effects
            button.bind("<Enter>", on_enter)  # When cursor enters the button
            button.bind("<Leave>", on_leave)  # When cursor leaves the button

        # Update the Back button to return to the evidence management screen
        back_button.config(command=lambda: self.open_evidence_frame())

    def upload_file(self, evidence_type):
        evidence_name = simpledialog.askstring("Evidence Name", f"Enter a name for the {evidence_type}:")
        if not evidence_name:
            messagebox.showwarning("No Name", "Evidence name required!")
            return

        file_path = filedialog.askopenfilename(
            title=f"Upload {evidence_type}",
            filetypes=[("All Files", "*.*")]
        )

        if file_path:
            self.evidence_list.append((evidence_name, file_path, evidence_type))
            messagebox.showinfo("Success", f"{evidence_type} uploaded!")

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

    def edit_evidence(self):
        global evidence_frame, title_label, back_button

        # Update the title
        title_label.config(text="Editing Evidences.....")

        # Hide existing buttons in the evidence_frame
        for widget in evidence_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget != back_button:
                widget.destroy()

        # Create a frame for selecting evidence to edit
        select_frame = tk.Frame(evidence_frame, bg='#CAE4DB')
        select_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Label for instructions
        tk.Label(select_frame, text="Select Evidence to Edit:", font=("Arial", 14), bg='#CAE4DB').pack(pady=10)

        # Listbox to display evidence items
        evidence_listbox = tk.Listbox(select_frame, font=("Arial", 12), selectmode=tk.SINGLE)
        evidence_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate the listbox with evidence items
        for idx, evidence in enumerate(self.evidence_list):
            evidence_listbox.insert(tk.END, f"{idx + 1}. {evidence[0]} ({evidence[2]})")

        # Button to proceed to edit the selected evidence
        select_button = tk.Button(select_frame, text="Edit Selected Evidence", font=("Arial", 14), bg='#274E70', fg='white',
                                  command=lambda: self.open_edit_form(evidence_listbox.curselection()))
        select_button.pack(pady=10)

        # Update the Back button to return to the evidence management screen
        back_button.config(command=lambda: self.open_evidence_frame())

    def open_edit_form(self, selected_index):
        global evidence_frame, title_label, back_button

        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select an evidence item to edit.")
            return

        # Get the selected evidence
        selected_evidence = self.evidence_list[selected_index[0]]

        # Clear the select_frame
        for widget in evidence_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget != back_button:
                widget.destroy()

        # Create a frame for editing evidence
        edit_frame = tk.Frame(evidence_frame, bg='#CAE4DB')
        edit_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Label and Entry for Evidence Name
        tk.Label(edit_frame, text="Evidence Name:", font=("Arial", 12), bg='#CAE4DB').place(relx=0.1, rely=0.1)
        name_entry = tk.Entry(edit_frame, font=("Arial", 12))
        name_entry.insert(0, selected_evidence[0])  # Populate with existing name
        name_entry.place(relx=0.4, rely=0.1, relwidth=0.5)

        # Label and Dropdown for Evidence Category
        tk.Label(edit_frame, text="Evidence Category:", font=("Arial", 12), bg='#CAE4DB').place(relx=0.1, rely=0.3)
        categories = ["Physical \nEvidence", "Digital \nEvidence", "Document \nEvidence"]
        category_var = tk.StringVar(value=selected_evidence[2])  # Populate with existing category
        category_dropdown = tk.OptionMenu(edit_frame, category_var, *categories)
        category_dropdown.config(font=("Arial", 12), bg='#274E70', fg='white')
        category_dropdown.place(relx=0.4, rely=0.3, relwidth=0.5)

        # Label and Button for Uploading New Evidence File
        tk.Label(edit_frame, text="Upload New File:", font=("Arial", 12), bg='#CAE4DB').place(relx=0.1, rely=0.5)
        upload_button = tk.Button(edit_frame, text="Browse", font=("Arial", 12), bg='#274E70', fg='white',
                                  command=lambda: self.upload_new_file(preview_label))
        upload_button.place(relx=0.4, rely=0.5, relwidth=0.5)

        # Preview Label for Image/File
        preview_label = tk.Label(edit_frame, text="Preview will appear here", font=("Arial", 12), bg='#CAE4DB')
        preview_label.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.2)

        # Display the existing image/file preview
        try:
            img = Image.open(selected_evidence[1])
            img.thumbnail((150, 150))  # Resize for preview
            photo = ImageTk.PhotoImage(img)
            preview_label.config(image=photo, text="")
            preview_label.image = photo  # Keep a reference
            preview_label.file_path = selected_evidence[1]  # Store the file path
        except Exception as e:
            # Handle non-image files
            preview_label.config(text=f"File: {selected_evidence[1]}", image=None)

        # Save Button
        save_button = tk.Button(
            edit_frame,
            text="Save Changes",
            command=lambda: self.save_evidence_changes(
                selected_index[0],  # index
                name_entry.get(),  # name
                category_var.get(),  # category
                preview_label  # preview_label
            )
        )
        save_button.place(relx=0.35, rely=0.9, relwidth=0.3)

        # Update the Back button to return to the evidence management screen
        back_button.config(command=lambda: self.open_evidence_frame())

    def save_evidence_changes(self, index, name, category, preview_label):
        if not name:
            messagebox.showwarning("Input Error", "Evidence name cannot be empty.")
            return

        if not hasattr(preview_label, 'file_path'):
            messagebox.showwarning("Input Error", "Please upload a new file.")
            return

        # Update the evidence list with the new details
        updated_evidence = (name, preview_label.file_path, category)
        self.evidence_list[index] = updated_evidence  # Replace the old evidence

        messagebox.showinfo("Success", "Evidence updated successfully!")
        self.open_evidence_frame()

    def delete_evidence(self):
        global evidence_frame, title_label, back_button

        # Update the title
        title_label.config(text="Deleting Evidences.....")

        # Hide existing buttons in the evidence_frame
        for widget in evidence_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget != back_button:
                widget.destroy()

        # Create a frame for selecting evidence to delete
        delete_frame = tk.Frame(evidence_frame, bg='#CAE4DB')
        delete_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Label for instructions
        tk.Label(delete_frame, text="Select Evidence to Delete:", font=("Arial", 14), bg='#CAE4DB').pack(pady=10)

        # Listbox to display evidence items
        evidence_listbox = tk.Listbox(delete_frame, font=("Arial", 12), selectmode=tk.SINGLE)
        evidence_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Populate the listbox with evidence items
        for idx, evidence in enumerate(self.evidence_list):
            evidence_listbox.insert(tk.END, f"{idx + 1}. {evidence[0]} ({evidence[2]})")

        # Button to delete the selected evidence
        delete_button = tk.Button(delete_frame, text="Delete Selected Evidence", font=("Arial", 14), bg='#274E70', fg='white',
                                  command=lambda: self.confirm_delete(evidence_listbox.curselection()))
        delete_button.pack(pady=10)

        # Update the Back button to return to the evidence management screen
        back_button.config(command=lambda: self.open_evidence_frame())

    def confirm_delete(self, selected_index):
        if not selected_index:
            messagebox.showwarning("Selection Error", "Please select an evidence item to delete.")
            return

        # Get the selected evidence
        selected_evidence = self.evidence_list[selected_index[0]]

        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{selected_evidence[0]}'?"):
            # Remove the evidence from the list
            self.evidence_list.pop(selected_index[0])
            messagebox.showinfo("Success", "Evidence deleted successfully!")
            self.open_evidence_frame()  # Return to evidence view

    def upload_new_file(self, preview_label):
        file_path = filedialog.askopenfilename(title="Upload New Evidence", filetypes=[("All Files", "*.*")])
        if file_path:
            try:
                # Display image preview
                img = Image.open(file_path)
                img.thumbnail((150, 150))  # Resize for preview
                photo = ImageTk.PhotoImage(img)
                preview_label.config(image=photo, text="")
                preview_label.image = photo  # Keep a reference
                preview_label.file_path = file_path  # Store the file path
            except Exception as e:
                # Handle non-image files
                preview_label.config(text=f"File: {file_path}", image=None)

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