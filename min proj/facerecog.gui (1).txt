import cv2
import face_recognition
import numpy as np
import mysql.connector
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Frame, Label, LEFT
from PIL import Image, ImageTk

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition App")

        # Set fullscreen mode
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.toggle_fullscreen)  # Allow exiting fullscreen with Esc

        # Set background image
        self.background_image = Image.open(r"C:\Users\Savio\Documents\mini proj\bg.png")
        self.background_image = self.background_image.resize((2560, 1440), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        # Create a label for the background
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        header_frame = Frame(root, bg="#201E43", padx=10, pady=20)
        header_frame.pack(fill=tk.X)

        try:
            self.header_image = Image.open(r"C:\Users\Savio\Documents\mini proj\F_resized1.png")
            self.header_image = self.header_image.resize((400, 120), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.header_image)
            img_label = Label(header_frame, image=self.photo, bg="#201E43")
            img_label.pack(side=LEFT, padx=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading header image: {str(e)}")

        # MySQL database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootsavio321",
            database="facerecognitiondb"
        )
        self.cursor = self.db.cursor()

        # Call the GUI setup function
        self.create_widgets()

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode."""
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

    def create_widgets(self):
        button_frame = Frame(self.root, bg=self.root.cget('bg'))  # Match button frame to the root background
        button_frame.pack(pady=10)

        # Add Reference Image Button
        self.add_reference_button = tk.Button(
             root, text="Add Reference Image", font=("Arial", 12), fg="white", bg="#201E43",command=self.add_reference_image,  padx=20, pady=10
        )
        self.add_reference_button.pack(pady=20)

        # Face Recognition Button
        self.recognition_button = tk.Button(
            root, text="Facial Recognition", font=("Arial", 12), fg="white", bg="#201E43",command=self.start_face_recognition,  padx=20, pady=10
        )
        self.recognition_button.pack(pady=20)

        # Exit Button
        self.exit_button = tk.Button(
            
            root, text="Exit", font=("Arial", 12), fg="white", bg="#201E43", command=self.root.quit, padx=20, pady=10
        )
        self.exit_button.pack(pady=20)

    def add_reference_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if file_path:
            name = simpledialog.askstring("Input", "Enter the name for this person:")
            if name:
                image = face_recognition.load_image_file(file_path)
                try:
                    encoding = face_recognition.face_encodings(image)[0]
                    # Store encoding as a blob
                    encoded_face = pickle.dumps(encoding)
                    self.cursor.execute("INSERT INTO faces (name, encoding) VALUES (%s, %s)", (name, encoded_face))
                    self.db.commit()
                    messagebox.showinfo("Success", f"Added {name} successfully.")
                except IndexError:
                    messagebox.showerror("Error", "No face found in the image. Please try another image.")

    def start_face_recognition(self):
        # Retrieve all stored encodings
        self.cursor.execute("SELECT name, encoding FROM faces")
        results = self.cursor.fetchall()
        
        known_face_encodings = []
        known_face_names = []

        for name, encoding in results:
            known_face_names.append(name)
            known_face_encodings.append(pickle.loads(encoding))  # Decode from blob

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

                # Draw rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Display the name above the rectangle
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 255), 2)
                

            cv2.imshow("Video", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()  