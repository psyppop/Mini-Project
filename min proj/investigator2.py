import socket
import threading
import re
from tkinter import *

class ForensicManagementClient:
    def __init__(self, root):
        self.root = root
        self.root.title("FACILITY")
        self.root.geometry("500x400")

        
        self.create_gradient_background()
        self.create_message_log()
        self.create_send_area()
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('192.168.1.41', 12346)) 
        threading.Thread(target=self.receive_messages, daemon=True).start()

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
            self.message_log.tag_config("left_msg", justify='left', background="#e0e0e0")
        else:  
            self.message_log.insert(END, f"{message}\n", "right_msg")
            self.message_log.tag_config("right_msg", justify='right', background="#0084ff", foreground="white")  # Blue for sent messages

        self.message_log.configure(state="disabled")
        self.message_log.yview(END)

def main():
    root = Tk()
    app = ForensicManagementClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
