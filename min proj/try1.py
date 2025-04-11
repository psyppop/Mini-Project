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


class Forensyncapp:
    def __init__(self, root, role="investigator"):
        self.root = root
        self.evidence_list = []
        self.cases = []
        self.role = role.lower()
        self.root.geometry("2560x1440")

        # Establish database connection
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

    def show_restricted_error(self):
        messagebox.showerror("Access Denied", "Only investigators can perform this action")

    def initialize_ui(self):
        self.root.title("ForenSync - Case Management")
        self.root.geometry("2560x1440")
        self.bg_color = "#201E43"
        self.root.config(bg=self.bg_color)
       
        # Load background image
        try:
            self.img1 = Image.open(r"C:\Users\Savio\Desktop\min proj\bg.png").resize((2560, 1440), Image.Resampling.LANCZOS)
            self.photo1 = ImageTk.PhotoImage(self.img1)
            self.img_label1 = tk.Label(self.root, image=self.photo1)
            self.img_label1.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load background image: {e}")

        # Load icons
        try:
            self.edit_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\edit.png").resize((20, 20)))
            self.delete_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\delete.jpeg").resize((20, 20)))
            self.add_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\edit.png").resize((40, 40)))
            self.search_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\search.jpeg").resize((30, 30)))
            self.create_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\create.jpeg").resize((50, 50)))
            self.view_icon = ImageTk.PhotoImage(Image.open(r"C:\Users\Savio\Downloads\view.jpeg").resize((50, 50)))
        except Exception as e:
            messagebox.showerror("Image Error", f"Failed to load icons: {e}")

        # Header frame
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

        # Case list frame
        self.listbox_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        self.listbox_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        # Title Frame with border
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

        self.case_frame_container = tk.Frame(self.canvas, bg='#CAE4DB')
        self.canvas.create_window((0, 0), window=self.case_frame_container, anchor='nw')
        self.case_frame_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Only show add button for investigators
        if self.role == "investigator":
            self.add_button = tk.Button(self.listbox_frame, image=self.add_icon, bg='#274E70', borderwidth=0, command=self.add_case)
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

        # Display cases
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

            # Only show edit/delete buttons for investigators
            if self.role == "investigator":
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

        # Update canvas
        self.canvas.update_idletasks()
        if self.role == "investigator":
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
        self.options_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        self.options_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        # Title Frame
        title_frame = tk.Frame(self.options_frame, bg='#274E70')
        title_frame.place(relwidth=1, height=40)

        title_label = tk.Label(title_frame, text=f"Case: {case_title}", font=("courier prime", 18), bg='#274E70', fg='#93dcd0')
        title_label.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(
            title_frame, text="Back", font=("Arial", 14), bg='#274E70', fg='white',
            command=lambda: self.switch_back_to_cases(self.options_frame), anchor='center', height=2
        )
        back_button.place(relx=1, rely=0.5, anchor='e')

        # Define buttons and positions
        button_positions = {
            "Evidence": {"x": 0.25, "y": 0.5, "height": 10, "width": 15},
            "Report": {"x": 0.75, "y": 0.5, "height": 10, "width": 15}
        }

        # Create buttons
        evidence_button = tk.Button(
            self.options_frame,
            text="Evidence",
            font=("Arial", 14),
            bg='#274E70',
            fg='white',
            anchor='center',
            height=button_positions["Evidence"]["height"],
            width=button_positions["Evidence"]["width"],
            command=self.open_evidence_frame
        )
        evidence_button.place(relx=button_positions["Evidence"]["x"], rely=button_positions["Evidence"]["y"], anchor='center')

        report_button = tk.Button(
            self.options_frame,
            text="Report",
            font=("Arial", 14),
            bg='#274E70',
            fg='white',
            anchor='center',
            height=button_positions["Report"]["height"],
            width=button_positions["Report"]["width"],
            command=self.open_report_frame
        )
        report_button.place(relx=button_positions["Report"]["x"], rely=button_positions["Report"]["y"], anchor='center')

    def open_report_frame(self):
        report_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        report_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        title_frame = tk.Frame(report_frame, bg='#274E70')
        title_frame.place(relwidth=1, height=40)

        title_label = tk.Label(title_frame, text="Report Management", font=("courier prime", 18), bg='#274E70', fg='#93dcd0')
        title_label.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(
            title_frame, text="Back", font=("Arial", 14), bg='#274E70', fg='white',
            command=lambda: self.switch_back(report_frame), anchor='center', height=2
        )
        back_button.place(relx=1, rely=0.5, anchor='e')

        section_positions = {
            "Create \nReport": {"x": 0.12, "y": 0.5, "height": 10, "width": 15},
            "Update \nReport": {"x": 0.37, "y": 0.5, "height": 10, "width": 15},
            "View \nReport": {"x": 0.62, "y": 0.5, "height": 10, "width": 15},
            "Delete \nReport": {"x": 0.87, "y": 0.5, "height": 10, "width": 15},
        }

        def on_enter(event):
            event.widget.config(relief=tk.RAISED, bd=3, bg='#3A5F7D')

        def on_leave(event):
            event.widget.config(relief=tk.FLAT, bd=1, bg='#274E70')

        def handle_report_action(action):
            action = action.lower()
            base_dir = r"C:\Users\Savio\Desktop\min proj"
            
            if action != "view" and self.role != "investigator":
                self.show_restricted_error()
                return
                
            try:
                if action == "view":
                    file_path = os.path.join(base_dir, "try.html")
                elif action == "create":
                    file_path = os.path.join(base_dir, "final_rep.html")
                elif action == "update":
                    file_path = os.path.join(base_dir, "reportlsat.html")
                elif action == "delete":
                    messagebox.showinfo("Delete Report", "Delete report functionality would go here")
                    return

                if os.path.exists(file_path):
                    webbrowser.get().open(f"file:///{os.path.normpath(file_path)}")
                else:
                    messagebox.showerror("Error", f"File not found: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open report: {e}")

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
            
            section_button.bind("<Enter>", on_enter)
            section_button.bind("<Leave>", on_leave)

    def open_evidence_frame(self):
        evidence_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        evidence_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        title_frame = tk.Frame(evidence_frame, bg='#274E70')
        title_frame.place(relwidth=1, height=40)

        title_label = tk.Label(title_frame, text="Evidences", font=("courier prime", 18), bg='#274E70', fg='#93dcd0')
        title_label.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(
            title_frame, text="Back", font=("Arial", 14), bg='#274E70', fg='white',
            command=lambda: self.switch_back(evidence_frame), anchor='center', height=2
        )
        back_button.place(relx=1, rely=0.5, anchor='e')

        sec_positions = {
            "Add \nEvidence": {"x": 0.12, "y": 0.5, "height": 10, "width": 15},
            "View \nEvidence": {"x": 0.37, "y": 0.5, "height": 10, "width": 15},
            "Edit \nEvidence": {"x": 0.62, "y": 0.5, "height": 10, "width": 15},
            "Delete \nEvidence": {"x": 0.87, "y": 0.5, "height": 10, "width": 15},
        }

        def on_enter(event):
            event.widget.config(relief=tk.RAISED, bd=3, bg='#3A5F7D')

        def on_leave(event):
            event.widget.config(relief=tk.FLAT, bd=1, bg='#274E70')

        def handle_evidence_action(action):
            action = action.lower().split()[0]
            
            if action != "view" and self.role != "investigator":
                self.show_restricted_error()
                return
                
            if action == "add":
                self.add_evidence_options()
            elif action == "view":
                self.view_evidence()
            elif action == "edit":
                self.edit_evidence()
            elif action == "delete":
                self.delete_evidence()

        for sec, pos in sec_positions.items():
            button = tk.Button(
                evidence_frame, text=sec, font=("Arial", 14), bg='#274E70', fg='white',
                anchor='center', height=pos["height"], width=pos["width"], 
                command=lambda s=sec: handle_evidence_action(s),
                relief=tk.FLAT, bd=1
            )
            button.place(relx=pos["x"], rely=pos["y"], anchor='center')
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

    def add_evidence_options(self):
        title_label = tk.Label(self.root, text="Adding Evidences.....", font=("courier prime", 18), bg='#274E70', fg='#93dcd0')
        title_label.pack()

        evidence_types = {
            "Physical \nEvidence": {"x": 0.17, "y": 0.5, "height": 10, "width": 15},
            "Digital \nEvidence": {"x": 0.50, "y": 0.5, "height": 10, "width": 15},
            "Document \nEvidence": {"x": 0.82, "y": 0.5, "height": 10, "width": 15},
        }

        for evidence_type, pos in evidence_types.items():
            button = tk.Button(
                self.root,
                text=evidence_type,
                font=("Arial", 14),
                bg='#274E70',
                fg='white',
                anchor='center',
                height=pos["height"],
                width=pos["width"],
                command=lambda et=evidence_type: self.upload_file(et)
            )
            button.place(relx=pos["x"], rely=pos["y"], anchor='center')

    def upload_file(self, evidence_type):
        if self.role != "investigator":
            self.show_restricted_error()
            return

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
        evidence_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        evidence_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        title_frame = tk.Frame(evidence_frame, bg='#274E70')
        title_frame.place(relwidth=1, height=40)

        title_label = tk.Label(title_frame, text="Viewing Evidence", font=("courier prime", 18), bg='#274E70', fg='#93dcd0')
        title_label.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(
            title_frame, text="Back", font=("Arial", 14), bg='#274E70', fg='white',
            command=lambda: self.switch_back(evidence_frame), anchor='center', height=2
        )
        back_button.place(relx=1, rely=0.5, anchor='e')

        categories = ["Physical \nEvidence", "Digital \nEvidence", "Document \nEvidence"]
        column_width = 0.32

        for col, category in enumerate(categories):
            cat_frame = tk.Frame(
                evidence_frame, bg='#274E70', highlightbackground="#93dcd0", highlightthickness=2
            )
            cat_frame.place(relx=col * column_width, rely=0.1, relwidth=column_width, height=45)

            tk.Label(
                cat_frame, text=category, bg='#274E70', fg='white', font=("Arial", 12, "bold")
            ).pack(pady=5)

            canvas = tk.Canvas(
                evidence_frame, bg='#CAE4DB', highlightbackground="#93dcd0", highlightthickness=2
            )
            canvas.place(relx=col * column_width, rely=0.2, relwidth=column_width, relheight=0.7)

            scrollbar = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")
            canvas.configure(yscrollcommand=scrollbar.set)

            content_frame = tk.Frame(canvas, bg='#CAE4DB')
            canvas.create_window((0, 0), window=content_frame, anchor="nw")

            category_evidence = [e for e in self.evidence_list if e[2] == category]

            for idx, (name, path, _) in enumerate(category_evidence):
                try:
                    img = Image.open(path)
                    img.thumbnail((120, 120))
                    photo = ImageTk.PhotoImage(img)

                    img_frame = tk.Frame(content_frame, bg='#274E70', padx=5, pady=5)
                    img_frame.grid(row=idx * 2, column=0, pady=5)

                    img_label = tk.Label(img_frame, image=photo, bg='#274E70')
                    img_label.image = photo
                    img_label.pack()

                    tk.Label(
                        content_frame, text=name, wraplength=120, bg='#CAE4DB', fg='#274E70',
                        font=("Arial", 10, "bold")
                    ).grid(row=idx * 2 + 1, column=0, pady=(0, 10))

                except Exception as e:
                    doc_frame = tk.Frame(content_frame, bg='#274E70', padx=5, pady=5)
                    doc_frame.grid(row=idx, column=0, pady=5)

                    tk.Label(
                        doc_frame, text=f"📄 {name}\n{path}", wraplength=120, bg='#274E70', fg='white',
                        font=("Arial", 10), justify="center"
                    ).pack()

            content_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

    def edit_evidence(self):
        if self.role != "investigator":
            self.show_restricted_error()
            return

        edit_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        edit_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        title_frame = tk.Frame(edit_frame, bg='#274E70')
        title_frame.place(relwidth=1, height=40)

        title_label = tk.Label(title_frame, text="Editing Evidence", font=("courier prime", 18), bg='#274E70', fg='#93dcd0')
        title_label.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(
            title_frame, text="Back", font=("Arial", 14), bg='#274E70', fg='white',
            command=lambda: self.switch_back(edit_frame), anchor='center', height=2
        )
        back_button.place(relx=1, rely=0.5, anchor='e')

        # Implementation for editing evidence would go here
        tk.Label(edit_frame, text="Evidence editing functionality", bg='#CAE4DB').pack(pady=50)

    def delete_evidence(self):
        if self.role != "investigator":
            self.show_restricted_error()
            return

        delete_frame = tk.Frame(self.root, bg='#CAE4DB', highlightbackground="black", highlightthickness=1)
        delete_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

        title_frame = tk.Frame(delete_frame, bg='#274E70')
        title_frame.place(relwidth=1, height=40)

        title_label = tk.Label(title_frame, text="Deleting Evidence", font=("courier prime", 18), bg='#274E70', fg='#93dcd0')
        title_label.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(
            title_frame, text="Back", font=("Arial", 14), bg='#274E70', fg='white',
            command=lambda: self.switch_back(delete_frame), anchor='center', height=2
        )
        back_button.place(relx=1, rely=0.5, anchor='e')

        # Implementation for deleting evidence would go here
        tk.Label(delete_frame, text="Evidence deletion functionality", bg='#CAE4DB').pack(pady=50)

    def switch_back_to_cases(self, current_frame):
        current_frame.place_forget()
        self.listbox_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

    def switch_back(self, current_frame):
        current_frame.place_forget()
        self.options_frame.place(x=400, y=250, relwidth=0.5, relheight=0.5)

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
    # Change role to "supervisor" to test supervisor access
    app = Forensyncapp(root, role="investigator")
    root.mainloop()


if __name__ == "__main__":
    main()