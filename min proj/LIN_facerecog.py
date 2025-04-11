import cv2
import face_recognition
import numpy as np
import mysql.connector
import pickle
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Frame, Label, LEFT
from PIL import Image, ImageTk
from threading import Thread
import queue
import time

class VideoCaptureThread:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.q = queue.Queue()
        self.thread = Thread(target=self._reader)
        self.thread.daemon = True
        self.thread.start()

    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

    def release(self):
        self.cap.release()

def facemain(root):  
    class FaceRecognitionApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Face Recognition App")

            self.root.attributes("-fullscreen", True)
            self.root.bind("<Escape>", self.toggle_fullscreen) 

            self.background_image = Image.open(r"C:\Users\Savio\Desktop\min proj\bg.png")
            self.background_image = self.background_image.resize((2560, 1440), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(self.background_image)

            self.bg_label = Label(root, image=self.bg_image)
            self.bg_label.place(relwidth=1, relheight=1)

            header_frame = Frame(root, bg="#201E43", padx=10, pady=20)
            header_frame.pack(fill=tk.X)

            try:
                self.header_image = Image.open(r"C:\Users\Savio\Downloads\Screenshot_2025-03-28_170205-removebg-preview.png")
                self.header_image = self.header_image.resize((300, 150), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(self.header_image)
                img_label = Label(header_frame, image=self.photo, bg="#201E43")
                img_label.pack(side=LEFT, padx=5)
            except Exception as e:
                messagebox.showerror("Error", f"Error loading header image: {str(e)}")

            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="rootsavio321",
                database="facerecognitiondb"
            )
            self.cursor = self.db.cursor()

            self.create_widgets()

        def toggle_fullscreen(self, event=None):
            """Toggle fullscreen mode."""
            self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

        def create_widgets(self):
            button_frame = Frame(self.root, bg=self.root.cget('bg'))  
            button_frame.pack(pady=10)

            self.add_reference_button = tk.Button(
                self.root, text="Add Reference Image", font=("Arial", 12), fg="white", bg="#201E43", command=self.add_reference_image, padx=20, pady=10
            )
            self.add_reference_button.pack(pady=20)

            self.recognition_button = tk.Button(
                self.root, text="Facial Recognition", font=("Arial", 12), fg="white", bg="#201E43", command=self.start_face_recognition, padx=20, pady=10
            )
            self.recognition_button.pack(pady=20)

            self.image_button = tk.Button(
                self.root, text="Image Processing", font=("Arial", 12), fg="white", bg="#201E43",
                command=self.open_mainimg, padx=20, pady=10
            )
            self.image_button.pack(pady=20)

            self.exit_button = tk.Button(
                self.root, 
                text="Exit", 
                font=("Arial", 12), 
                fg="white", 
                bg="#201E43", 
                command=self.exit_app,
                padx=20, 
                pady=10
            )
            self.exit_button.pack(pady=20)

        def exit_app(self):
            """Close database connection and exit the application"""
            self.db.close()
            self.root.destroy()

        def open_mainimg(self):
            """Open the image processing module"""
            from LIN_img import mainimg
            self.root.destroy()
            mainimg()  

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

            video_capture = VideoCaptureThread(0)
            
            
            face_tracker = {}  
            tracker_id = 0
            frame_counter = 0
            detection_interval = 3
            tracking_frames = 3  
            
            prev_time = 0
            curr_time = 0
            
            while True:
                frame = video_capture.read()
                curr_time = time.time()
                fps = 1/(curr_time - prev_time)
                prev_time = curr_time
                
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                rgb_small_frame = small_frame[:, :, ::-1]
                
                current_face_locations = []
                current_face_names = []
                
                if frame_counter % detection_interval == 0:
                    face_locations = face_recognition.face_locations(
                        rgb_small_frame, 
                        number_of_times_to_upsample=1, 
                        model="hog"
                    )
                    
                    face_tracker = {}
                    tracker_id = 0
                    
                    for (top, right, bottom, left) in face_locations:
                        top *= 2; right *= 2; bottom *= 2; left *= 2
                        
                        face_encoding = face_recognition.face_encodings(
                            rgb_small_frame,
                            [(top//2, right//2, bottom//2, left//2)]
                        )[0]
                        
                        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        name = "Unknown"
                        
                        if True in matches:
                            first_match_index = matches.index(True)
                            name = known_face_names[first_match_index]
                        
                        face_tracker[tracker_id] = {
                            'name': name,
                            'location': (left, top, right, bottom),
                            'last_seen': frame_counter
                        }
                        current_face_locations.append((left, top, right, bottom))
                        current_face_names.append(name)
                        tracker_id += 1
                else:
                    for face_id, face_data in list(face_tracker.items()):
                        if frame_counter - face_data['last_seen'] > tracking_frames:
                            face_tracker.pop(face_id)
                            continue
                            
                        left, top, right, bottom = face_data['location']
                        current_face_locations.append((left, top, right, bottom))
                        current_face_names.append(face_data['name'])
                
                for (left, top, right, bottom), name in zip(current_face_locations, current_face_names):
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow("Video", frame)
                frame_counter += 1
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            video_capture.release()
            cv2.destroyAllWindows()

    app = FaceRecognitionApp(root)

if __name__ == "__main__":
    root = tk.Tk()  
    facemain(root)
    root.mainloop()