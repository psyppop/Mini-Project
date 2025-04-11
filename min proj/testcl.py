import socketio
from tkinter import *



def mainchat():

    class ForensicManagementClient:
        def __init__(self, root):
            self.root = root
            self.root.title("FACILITY")
            self.root.geometry("2560x1440")
            self.create_gradient_background()
            self.create_message_log()
            self.create_send_area()

            # Initialize last sent message to prevent AttributeError
            self.last_sent_message = None  

            # Socket.IO connection
            self.client_socket = socketio.Client()
            self.client_socket.on('connect', self.on_connect)
            self.client_socket.on('message', self.on_message)
            self.client_socket.on('disconnect', self.on_disconnect)

            self.connect_to_server()

        def connect_to_server(self):
            try:
                self.client_socket.connect("https://c85df12a-baaf-4718-af91-2d071411816b-00-shyv3lyu55i4.pike.replit.dev")
                self.log_message("Connected to server.", "left")
            except Exception as e:
                self.log_message(f"Connection error: {e}", "left")

        def on_connect(self):
            self.log_message("Successfully connected to server!", "left")

        def on_message(self, msg):
            """ Only log received messages (avoiding duplication). """
            if msg != self.last_sent_message:
                self.log_message(msg, "left")

        def on_disconnect(self):
            self.log_message("Disconnected from server.", "left")

        def create_gradient_background(self):
            self.top_frame = Frame(self.root, bg="#003366")
            self.top_frame.place(relwidth=1, relheight=0.4, rely=0)

            self.bottom_frame = Frame(self.root, bg="#005588")
            self.bottom_frame.place(relwidth=1, relheight=0.6, rely=0.4)

        def create_message_log(self):
            self.log_frame = Frame(self.root, bg="#005588", padx=10, pady=10)
            self.log_frame.place(relwidth=0.9, relheight=0.6, relx=0.05, rely=0.05)

            Label(self.log_frame, text="INVESTIGATOR 2", font=("Arial", 16, "bold"), bg="#005588", fg="white").pack(pady=5)
            self.message_log = Text(self.log_frame, font=("Arial", 12), bg="white", fg="black", state='normal', wrap='word')
            self.message_log.pack(expand=True, fill=BOTH)
            self.message_log.configure(state="disabled")

        def create_send_area(self):
            send_frame = Frame(self.root, bg="#003366", padx=10, pady=10)
            send_frame.place(relwidth=0.9, relheight=0.15, relx=0.05, rely=0.75)
            self.message_entry = Entry(send_frame, width=35, font=("Arial", 12))
            self.message_entry.pack(side=LEFT, padx=5, fill=X, expand=True)

            Button(send_frame, text="Send", command=self.send_message, bg="#66ccff", fg="black", font=("Arial", 12, "bold")).pack(side=RIGHT, padx=5)

        def send_message(self):
            message = self.message_entry.get()
            if message:
                self.last_sent_message = message  # Store the last sent message
                self.client_socket.send(message)  # Send message to server
                self.log_message(message, "right")  # Log the sent message
                self.message_entry.delete(0, END)  # Clear the entry field

        def log_message(self, message, side):
            self.message_log.configure(state="normal")

            if side == "left":
                self.message_log.insert(END, f"{message}\n", "left_msg")
                self.message_log.tag_config("left_msg", justify='left', background="#e0e0e0")
            else:  
                self.message_log.insert(END, f"{message}\n", "right_msg")
                self.message_log.tag_config("right_msg", justify='right', background="#0084ff", foreground="white")

            self.message_log.configure(state="disabled")
            self.message_log.yview(END)

    # Create the Tkinter window and run the application
    root = Tk()
    app = ForensicManagementClient(root)
    root.mainloop()

if __name__ == "__main__":
    mainchat()
