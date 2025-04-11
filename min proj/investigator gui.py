import cv2
import numpy as np
import tkinter as tk
from tkinter import Frame, Label, LEFT
from PIL import Image, ImageTk

class InvestigatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Investigator")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.toggle_fullscreen)

        self.background_image = Image.open(r"C:\Users\Savio\Documents\mini proj\bg.png")
        self.background_image = self.background_image.resize((2560, 1440), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(self.background_image)

        self.bg_label = Label(root, image=self.bg_image)
        self.bg_label.place(relwidth=1, relheight=1)

        header_frame = Frame(root, bg="#201E43", padx=10, pady=20)
        header_frame.pack(fill=tk.X)

        self.header_image = Image.open(r"C:\Users\Savio\Documents\mini proj\F_resized1.png")
        self.header_image = self.header_image.resize((400, 120), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.header_image)
        img_label = Label(header_frame, image=self.photo, bg="#201E43")
        img_label.pack(side=LEFT, padx=5)

    def toggle_fullscreen(self, event=None):
        current_state = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current_state)

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestigatorApp(root)
    root.mainloop()
