import tkinter as tk
from tkinter import Frame, Label, LEFT, Button, Toplevel, filedialog, messagebox, simpledialog
from PIL import ImageTk, Image
import cv2
import face_recognition
import mysql.connector
import json

def mainimg():
    class ImageProcessingApp:
        def __init__(self, root):
            self.root = root
            self.root.attributes("-fullscreen", True)
            self.root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

            try:
                # Background image
                self.bg_image = Image.open(r"C:\Users\Savio\Desktop\min proj\bg.png")
                self.bg_image = self.bg_image.resize((2560, 1440), Image.LANCZOS)
                self.bg_photo = ImageTk.PhotoImage(self.bg_image)
                
                self.bg_label = tk.Label(root, image=self.bg_photo)
                self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

                # Header frame
                self.header_frame = Frame(root, bg="#201E43", padx=10, pady=20)
                self.header_frame.pack(fill=tk.X)

                # Header image
                self.header_image = Image.open(r"C:\Users\Savio\Downloads\Screenshot_2025-03-28_165357-removebg-preview.png")
                self.header_image = self.header_image.resize((400, 120), Image.LANCZOS)
                self.header_photo = ImageTk.PhotoImage(self.header_image)
                
                self.img_label = Label(self.header_frame, image=self.header_photo, bg="#201E43")
                self.img_label.pack(side=LEFT, padx=5)

            except Exception as e:
                messagebox.showerror("Error", f"Error loading images: {str(e)}")

            # Create buttons
            self.add_ref_btn = Button(
                root,
                text="Add Reference Image",
                font=("Arial", 12),
                fg="white",
                bg="#201E43",
                command=lambda: self.open_file_dialog(True),
                padx=20,
                pady=10
            )
            self.compare_btn = Button(
                root,
                text="Compare User Image",
                font=("Arial", 12),
                fg="white",
                bg="#201E43",
                command=lambda: self.open_file_dialog(False),
                padx=20,
                pady=10
            )
            
            # Add Exit button
            self.exit_btn = Button(
                root,
                text="Exit to Face Recognition",
                font=("Arial", 12),
                fg="white",
                bg="#201E43",
                command=self.exit_to_face_recognition,
                padx=20,
                pady=10
            )

            self.add_ref_btn.pack(pady=20)
            self.compare_btn.pack(pady=20)
            self.exit_btn.pack(pady=20)

        def exit_to_face_recognition(self):
            """Close current window and return to face recognition"""
            self.root.destroy()
            from LIN_facerecog import facemain
            facemain(tk.Tk())

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
                
                # Store the image reference in the class
                self.matched_image = Image.open(image_path)
                self.matched_image = self.matched_image.resize((400, 400), Image.LANCZOS)
                self.matched_photo = ImageTk.PhotoImage(self.matched_image)

                img_label = Label(top, image=self.matched_photo)
                img_label.pack()
                
                # Keep a reference to avoid garbage collection
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

    def img_main():
        root = tk.Tk()
        app = ImageProcessingApp(root)
        root.mainloop()

    img_main()

if __name__ == "__main__":
    mainimg()