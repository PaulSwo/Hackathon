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

        face_recognition.setup_picam()

        root = tkinter.Tk()
        root.title("Pokedex")
        root.minsize(480, 800)
        root.maxsize(480, 800)

        camera_image = Label(root)
        camera_image.pack()

        button = Button(root, text="Save")
        button.config(command=lambda: face_recognition.save_current_face(root))
        button.pack()

        showButton = Button(root, text="Show")
        showButton.config(command=lambda: self.show_all_faces(root, face_recognition))
        showButton.pack()

        def update_image():
            frame = face_recognition.get_camera_frame()
            scanned_frame = face_recognition.scan_faces_in_frame(frame)
            camera_image.photo_image = scanned_frame
            camera_image.config(image=camera_image.photo_image)

            root.after(10, update_image)  # Update every 100 milliseconds

        update_image()
        
        root.mainloop()

    def show_all_faces(self, root, face_recognition):
        images = face_recognition.get_all_faces()

        self.listViewPopup = Toplevel(root)
        self.listViewPopup.title("List of Known Faces")

        frame = Frame(self.listViewPopup)
        frame.pack()

        for index, image_file in enumerate(images):
            img_path = os.path.join("faces", image_file)
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)

            label = Label(frame, image=photo)
            label.image = photo
            label.grid(row=(index // 4) * 2, column=index % 4, padx=10, pady=10)

            name = Label(frame, text=image_file.split(".")[0])
            name.grid(row=(index // 4) * 2 + 1, column=index % 4, padx=10, pady=10)