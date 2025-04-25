import socketio
from tkinter import *
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db


def mainchat():
    # Initialize Firebase only if not already initialized
    try:
        firebase_admin.get_app()
    except ValueError:
        # Firebase not initialized, so initialize it
        cred = credentials.Certificate(r"C:\Users\Savio\Desktop\min proj\chatapp-336f3-firebase-adminsdk-fbsvc-875ce7130d.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://chatapp-336f3-default-rtdb.firebaseio.com/'
        })

    def login_and_get_username():
        login_window = Tk()
        login_window.withdraw()

        username = simpledialog.askstring("Login", "Enter Username:")
        password = simpledialog.askstring("Login", "Enter Password:", show="*")

        ref = db.reference("/users")

        if username == "Admin" and password == "Admin":
            new_username = simpledialog.askstring("Register", "Enter new Username:")
            new_password = simpledialog.askstring("Register", "Enter new Password:", show="*")
            if new_username and new_password:
                users = ref.get() or {}
                if new_username in users:
                    messagebox.showerror("Error", "Username already exists.")
                    return None
                ref.child(new_username).set({
                    "password": new_password,
                    "messages": {}
                })
                messagebox.showinfo("Success", f"User '{new_username}' registered.")
                return None
        else:
            users = ref.get()
            if users and username in users and users[username]["password"] == password:
                return username, username  # user_id = username for Firebase
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")
                return None

    # --- MAIN CHAT CLASS ---
    class Investigator2ChatClient:
        def __init__(self, root, username, user_id):
            self.root = root
            self.username = username
            self.user_id = user_id
            self.root.title(f"Forensic Chat - {self.username}")
            self.root.geometry("800x600")
            self.root.configure(bg="#1e1e2f")

            self.current_chat = None
            self.contacts = self.load_contacts()
            self.message_history = {}

            self.client_socket = socketio.Client()
            self.client_socket.on('connect', self.on_connect)
            self.client_socket.on('private_message', self.on_private_message)
            self.client_socket.on('disconnect', self.on_disconnect)

            self.setup_ui()
            self.connect_to_server()

        def load_contacts(self):
            users = db.reference("/users").get()
            if users:
                return [user for user in users if user != self.username]
            return []

        def save_message_to_db(self, receiver_username, message):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message_data = {
                "sender": self.username,
                "receiver": receiver_username,
                "message": message,
                "timestamp": timestamp
            }
            sender_ref = db.reference(f"/users/{self.username}/messages/{receiver_username}")
            receiver_ref = db.reference(f"/users/{receiver_username}/messages/{self.username}")
            sender_ref.push(message_data)
            receiver_ref.push(message_data)

        def load_chat_history_from_db(self, contact_username):
            ref = db.reference(f"/users/{self.username}/messages/{contact_username}")
            messages = ref.get() or {}
            # Convert messages to list and ensure they have the correct format
            formatted_messages = []
            for msg_id, msg_data in messages.items():
                if isinstance(msg_data, dict):
                    # Ensure all required fields exist
                    formatted_msg = {
                        'sender': msg_data.get('sender', 'Unknown'),
                        'message': msg_data.get('message', ''),
                        'timestamp': msg_data.get('timestamp', '')
                    }
                    formatted_messages.append(formatted_msg)
            return sorted(formatted_messages, key=lambda x: x.get('timestamp', ''))

        def setup_ui(self):
            header = Frame(self.root, bg="#151d33")
            header.pack(fill=X)
            Label(header, text=f"Forensic Chat - {self.username}", font=("Segoe UI", 16, "bold"), fg="white", bg="#151d33", padx=10).pack(side=LEFT)

            contacts_frame = Frame(self.root, bg="#1e1e2f", width=200)
            contacts_frame.pack(side=LEFT, fill=Y, padx=5, pady=5)
            Label(contacts_frame, text="Contacts", font=("Segoe UI", 12, "bold"), fg="white", bg="#1e1e2f").pack(pady=10)

            self.contacts_listbox = Listbox(contacts_frame, bg="#2b2b3d", fg="white", selectbackground="#4CAF50", font=("Segoe UI", 11), height=20, width=20)
            self.contacts_listbox.pack(fill=BOTH, expand=True, padx=5, pady=5)

            for contact in self.contacts:
                self.contacts_listbox.insert(END, contact)

            self.contacts_listbox.bind("<<ListboxSelect>>", self.select_contact)

            chat_container = Frame(self.root, bg="#1e1e2f")
            chat_container.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

            self.chat_header = Frame(chat_container, bg="#151d33")
            self.chat_header.pack(fill=X)
            self.current_chat_label = Label(self.chat_header, text="Select a contact", font=("Segoe UI", 12, "bold"), fg="white", bg="#151d33")
            self.current_chat_label.pack(pady=5)

            self.chat_frame = Frame(chat_container, bg="#1e1e2f")
            self.chat_frame.pack(fill=BOTH, expand=True)

            self.canvas = Canvas(self.chat_frame, bg="#1e1e2f", highlightthickness=0)
            self.scrollbar = Scrollbar(self.chat_frame, orient=VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=RIGHT, fill=Y)
            self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

            self.scrollable_frame = Frame(self.canvas, bg="#1e1e2f")
            self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

            def configure_scrollable_frame(event):
                self.canvas.itemconfig(self.canvas_window, width=event.width)
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            self.canvas.bind("<Configure>", configure_scrollable_frame)
            self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

            input_frame = Frame(chat_container, bg="#151d33")
            input_frame.pack(fill=X, pady=5)

            self.message_entry = Entry(input_frame, font=("Segoe UI", 12), bg="#2b2b3d", fg="white", relief=FLAT, insertbackground="white")
            self.message_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 10), ipady=8)
            self.message_entry.bind("<Return>", lambda e: self.send_private_message())

            self.send_button = Button(input_frame, text="Send", command=self.send_private_message, bg="#4CAF50", fg="white", font=("Segoe UI", 12, "bold"), padx=20, pady=6, relief=FLAT)
            self.send_button.pack(side=RIGHT)
            self.send_button.config(state=DISABLED)

        def connect_to_server(self):
            try:
                # Connect to Socket.IO server
                self.client_socket.connect("https://582cb979-13fd-4725-bb1a-f4fab6e0869a-00-33wpufgnnjrg4.pike.replit.dev:8080/")
                self.client_socket.emit('register', {'username': self.username})
                print(f"{self.username} connected to server.")
            except Exception as e:
                print(f"Connection error: {e}")
                messagebox.showerror("Connection Error", "Could not connect to chat server. Please try again later.")

        def on_connect(self):
            print("Connected to server")

        def on_private_message(self, data):
            try:
                sender = data.get('sender')
                message = data.get('message')

                if sender not in self.message_history:
                    self.message_history[sender] = []
                self.message_history[sender].append((sender, message))

                if self.current_chat == sender:
                    self.display_message(sender, message)
            except Exception as e:
                print(f"Error handling message: {e}")

        def on_disconnect(self):
            print("Disconnected from server")

        def select_contact(self, event):
            selection = self.contacts_listbox.curselection()
            if selection:
                self.current_chat = self.contacts_listbox.get(selection[0])
                self.current_chat_label.config(text=f"Chat with {self.current_chat}")
                self.send_button.config(state=NORMAL)
                self.load_chat_history()

        def load_chat_history(self):
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            if self.current_chat:
                messages = self.load_chat_history_from_db(self.current_chat)
                for msg in messages:
                    try:
                        sender = msg.get('sender', 'Unknown')
                        message_text = msg.get('message', '')
                        if message_text:  # Only display non-empty messages
                            self.display_message(sender, message_text)
                    except Exception as e:
                        print(f"Error displaying message: {e}")

        def send_private_message(self):
            message = self.message_entry.get().strip()
            if message and self.current_chat:
                try:
                    # Save message to database
                    self.save_message_to_db(self.current_chat, message)
                    
                    # Send message through Socket.IO
                    self.client_socket.emit('private_message', {
                        'recipient': self.current_chat,
                        'message': message,
                        'sender': self.username
                    })
                    
                    # Display message in UI
                    self.display_message(self.username, message)
                    self.message_entry.delete(0, END)
                except Exception as e:
                    print(f"Error sending message: {e}")
                    messagebox.showerror("Error", "Could not send message. Please try again.")

        def display_message(self, sender, message):
            try:
                if not message:  # Skip empty messages
                    return

                is_own_message = (sender == self.username)

                outer_frame = Frame(self.scrollable_frame, bg="#1e1e2f")
                outer_frame.pack(fill=X, pady=5)

                inner_frame = Frame(outer_frame, bg="#1e1e2f")
                inner_frame.pack(anchor=E if is_own_message else W, padx=10, fill=X)

                bg_color = "#4CAF50" if is_own_message else "#5DADE2"
                if not is_own_message:
                    Label(inner_frame, text=sender, font=("Segoe UI", 9, "bold"), 
                          bg="#1e1e2f", fg="#5DADE2").pack(anchor=W)

                message_label = Label(inner_frame, text=message, font=("Segoe UI", 11), 
                                    wraplength=400, justify=LEFT, bg=bg_color, 
                                    fg="white", padx=12, pady=8, bd=0)
                message_label.pack(anchor=E if is_own_message else W)

                self.canvas.yview_moveto(1.0)
            except Exception as e:
                print(f"Error displaying message: {e}")

    # --- APP ENTRY POINT ---
    login_result = login_and_get_username()
    if login_result:
        username, user_id = login_result
        root = Tk()
        app = Investigator2ChatClient(root, username, user_id)
        root.mainloop()

if __name__ == "__main__":
    mainchat()