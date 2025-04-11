import socket
import threading
from tkinter import *
from tkinter import scrolledtext

class ForensicManagementServer:
    def __init__(self, root):
        self.root = root
        self.root.title("ForenSync Server")
        self.root.geometry("400x300")

        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 12346))
        self.server_socket.listen(5)

        self.create_client_log()
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def create_client_log(self):
        self.log_frame = Frame(self.root, padx=10, pady=10)
        self.log_frame.pack(expand=True, fill=BOTH)

        Label(self.log_frame, text="Client Log", font=("Arial", 16)).pack(pady=5)
        self.client_log = scrolledtext.ScrolledText(self.log_frame, font=("Arial", 12), state='normal')
        self.client_log.pack(expand=True, fill=BOTH)

    def accept_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.clients.append(client_socket)
            self.log_message(f"Client {addr} connected.")
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()

    def handle_client(self, client_socket, addr):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    self.log_message(f"Client {addr}: {message}")
                    self.broadcast_message(f"Client {addr}: {message}", client_socket)
                else:
                    self.remove_client(client_socket, addr)
                    break
            except Exception as e:
                self.log_message(f"Error handling client {addr}: {e}")
                self.remove_client(client_socket, addr)
                break

    def broadcast_message(self, message, exclude_socket):
        for client in self.clients:
            if client != exclude_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(client, None)

    def remove_client(self, client_socket, addr):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            if addr:
                self.log_message(f"Client {addr} disconnected.")
            client_socket.close()

    def log_message(self, message):
        self.client_log.insert(END, message + '\n')
        self.client_log.yview(END)
def main():
    root = Tk()
    app = ForensicManagementServer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
