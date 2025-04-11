from tkinter import *
from tkinter import ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import os
import socket
import threading
import re
import cv2
import face_recognition
import pickle
from tkinter import messagebox, filedialog, simpledialog


class ForenSyncDashboard:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Store the username for personalized greeting
        self.root.title("ForenSync - Investigator Dashboard")
        self.root.geometry("2560x1440")

        # Load and set the background image
        self.set_background_image(r"C:\Users\Savio\Documents\mini proj\bg.png")

        self.setup_styles()
        self.create_header()
        self.create_main_content() 

    def set_background_image(self, image_path):
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((2560, 1440), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(bg_image)
        bg_label = Label(self.root, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def setup_styles(self):
        # Custom colors
        self.bg_color = '#201E43'  # Dark blue
        self.button_color = '#91DDCF'  # Mint green
        self.text_color = '#201E43'  # Dark blue for text

        # Custom font
        self.header_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=12)

    def create_header(self):
        header_frame = Frame(self.root, bg="#201E43", padx=10, pady=20)
        header_frame.place(x=0, y=0, relwidth=1)

        img_path = r"C:\Users\Savio\Documents\mini proj\F_resized1.png"
        img = Image.open(img_path)
        img = img.resize((400, 120), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)

        img_label = Label(header_frame, image=photo, bg="#201E43")
        img_label.image = photo
        img_label.grid(row=0, column=0, padx=5)

        title_label = Label(header_frame, font=self.header_font, bg=self.bg_color, fg=self.button_color)
        title_label.grid(row=0, column=1, padx=50)

        # Logout Button using tk.Button
        logout_btn = Button(header_frame, text="Logout", bg=self.button_color, fg=self.text_color, font=self.button_font, command=self.logout)
        logout_btn.place(x=1050, y=30)

    def logout(self):
        self.root.destroy()  # Close the current Tkinter window
        os.system("python Main.py")

    def create_main_content(self):
        main_frame = Frame(self.root, bg=self.bg_color)
        main_frame.place(x=370, y=200, width=500, height=400)

        # Personalized welcome message for each investigator
        welcome_label = Label(main_frame, text=f"Welcome, Investigator 2", bg="#91DDCF", fg="#201E43", font=("Helvetica", 17), anchor="center")
        welcome_label.place(x=0, y=0, height=50, width=500)

        # Place buttons using tk.Button and configure colors
        btn1 = self.create_dashboard_button(main_frame, "🔍 Evidence\nManagement")
        btn1.place(x=45, y=80, width=200, height=60)

        btn2 = self.create_dashboard_button(main_frame, "👤 Offender Photo\nArchive")
        btn2.place(x=250, y=80, width=200, height=60)

        btn3 = self.create_dashboard_button(main_frame, "📁 Case\nManagement")
        btn3.place(x=45, y=160, width=200, height=60)

        btn4 = self.create_dashboard_button(main_frame, "📊 Statistics")
        btn4.place(x=250, y=160, width=200, height=60)

        btn5 = self.create_dashboard_button(main_frame, "💬 Chat", command=self.open_chat)
        btn5.place(x=45, y=240, width=200, height=60)

        btn6 = self.create_dashboard_button(main_frame, "📋 Automated\nReports")
        btn6.place(x=250, y=240, width=200, height=60)

        btn7 = self.create_dashboard_button(main_frame, "🗄️ Case Record\nArchive")
        btn7.place(x=45, y=320, width=200, height=60)

        btn8 = self.create_dashboard_button(main_frame, "📷 Facial Analysis")
        btn8.place(x=250, y=320, width=200, height=60)

    def create_dashboard_button(self, parent, text, command=None):
        return Button(parent, text=text, bg=self.button_color, fg=self.text_color, font=self.button_font, padx=20, pady=10, command=command)
    
    def open_chat(self):
        self.root.destroy()  # Close the current Tkinter window
        self.launch_chat_client()

    def launch_chat_client(self):
        chat_root = Tk()
        app = ForensicManagementClient(chat_root)
        chat_root.mainloop()

class ForensicManagementClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Investigator1")
        self.root.geometry("500x400")
        self.create_gradient_background()
        self.create_message_log()
        self.create_send_area()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.146.228', 12346))  
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def create_gradient_background(self):
        self.top_frame = Frame(self.root, bg="#003366")
        self.top_frame.place(relwidth=1, relheight=0.4, rely=0)

        self.bottom_frame = Frame(self.root, bg="#005588")
        self.bottom_frame.place(relwidth=1, relheight=0.6, rely=0.4)

    def create_message_log(self):
        self.log_frame = Frame(self.root, bg="#005588", padx=10, pady=10)
        self.log_frame.place(relwidth=0.9, relheight=0.6, relx=0.05, rely=0.05)

        Label(self.log_frame, text="INVESTIGATOR 1", font=("Arial", 16, "bold"), bg="#005588", fg="white").pack(pady=5)
        self.message_log = Text(self.log_frame, font=("Arial", 12), bg="white", fg="black", state='normal', wrap='word')
        self.message_log.pack(expand=True, fill=BOTH)
        self.message_log.configure(state="disabled")

    def create_send_area(self):
        send_frame = Frame(self.root, bg="#003366", padx=10, pady=10)
        send_frame.place(relwidth=0.9, relheight=0.15, relx=0.05, rely=0.75)

        self.message_entry = Entry(send_frame, width=35, font=("Arial", 12))
        self.message_entry.pack(side=LEFT, padx=5, fill=X, expand=True)

        Button(send_frame, text="Send", command=self.send_message, bg="#66ccff", fg="black", font=("Arial", 12, "bold")).pack(side=RIGHT, padx=5)

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                if msg:
                    cleaned_msg = self.clean_message(msg)
                    self.log_message(cleaned_msg, "left")
            except Exception:
                self.log_message("Error receiving message. Please check your connection.", "left")
                break

    def clean_message(self, msg):
        cleaned_msg = re.sub(r'Client \(\S+, \d+\): ', '', msg)  
        return cleaned_msg.strip() 

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.log_message(message, "right")
            self.message_entry.delete(0, END)

    def log_message(self, message, side):
        self.message_log.configure(state="normal")
        
        if side == "left":
            self.message_log.insert(END, f"{message}\n", "left_msg")
            self.message_log.tag_config("left_msg", justify='left', background="#e0e0e0")  # Light grey for received messages
        else: 
            self.message_log.insert(END, f"{message}\n", "right_msg")
            self.message_log.tag_config("right_msg", justify='right', background="#0084ff", foreground="white")  # Blue for sent messages

        self.message_log.configure(state="disabled")
        self.message_log.yview(END)
    def open_face(self):
        self.root.destroy()  # Close the current Tkinter window
        self.launch_face_client()

    def launch_face_client(self):
        face_root = Tk()
        app = FaceRecognitionApp(face_root)
        face_root.mainloop()
    
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

def main():
    root = Tk()
    app = ForenSyncDashboard(root, "Investigator")  # Pass a sample username for demonstration
    root.mainloop()

if __name__ == "__main__":
    main()
