from tkinter import *
import tkinter
import os
import facerecognition
from PIL import Image, ImageTk

class Pokedex:
    def open(self):

        face_recognition = facerecognition.FaceRecognition()

        face_recognition.setup_wincam()

        root = tkinter.Tk()
        root.title("Pokedex")
        root.minsize(480, 800)
        root.maxsize(480, 800)


        #img = face_recognition.get_camera_frame()

        #frame = face_recognition.get_camera_frame()
        #img = face_recognition.scan_faces_in_frame(frame)
        
        #image = Label(root)
        #image.photo_image = img
        #image.config(image=img)
        #image.pack()

        image = Label(root)
        image.pack()

        def update_image():
            frame = face_recognition.get_camera_frame()
            img = face_recognition.scan_faces_in_frame(frame)
            image.photo_image = img
            image.config(image=image.photo_image)

            root.after(10, update_image) 
        
        update_image()

        button = Button(root, text="Gesicht speichern", command=lambda: face_recognition.save_current_face(root))
        button.pack()
        

        
        

        
        root.mainloop()


pokedex = Pokedex()
pokedex.open()