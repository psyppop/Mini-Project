import cv2
import face_recognition
import numpy as np
import mysql.connector
import pickle
import tkinter as tk
from tkinter import *  # This will import all constants including BOTH
from tkinter import filedialog, messagebox, simpledialog, Frame, Label, LEFT, Button, Toplevel, Entry
from PIL import Image, ImageTk
import json
import tkinter.font as tkfont
import io

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
            
            # Configure the root window
            self.root.title("ForenSync - Facial Analysis")
            self.root.attributes('-fullscreen', True)
            self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))
            
            # Modern color scheme
            self.bg_color = '#201E43'
            self.card_color = '#1A1A3A'
            self.primary_color = '#4A6FA5'
            self.accent_color = '#6D9DC5'
            self.text_color = '#FFFFFF'
            self.highlight_color = '#7FB2E5'
            
            # Setup styles and UI elements
            self.setup_styles()
            self.set_background()
            self.create_header()
            self.create_main_content()

        def setup_styles(self):
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
                img_label = Label(header_frame, image=self.header_image, bg=self.bg_color)
                img_label.pack(side=LEFT, padx=20)
            except Exception as e:
                header_label = Label(header_frame, text="ForenSync", font=self.header_font, 
                                   bg=self.bg_color, fg=self.text_color)
                header_label.pack(side=LEFT, padx=20)

        def create_main_content(self):
            # Main container with proper padding
            main_frame = Frame(self.root, bg=self.card_color)
            main_frame.place(x=50, y=180, relwidth=0.9, height=550, anchor='nw')
            
            welcome_panel = Frame(main_frame, bg=self.primary_color)
            welcome_panel.pack(fill='x', pady=(0, 20))
            
            welcome_label = Label(
                welcome_panel, 
                text="Facial Analysis",
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
                text="IMAGE PROCESSING AND FACE RECOGNITION",
                bg=self.primary_color,
                fg=self.accent_color,
                font=self.subtitle_font,
                padx=25,
                anchor='w'
            )
            subtitle.pack(fill='x', pady=(0, 12))

            # Separator line
            Frame(main_frame, bg=self.accent_color, height=1).pack(fill='x', pady=10)
            
            # Button container with proper padding
            button_container = Frame(main_frame, bg=self.card_color, padx=25, pady=10)
            button_container.pack(fill='both', expand=True)

            buttons = [
                ("🔍 ADD REFERENCE IMAGE", lambda: self.open_file_dialog(True)),
                ("👤 COMPARE USER IMAGE", lambda: self.open_file_dialog(False)),
                ("🔙 RETURN TO DASHBOARD", self.return_to_dashboard),
            ]
            
            for text, command in buttons:
                btn_frame = Frame(button_container, bg=self.card_color)
                btn_frame.pack(fill='x', pady=8)
                
                btn = RoundedButton(
                    btn_frame,
                    text=text,
                    btnbackground=self.primary_color,
                    btnforeground=self.text_color,
                    clicked=command,
                    height=60,
                    font_size=self.button_font_size
                )
                btn.pack(fill='x')
                btn.draw_button()

        def return_to_dashboard(self):
            self.root.destroy()
            self.main_app.show_main_window()

        def set_background(self):
            try:
                bg_image = Image.open("bg.png")
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

def facemain(root, dashboard_window=None):
    app = FaceRecognitionApp(root, dashboard_window)

