import cv2
import face_recognition
import numpy as np
import mysql.connector
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Frame, Label, LEFT
from PIL import Image, ImageTk
from tkinter import Frame, Label, LEFT, Button, Toplevel, filedialog, messagebox, simpledialog
from PIL import ImageTk, Image
import cv2
import face_recognition
import json
import tkinter.font as tkfont

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

def mainimg(root, main_app):
    class ImageProcessingApp:
        def __init__(self, root, main_app):
            self.root = root
            self.main_app = main_app
            self.root.attributes("-fullscreen", True)
            self.root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
            
            # Modern color scheme
            self.bg_color = '#201E43'
            self.card_color = '#1A1A3A'
            self.primary_color = '#4A6FA5'
            self.text_color = '#FFFFFF'
            
            # Set background
            self.set_background()
            
            # Create header (same as in facemain)
            self.create_header()
            
            # Create main container
            self.main_frame = Frame(self.root, bg=self.card_color, padx=20, pady=20)
            self.main_frame.place(relx=0.5, rely=0.5, anchor='center', width=600, height=400)
            
            # Title label
            title_label = Label(self.main_frame, text="Image Processing", font=("Segoe UI", 24, "bold"), 
                               bg=self.card_color, fg=self.text_color)
            title_label.pack(pady=(0, 30), anchor='center')
            
            # Button container
            button_frame = Frame(self.main_frame, bg=self.card_color)
            button_frame.pack(expand=True, fill='both')
            
            # Create rounded buttons (centered)
            self.add_ref_btn = RoundedButton(
                button_frame,
                text="Add Reference Image",
                btnbackground=self.primary_color,
                btnforeground=self.text_color,
                clicked=lambda: self.open_file_dialog(True),
                font_size=16,
                height=60,
                width=400
            )
            self.add_ref_btn.pack(pady=10, anchor='center')
            
            self.compare_btn = RoundedButton(
                button_frame,
                text="Compare User Image",
                btnbackground=self.primary_color,
                btnforeground=self.text_color,
                clicked=lambda: self.open_file_dialog(False),
                font_size=16,
                height=60,
                width=400
            )
            self.compare_btn.pack(pady=10, anchor='center')
            
            # Back button
            self.back_btn = RoundedButton(
                button_frame,
                text="Exit",
                btnbackground=self.primary_color,
                btnforeground=self.text_color,
                clicked=self.return_to_dashboard,
                font_size=16,
                height=60,
                width=400
            )
            self.back_btn.pack(pady=10, anchor='center')
            
            # Draw buttons
            self.add_ref_btn.draw_button()
            self.compare_btn.draw_button()
            self.back_btn.draw_button()

        def create_header(self):
            header_frame = Frame(self.root, bg=self.bg_color, padx=30, pady=20)
            header_frame.place(x=0, y=0, relwidth=1, height=140)
            
            separator = Frame(self.root, bg=self.primary_color, height=2)
            separator.place(x=0, y=140, relwidth=1)

            try:
                img = Image.open(r"C:\Users\Savio\Desktop\min proj\F_resized1.png")
                img = img.resize((380, 114), Image.Resampling.LANCZOS)
                self.header_image = ImageTk.PhotoImage(img)
                img_label = Label(header_frame, image=self.header_image, bg=self.bg_color)
                img_label.pack(side=LEFT, padx=20)
            except Exception as e:
                header_label = Label(header_frame, text="Face Recognition", font=("Segoe UI", 24, "bold"), 
                                   bg=self.bg_color, fg=self.text_color)
                header_label.pack(side=LEFT, padx=20)

        def return_to_dashboard(self):
            self.root.destroy()
            self.main_app.show_main_window()

        def set_background(self):
            try:
                bg_image = Image.open(r"C:\Users\Savio\Desktop\min proj\bg.png")
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(bg_image)
                bg_label = Label(self.root, image=self.bg_photo)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label.lower()  # Ensure background stays behind other widgets
            except Exception as e:
                self.root.configure(bg=self.bg_color)

        def connect_db(self):
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="rootsavio321",
                    database="facerecognitiondb"
                )
                self.create_table(conn)
                return conn
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error connecting to database: {err}")
                return None

        def create_table(self, conn):
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS reference_images (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        image_encoding TEXT NOT NULL,
                        image_path TEXT NOT NULL
                    )
                """)
                conn.commit()
                cursor.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error creating table: {err}")

        def add_reference_image(self, image_path, name):
            img = cv2.imread(image_path)
            if img is None:
                messagebox.showerror("Error", "Could not load image. Please try a different file.")
                return
            
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)
            
            if not encodings:
                messagebox.showerror("Error", "No face detected in the image. Try another image.")
                return

            img_encoding = encodings[0]
            img_encoding_str = json.dumps(img_encoding.tolist())

            conn = self.connect_db()
            if conn is None:
                return
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "INSERT INTO reference_images (name, image_encoding, image_path) VALUES (%s, %s, %s)",
                    (name, img_encoding_str, image_path)
                )
                conn.commit()
                messagebox.showinfo("Success", f"Reference image for {name} added successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error saving data: {err}")
            finally:
                cursor.close()
                conn.close()

        def show_matched_image(self, image_path):
            try:
                top = Toplevel()
                top.title("Matched Image")
                
                self.matched_image = Image.open(image_path)
                self.matched_image = self.matched_image.resize((400, 400), Image.LANCZOS)
                self.matched_photo = ImageTk.PhotoImage(self.matched_image)

                img_label = Label(top, image=self.matched_photo)
                img_label.pack()
                
                top.matched_photo = self.matched_photo
            except Exception as e:
                messagebox.showerror("Error", f"Error displaying matched image: {str(e)}")

        def compare_user_image(self, user_img_path):
            img = cv2.imread(user_img_path)
            if img is None:
                messagebox.showerror("Error", "Could not load image. Please try a different file.")
                return
            
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)

            if not encodings:
                messagebox.showinfo("No Match", "No face detected in the image.")
                return

            img_encoding = encodings[0]

            conn = self.connect_db()
            if conn is None:
                return
            cursor = conn.cursor()
            
            try:
                cursor.execute("SELECT name, image_encoding, image_path FROM reference_images")
                results = cursor.fetchall()

                for name, encoding_str, image_path in results:
                    ref_encoding = json.loads(encoding_str)
                    result = face_recognition.compare_faces([ref_encoding], img_encoding)
                    if result[0]:
                        messagebox.showinfo("Match Found", f"MATCH FOUND with {name}")
                        cursor.close()
                        conn.close()
                        self.show_matched_image(image_path)
                        return
                
                messagebox.showinfo("Match Not Found", "MATCH NOT FOUND")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error retrieving data: {err}")
            finally:
                cursor.close()
                conn.close()

        def open_file_dialog(self, is_reference):
            file_path = filedialog.askopenfilename()
            if file_path:
                if is_reference:
                    name = simpledialog.askstring("Input", "Enter the name for the reference image:")
                    if name:
                        self.add_reference_image(file_path, name)
                else:
                    self.compare_user_image(file_path)

    app = ImageProcessingApp(root, main_app)

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.toggle_fullscreen)
        
        # Modern color scheme
        self.bg_color = '#201E43'
        self.card_color = '#1A1A3A'
        self.primary_color = '#4A6FA5'
        self.accent_color = '#6D9DC5'
        self.text_color = '#FFFFFF'
        
        # Initialize UI
        self.show_main_window()

        # Database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootsavio321",
            database="facerecognitiondb"
        )
        self.cursor = self.db.cursor()

    def show_main_window(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Set background
        self.set_background()
        
        # Create header
        self.create_header()
        
        # Main content
        self.create_main_content()

    def set_background(self):
        try:
            bg_image = Image.open(r"C:\Users\Savio\Desktop\min proj\bg.png")
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()  # Ensure background stays behind other widgets
        except Exception as e:
            self.root.configure(bg=self.bg_color)

    def create_header(self):
        header_frame = Frame(self.root, bg=self.bg_color, padx=30, pady=20)
        header_frame.place(x=0, y=0, relwidth=1, height=140)
        
        separator = Frame(self.root, bg=self.primary_color, height=2)
        separator.place(x=0, y=140, relwidth=1)

        try:
            img = Image.open(r"C:\Users\Savio\Desktop\min proj\F_resized1.png")
            img = img.resize((380, 114), Image.Resampling.LANCZOS)
            self.header_image = ImageTk.PhotoImage(img)
            img_label = Label(header_frame, image=self.header_image, bg=self.bg_color)
            img_label.pack(side=LEFT, padx=20)
        except Exception as e:
            header_label = Label(header_frame, text="Face Recognition", font=("Segoe UI", 24, "bold"), 
                               bg=self.bg_color, fg=self.text_color)
            header_label.pack(side=LEFT, padx=20)

    def create_main_content(self):
        main_frame = Frame(self.root, bg=self.card_color)
        main_frame.place(relx=0.5, rely=0.5, anchor='center', width=600, height=500)
        
        title_label = Label(main_frame, text="Face Recognition", font=("Segoe UI", 24, "bold"), 
                          bg=self.card_color, fg=self.text_color)
        title_label.pack(pady=(20, 30), anchor='center')
        
        button_frame = Frame(main_frame, bg=self.card_color)
        button_frame.pack(expand=True, fill='both', padx=40, pady=20)
        
        buttons = [
            ("Add Reference Image", self.add_reference_image),
            ("Facial Recognition", self.start_face_recognition),
            ("Image Processing", self.launch_image_processing),
            ("Exit", self.return_to_dashboard)
        ]
        
        for text, command in buttons:
            btn = RoundedButton(
                button_frame,
                text=text,
                btnbackground=self.primary_color,
                btnforeground=self.text_color,
                clicked=command,
                font_size=16,
                height=60,
                width=400
            )
            btn.pack(pady=10, anchor='center')
            btn.draw_button()

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def return_to_dashboard(self):
        self.db.close()
        self.root.destroy()

    def launch_image_processing(self):
        self.root.withdraw()
        img_window = tk.Toplevel()
        mainimg(img_window, self)
        img_window.protocol("WM_DELETE_WINDOW", lambda: self.on_img_window_close(img_window))

    def on_img_window_close(self, img_window):
        img_window.destroy()
        self.root.deiconify()
        self.show_main_window()  # Recreate the main window elements

    def add_reference_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            name = simpledialog.askstring("Input", "Enter the name for this person:")
            if name:
                image = face_recognition.load_image_file(file_path)
                try:
                    encoding = face_recognition.face_encodings(image)[0]
                    encoded_face = pickle.dumps(encoding)
                    self.cursor.execute("INSERT INTO faces (name, encoding) VALUES (%s, %s)", (name, encoded_face))
                    self.db.commit()
                    messagebox.showinfo("Success", f"Added {name} successfully.")
                except IndexError:
                    messagebox.showerror("Error", "No face found in the image. Please try another image.")

    def start_face_recognition(self):
     self.cursor.execute("SELECT name, encoding FROM faces")
     results = self.cursor.fetchall()

     known_face_encodings = []
     known_face_names = []

     for name, encoding in results:
        known_face_names.append(name)
        known_face_encodings.append(pickle.loads(encoding))

     video_capture = cv2.VideoCapture(0)
     # Set smaller resolution for faster processing
     video_capture.set(3, 640)  # Width
     video_capture.set(4, 480)  # Height
    
     # Skip frames for better performance
     frame_skip = 2
     frame_count = 0

     while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        frame_count += 1
        if frame_count % frame_skip != 0:
            continue
            
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        
        # Convert to RGB only once
        rgb_small_frame = small_frame[:, :, ::-1]
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Scale back up face locations
            top *= 2
            right *= 2
            bottom *= 2
            left *= 2
            
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 255), 2)

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

     video_capture.release()
     cv2.destroyAllWindows()

def facemain(root):
    app = FaceRecognitionApp(root)

if __name__ == "__main__":
    root = tk.Tk()
    facemain(root)
    root.mainloop()