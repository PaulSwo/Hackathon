import face_recognition
import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 
import os

class UI:

    def __init__(self, fr):
        self.root = Tk()
        self.root.bind('<Escape>', lambda e: destroy()) 
        self.root.title("Humandex")
        self.root.minsize(1200, 700)
        self.root.maxsize(1200, 700)

        self.image_label = Label(self.root)
        self.image_label.config(width=800, height=450)
        self.image_label.pack()
        self.fr = fr


    def showUI(self):
        while True:
            img = self.fr.get_frame()

            self.image_label.photo_image = img
            self.image_label.config(image=img)
            self.root.update()
    def destroy(self):
        fr.release()
        root.quit()