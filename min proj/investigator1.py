import socket
import threading
import re
from tkinter import *

def mainchat(self):
    def create_gradient_background(root):
        top_frame = Frame(root, bg="#003366")
        top_frame.place(relwidth=1, relheight=0.4, rely=0)

        bottom_frame = Frame(root, bg="#005588")
        bottom_frame.place(relwidth=1, relheight=0.6, rely=0.4)

    def create_message_log(root):
        log_frame = Frame(root, bg="#005588", padx=10, pady=10)
        log_frame.place(relwidth=0.9, relheight=0.6, relx=0.05, rely=0.05)

        Label(log_frame, text="INVESTIGATOR 1", font=("Arial", 16, "bold"), bg="#005588", fg="white").pack(pady=5)
        message_log = Text(log_frame, font=("Arial", 12), bg="white", fg="black", state='normal', wrap='word')
        message_log.pack(expand=True, fill=BOTH)
        message_log.configure(state="disabled")
        return message_log

    def create_send_area(root, send_message):
        send_frame = Frame(root, bg="#003366", padx=10, pady=10)
        send_frame.place(relwidth=0.9, relheight=0.15, relx=0.05, rely=0.75)

        message_entry = Entry(send_frame, width=35, font=("Arial", 12))
        message_entry.pack(side=LEFT, padx=5, fill=X, expand=True)

        Button(send_frame, text="Send", command=send_message, bg="#66ccff", fg="black", font=("Arial", 12, "bold")).pack(side=RIGHT, padx=5)
        return message_entry

    def receive_messages(client_socket, message_log):
        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if msg:
                    cleaned_msg = clean_message(msg)
                    log_message(message_log, cleaned_msg, "left")
            except Exception:
                log_message(message_log, "Error receiving message. Please check your connection.", "left")
                break

    def clean_message(msg):
        cleaned_msg = re.sub(r'Client \(\S+, \d+\): ', '', msg)
        return cleaned_msg.strip()

    def send_message():
        message = message_entry.get()
        if message:
            client_socket.send(message.encode('utf-8'))
            log_message(message_log, message, "right")
            message_entry.delete(0, END)

    def log_message(message_log, message, side):
        message_log.configure(state="normal")
        if side == "left":
            message_log.insert(END, f"{message}\n", "left_msg")
            message_log.tag_config("left_msg", justify='left', background="#e0e0e0")  # Light grey for received messages
        else:
            message_log.insert(END, f"{message}\n", "right_msg")
            message_log.tag_config("right_msg", justify='right', background="#0084ff", foreground="white")  # Blue for sent messages

        message_log.configure(state="disabled")
        message_log.yview(END)

    # Start of the application
    root = Tk()
    root.title("FACILITATOR")
    root.geometry("500x400")

    # Create gradient background
    create_gradient_background(root)

    # Create message log and send area
    message_log = create_message_log(root)
    message_entry = create_send_area(root, send_message)

    # Set up client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('192.168.1.38', 12346))

    # Start receiving messages in a separate thread
    threading.Thread(target=receive_messages, args=(client_socket, message_log), daemon=True).start()

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    mainchat(self)