class FaceRecognitionApp:
    def __init__(self, root, dashboard_window=None):
        self.root = root
        self.dashboard_window = dashboard_window
        
        # Configure the root window
        self.root.title("ForenSync - Facial Analysis")
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.attributes('-fullscreen', False))
        
        # Modern color scheme
        self.bg_color = '#201E43'
        self.card_color = '#1A1A3A'
        self.primary_color = '#4A6FA5'
        self.accent_color = '#6D9DC5'
        self.text_color = '#FFFFFF'
        self.highlight_color = '#7FB2E5'
        
        # Initialize database connection
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="facerecognitiondb"
            )
            self.cursor = self.db.cursor()
            
            # Create table if it doesn't exist
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS face_recognition (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    face_data LONGBLOB NOT NULL,
                    face_image LONGBLOB
                )
            """)
            self.db.commit()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            self.db = None
            self.cursor = None
        
        # Setup styles and UI elements
        self.setup_styles()
        self.set_background()
        self.create_header()
        self.create_main_content()

    def __del__(self):
        # Close database connection when object is destroyed
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'db') and self.db:
            self.db.close()

    def setup_styles(self):
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
            img_label = Label(header_frame, image=self.header_image, bg=self.bg_color)
            img_label.pack(side=LEFT, padx=20)
        except Exception as e:
            header_label = Label(header_frame, text="ForenSync", font=self.header_font, 
                               bg=self.bg_color, fg=self.text_color)
            header_label.pack(side=LEFT, padx=20)

    def create_main_content(self):
        # Main container with proper padding
        main_frame = Frame(self.root, bg=self.card_color)
        main_frame.place(x=50, y=180, relwidth=0.9, height=550, anchor='nw')
        
        welcome_panel = Frame(main_frame, bg=self.primary_color)
        welcome_panel.pack(fill='x', pady=(0, 20))
        
        welcome_label = Label(
            welcome_panel, 
            text="Facial Analysis",
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
            text="FACE RECOGNITION AND COMPARISON",
            bg=self.primary_color,
            fg=self.accent_color,
            font=self.subtitle_font,
            padx=25,
            anchor='w'
        )
        subtitle.pack(fill='x', pady=(0, 12))

        # Separator line
        Frame(main_frame, bg=self.accent_color, height=1).pack(fill='x', pady=10)
        
        # Button container with proper padding
        button_container = Frame(main_frame, bg=self.card_color, padx=25, pady=10)
        button_container.pack(fill='both', expand=True)

        buttons = [
            ("👤 ADD FACE", self.add_face),
            ("🔍 RECOGNIZE FACE", self.recognize_face),
            ("🔄 COMPARE IMAGES", self.compare_images),
            ("🔙 RETURN TO DASHBOARD", self.return_to_dashboard),
        ]
        
        for text, command in buttons:
            btn_frame = Frame(button_container, bg=self.card_color)
            btn_frame.pack(fill='x', pady=8)
            
            btn = RoundedButton(
                btn_frame,
                text=text,
                btnbackground=self.primary_color,
                btnforeground=self.text_color,
                clicked=command,
                height=60,
                font_size=self.button_font_size
            )
            btn.pack(fill='x')
            btn.draw_button()

    def set_background(self):
        try:
            bg_image = Image.open("bg.png")
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()  # Ensure background stays behind other widgets
        except Exception as e:
            self.root.configure(bg=self.bg_color)

    def return_to_dashboard(self):
        """Return to the dashboard by closing the current window and showing the dashboard"""
        if self.dashboard_window:
            self.root.destroy()  # Close the facial analysis window
            self.dashboard_window.deiconify()  # Show the dashboard window

    def add_face(self):
        # Create a new window for adding a face
        add_window = Toplevel(self.root)
        add_window.title("Add Face")
        add_window.geometry("400x400")
        add_window.configure(bg=self.bg_color)
        
        # Name entry
        name_label = Label(add_window, text="Enter Name:", font=self.subtitle_font, 
                         bg=self.bg_color, fg=self.text_color)
        name_label.pack(pady=10)
        name_entry = Entry(add_window, font=self.subtitle_font)
        name_entry.pack(pady=5)

        def upload_image():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a name")
                return

            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
            )
            
            if file_path:
                try:
                    # Load and process the image
                    image = face_recognition.load_image_file(file_path)
                    face_locations = face_recognition.face_locations(image)
                    
                    if not face_locations:
                        messagebox.showerror("Error", "No face detected in the image")
                        return
                    
                    face_encoding = face_recognition.face_encodings(image, face_locations)[0]
                    face_encoding_bytes = pickle.dumps(face_encoding)
                    
                    # Read the image file as binary data
                    with open(file_path, 'rb') as file:
                        image_data = file.read()
                    
                    # Store in database
                    self.cursor.execute("""
                        INSERT INTO face_recognition (name, face_data, face_image) 
                        VALUES (%s, %s, %s)
                    """, (name, face_encoding_bytes, image_data))
                    self.db.commit()
                    
                    messagebox.showinfo("Success", f"Face data for {name} has been saved!")
                    add_window.destroy()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to process image: {str(e)}")

        # Upload button
        upload_button = RoundedButton(
            add_window,
            text="📤 UPLOAD IMAGE",
            btnbackground=self.primary_color,
            btnforeground=self.text_color,
            clicked=upload_image,
            height=40,
            font_size=14
        )
        upload_button.pack(pady=10)
        upload_button.draw_button()

        # Separator
        separator = Label(add_window, text="- OR -", font=self.subtitle_font, 
                        bg=self.bg_color, fg=self.accent_color)
        separator.pack(pady=10)

        def capture_face():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a name")
                return

            try:
                # Try different camera indices and backends
                camera_opened = False
                cap = None
                
                # Try DirectShow backend first
                cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                if cap.isOpened():
                    camera_opened = True
                else:
                    # Try default backend
                    cap = cv2.VideoCapture(0)
                    if cap.isOpened():
                        camera_opened = True
                    else:
                        # Try other camera indices
                        for i in range(1, 4):
                            cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
                            if cap.isOpened():
                                camera_opened = True
                                break
                            cap.release()

                if not camera_opened:
                    messagebox.showerror("Error", "Could not access any camera")
                    return

                # Set camera properties for better performance
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                cap.set(cv2.CAP_PROP_FPS, 30)

                face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                face_detected = False

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        messagebox.showerror("Error", "Failed to grab frame from camera")
                        break

                    # Convert to RGB for face_recognition
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        face_detected = True

                    cv2.imshow('Capture Face - Press SPACE when face is detected, ESC to cancel', frame)

                    key = cv2.waitKey(1)
                    if key == 27:  # ESC key
                        break
                    elif key == 32 and face_detected:  # SPACE key and face is detected
                        try:
                            # Get face encoding
                            face_locations = face_recognition.face_locations(rgb_frame)
                            if face_locations:
                                face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                                face_encoding_bytes = pickle.dumps(face_encoding)
                                
                                # Convert frame to image data
                                _, buffer = cv2.imencode('.jpg', frame)
                                image_data = buffer.tobytes()
                                
                                # Store in database
                                self.cursor.execute("""
                                    INSERT INTO face_recognition (name, face_data, face_image) 
                                    VALUES (%s, %s, %s)
                                """, (name, face_encoding_bytes, image_data))
                                self.db.commit()
                                
                                messagebox.showinfo("Success", f"Face data for {name} has been saved!")
                                break
                            else:
                                messagebox.showerror("Error", "No face detected. Please try again.")
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to save face data: {str(e)}")
                            break

            except Exception as e:
                messagebox.showerror("Error", f"Camera error: {str(e)}")
            finally:
                if 'cap' in locals() and cap is not None:
                    cap.release()
                cv2.destroyAllWindows()
                add_window.destroy()

        # Capture button
        capture_button = RoundedButton(
            add_window,
            text="📸 CAPTURE FACE",
            btnbackground=self.primary_color,
            btnforeground=self.text_color,
            clicked=capture_face,
            height=40,
            font_size=14
        )
        capture_button.pack(pady=20)
        capture_button.draw_button()

    def recognize_face(self):
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Error", "Could not access camera")
                return

            # Get all faces from database
            self.cursor.execute("SELECT name, face_data FROM face_recognition")
            known_faces = self.cursor.fetchall()

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Find faces in the frame
                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    name = "Unknown"
                    
                    # Compare with known faces
                    for known_name, known_face_data in known_faces:
                        known_encoding = pickle.loads(known_face_data)
                        if face_recognition.compare_faces([known_encoding], face_encoding)[0]:
                            name = known_name
                            break

                    # Draw rectangle and name
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

                cv2.imshow('Face Recognition - Press ESC to exit', frame)

                if cv2.waitKey(1) == 27:  # ESC key
                    break

        finally:
            cap.release()
            cv2.destroyAllWindows()

    def compare_images(self):
        # Create comparison window
        compare_window = Toplevel(self.root)
        compare_window.title("Compare Images")
        compare_window.geometry("1000x700")
        compare_window.configure(bg=self.bg_color)

        # Main container frame
        main_frame = Frame(compare_window, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title
        title_label = Label(main_frame, text="Compare Images", 
                          font=self.welcome_font, 
                          bg=self.bg_color, fg=self.text_color)
        title_label.pack(pady=(0, 20))

        # Frame for image containers
        images_frame = Frame(main_frame, bg=self.bg_color)
        images_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Left frame (Input Image)
        left_frame = Frame(images_frame, bg=self.bg_color, width=400, height=400)
        left_frame.pack(side=LEFT, padx=20)
        left_frame.pack_propagate(False)

        # Right frame (Matched Image)
        right_frame = Frame(images_frame, bg=self.bg_color, width=400, height=400)
        right_frame.pack(side=RIGHT, padx=20)
        right_frame.pack_propagate(False)

        # Labels for frames
        Label(left_frame, text="Input Image", font=self.subtitle_font, 
              bg=self.bg_color, fg=self.text_color).pack(pady=(0, 10))
        Label(right_frame, text="Matched Image", font=self.subtitle_font, 
              bg=self.bg_color, fg=self.text_color).pack(pady=(0, 10))

        # Image placeholders with borders
        input_frame = Frame(left_frame, bg="white", padx=2, pady=2)
        input_frame.pack(expand=True)
        input_placeholder = Label(input_frame, text="No image selected", 
                                bg=self.primary_color, fg=self.text_color,
                                width=400, height=400)
        input_placeholder.pack()

        match_frame = Frame(right_frame, bg="white", padx=2, pady=2)
        match_frame.pack(expand=True)
        match_placeholder = Label(match_frame, text="No match found", 
                                bg=self.primary_color, fg=self.text_color,
                                width=400, height=400)
        match_placeholder.pack()

        # Status label
        status_label = Label(main_frame, text="Select an image to compare", 
                           font=self.subtitle_font, 
                           bg=self.bg_color, fg=self.text_color)
        status_label.pack(pady=20)

        def select_image():
            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
            )
            
            if file_path:
                try:
                    # Load and display input image
                    input_image = Image.open(file_path)
                    input_image = input_image.resize((400, 400), Image.Resampling.LANCZOS)
                    input_photo = ImageTk.PhotoImage(input_image)
                    input_placeholder.configure(image=input_photo, text="")
                    input_placeholder.image = input_photo  # Keep a reference
                    
                    # Process image for face recognition
                    image = face_recognition.load_image_file(file_path)
                    face_locations = face_recognition.face_locations(image)
                    
                    if not face_locations:
                        status_label.config(text="⚠️ No face detected in the image", fg="#FF0000")
                        match_placeholder.configure(text="No face detected")
                        return
                    
                    face_encoding = face_recognition.face_encodings(image, face_locations)[0]
                    
                    # Get all faces from database
                    self.cursor.execute("SELECT name, face_data FROM face_recognition")
                    known_faces = self.cursor.fetchall()
                    
                    if not known_faces:
                        status_label.config(text="⚠️ No faces found in database", fg="#FF0000")
                        return

                    # Compare with known faces
                    for known_name, known_face_data in known_faces:
                        known_encoding = pickle.loads(known_face_data)
                        if face_recognition.compare_faces([known_encoding], face_encoding)[0]:
                            # Show match found status
                            status_label.config(text=f"✅ Match found with {known_name}!", fg="#00FF00")
                            
                            # Get the matched face image from database
                            self.cursor.execute("SELECT face_image FROM face_recognition WHERE name = %s", (known_name,))
                            result = self.cursor.fetchone()
                            
                            if result and result[0]:
                                # Convert the stored image data to an image
                                matched_image = Image.open(io.BytesIO(result[0]))
                                matched_image = matched_image.resize((400, 400), Image.Resampling.LANCZOS)
                                matched_photo = ImageTk.PhotoImage(matched_image)
                                match_placeholder.configure(image=matched_photo, text="")
                                match_placeholder.image = matched_photo  # Keep a reference
                            else:
                                match_placeholder.configure(text="Stored image not available")
                            return
                    
                    # If no match found
                    status_label.config(text="❌ No matching face found in database", fg="#FF0000")
                    match_placeholder.configure(text="No Match Found")
                    
                except Exception as e:
                    status_label.config(text=f"⚠️ Error: {str(e)}", fg="#FF0000")

        # Select Image button
        select_button = RoundedButton(
            main_frame,
            text="📂 SELECT IMAGE TO COMPARE",
            btnbackground=self.primary_color,
            btnforeground=self.text_color,
            clicked=select_image,
            height=40,
            font_size=14
        )
        select_button.pack(pady=20)
        select_button.draw_button()

if __name__ == "__main__":
    root = tk.Tk()
    facemain(root)
    root.mainloop()