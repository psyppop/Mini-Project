import tkinter as tk
from tkinter import Frame, Label, LEFT, Button, Toplevel, filedialog, messagebox, simpledialog
from PIL import ImageTk, Image
import cv2
import face_recognition
import mysql.connector
import json

def img_main():

    def connect_db():
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

    def add_reference_image(image_path, name):
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

        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO reference_images (name, image_encoding, image_path) VALUES (%s, %s, %s)", 
                           (name, img_encoding_str, image_path))
            conn.commit()
            messagebox.showinfo("Success", f"Reference image for {name} added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error saving data: {err}")
        finally:
            cursor.close()
            conn.close()

    def show_matched_image(image_path):
        try:
            top = Toplevel()
            top.title("Matched Image")
            
            img = Image.open(image_path)
            img = img.resize((400, 400), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            img_label = Label(top, image=img_tk)
            img_label.image = img_tk
            img_label.pack()
        except Exception as e:
            messagebox.showerror("Error", f"Error displaying matched image: {str(e)}")

    def compare_user_image(user_img_path):
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

        conn = connect_db()
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
                    show_matched_image(image_path)
                    return
            
            messagebox.showinfo("Match Not Found", "MATCH NOT FOUND")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error retrieving data: {err}")
        finally:
            cursor.close()
            conn.close()

    def open_file_dialog(is_reference):
        file_path = filedialog.askopenfilename()
        if file_path:
            if is_reference:
                name = simpledialog.askstring("Input", "Enter the name for the reference image:")
                if name:
                    add_reference_image(file_path, name)
            else:
                compare_user_image(file_path)

    def create_gui():
        root = tk.Tk()
        root.attributes("-fullscreen", True)
        root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))

        try:
            bg_image = Image.open(r"C:\Users\Savio\Documents\mini proj\bg.png")
            bg_image = bg_image.resize((2560, 1440), Image.LANCZOS)
            bg_image_tk = ImageTk.PhotoImage(bg_image)
            
            bg_label = tk.Label(root, image=bg_image_tk)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            header_frame = Frame(root, bg="#201E43", padx=10, pady=20)
            header_frame.pack(fill=tk.X)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading background image: {str(e)}")

        try:
            header_image = Image.open(r"C:\Users\Savio\Documents\mini proj\F_resized1.png")
            header_image = header_image.resize((400, 120), Image.LANCZOS)
            photo = ImageTk.PhotoImage(header_image)
            img_label = Label(header_frame, image=photo, bg="#201E43")
            img_label.pack(side=LEFT, padx=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading header image: {str(e)}")

        add_ref_btn = Button(root, text="Add Reference Image", font=("Arial", 12), fg="white", bg="#201E43", 
                             command=lambda: open_file_dialog(True), padx=20, pady=10)
        compare_btn = Button(root, text="Compare User Image", font=("Arial", 12), fg="white", bg="#201E43", 
                             command=lambda: open_file_dialog(False), padx=20, pady=10)

        add_ref_btn.pack(pady=20)
        compare_btn.pack(pady=20)

        root.mainloop()

    create_gui()

if __name__ == "__main__":
    img_main()
