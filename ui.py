import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 
import tkinter
import os
import facerecognition

class ui:
    def open(self):

        face_recognition = facerecognition.FaceRecognition()

        face_recognition.setup_wincam()
        face_recognition.setup_wincam()

        root = tkinter.Tk()
        root.title("Pokedex")
        root.minsize(480, 800)
        root.maxsize(480, 800)

        camera_image = Label(root)
        camera_image.pack()

        button = Button(root, text="Save")
        button.config(command=lambda: face_recognition.save_current_face(root))
        button.pack()

        def update_image():
            frame = face_recognition.get_camera_frame()
            scanned_frame = face_recognition.scan_faces_in_frame(frame)
            camera_image.photo_image = scanned_frame
            camera_image.config(image=camera_image.photo_image)

            root.after(10, update_image)  # Update every 100 milliseconds

        update_image()
        
        root.mainloop()
    