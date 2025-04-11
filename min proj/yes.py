import cv2
import face_recognition
import numpy as np
import mysql.connector
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Frame, Label, LEFT, Button, Toplevel
from PIL import Image, ImageTk
import json

def clear_window(root):
    """Clear all widgets from the window"""
    for widget in root.winfo_children():
        widget.destroy()

def facemain(root):  
    class FaceRecognitionApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Face Recognition App")
            self.root.attributes("-fullscreen", True)
            self.root.bind("<Escape>", self.toggle_fullscreen) 

            # Background setup
            self.background_image = Image.open(r"C:\Users\Savio\Desktop\min proj\bg.png")
            self.background_image = self.background_image.resize((2560, 1440), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(self.background_image)

            self.bg_label = Label(root, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)

            # Header frame
            header_frame = Frame(root, bg="#201E43", padx=10, pady=20)
            header_frame.pack(fill=tk.X)

            try:
                self.header_image = Image.open(r"C:\Users\Savio\Desktop\min proj\F_resized1.png")
                self.header_image = self.header_image.resize((400, 120), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(self.header_image)
                img_label = Label(header_frame, image=self.photo, bg="#201E43")
                img_label.pack(side=LEFT, padx=5)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading header image: {str(e)}")

            # Database connection
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="facerecognitiondb"
            )
            self.cursor = self.db.cursor()

            self.create_widgets()

        def toggle_fullscreen(self, event=None):
            self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

        def create_widgets(self):
            button_frame = Frame(self.root, bg=self.root.cget('bg'))
            button_frame.pack(pady=10)

            # Buttons
            self.add_reference_button = tk.Button(
                self.root, text="Add Reference Image", font=("Arial", 12), 
                fg="white", bg="#201E43", command=self.add_reference_image, 
                padx=20, pady=10
            )
            self.add_reference_button.pack(pady=20)

            self.recognition_button = tk.Button(
                self.root, text="Facial Recognition", font=("Arial", 12), 
                fg="white", bg="#201E43", command=self.start_face_recognition, 
                padx=20, pady=10
            )
            self.recognition_button.pack(pady=20)

            self.image_processing_button = tk.Button(
                self.root, text="Image Processing", font=("Arial", 12), 
                fg="white", bg="#201E43", command=lambda: self.show_image_processing(),
                padx=20, pady=10
            )
            self.image_processing_button.pack(pady=20)

            self.exit_button = tk.Button(
                self.root, text="Exit", font=("Arial", 12), 
                fg="white", bg="#201E43", command=self.exit_app,
                padx=20, pady=10
            )
            self.exit_button.pack(pady=20)

        def show_image_processing(self):
            """Show image processing screen in the same window"""
            clear_window(self.root)
            ImageProcessingApp(self.root)

        def exit_app(self):
            self.db.close()
            self.root.destroy()

        def add_reference_image(self):
            file_path = filedialog.askopenfilename(
                title="Select an Image", 
                filetypes=[("Image Files", "*.jpg *.png *.jpeg")]
            )
            if file_path:
                name = simpledialog.askstring("Input", "Enter the name for this person:")
                if name:
                    image = face_recognition.load_image_file(file_path)
                    try:
                        encoding = face_recognition.face_encodings(image)[0]
                        encoded_face = pickle.dumps(encoding)
                        self.cursor.execute(
                            "INSERT INTO faces (name, encoding) VALUES (%s, %s)", 
                            (name, encoded_face)
                        )
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

            while True:
                ret, frame = video_capture.read()
                if not ret:
                    break

                face_locations = face_recognition.face_locations(frame)
                face_encodings = face_recognition.face_encodings(frame, face_locations)

                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
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

    app = FaceRecognitionApp(root)

class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        
        # Background setup
        try:
            self.bg_image = Image.open(r"C:\Users\Savio\Desktop\min proj\bg.png")
            self.bg_image = self.bg_image.resize(
                (root.winfo_screenwidth(), root.winfo_screenheight()), 
                Image.LANCZOS
            )
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            bg_label = tk.Label(root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading background: {str(e)}")

        # Header frame
        self.header_frame = tk.Frame(root, bg="#201E43", height=120)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)

        try:
            self.header_image = Image.open(r"C:\Users\Savio\Desktop\min proj\F_resized1.png")
            self.header_image = self.header_image.resize((400, 100), Image.LANCZOS)
            self.header_photo = ImageTk.PhotoImage(self.header_image)
            header_label = tk.Label(self.header_frame, image=self.header_photo, bg="#201E43")
            header_label.pack(side=tk.LEFT, padx=20)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading header image: {str(e)}")

        # Button container
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=100)

        # Button style
        button_style = {
            'font': ("Arial", 12),
            'fg': "white",
            'bg': "#201E43",
            'padx': 20,
            'pady': 10
        }

        # Image processing buttons
        tk.Button(
            self.button_frame, 
            text="Add Reference Image", 
            command=lambda: self.open_file_dialog(True),
            **button_style
        ).pack(pady=15)

        tk.Button(
            self.button_frame, 
            text="Compare User Image", 
            command=lambda: self.open_file_dialog(False),
            **button_style
        ).pack(pady=15)

        tk.Button(
            self.button_frame, 
            text="Back to Main Menu", 
            command=lambda: facemain(root),
            **button_style
        ).pack(pady=15)

        # Database connection
        self.db = self.connect_db()

    def connect_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="face_recognition_db"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to database: {err}")
            return None

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
            
            matched_image = Image.open(image_path)
            matched_image = matched_image.resize((400, 400), Image.LANCZOS)
            matched_photo = ImageTk.PhotoImage(matched_image)

            img_label = Label(top, image=matched_photo)
            img_label.pack()
            
            top.matched_photo = matched_photo
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

if __name__ == "__main__":
    root = tk.Tk()
    facemain(root)
    root.mainloop()