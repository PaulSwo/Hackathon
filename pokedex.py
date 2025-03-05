from tkinter import *
import tkinter
import os
import facerecognition
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

class Pokedex:
    def open(self):

        face_recognition = facerecognition.FaceRecognition()

        face_recognition.setup_wincam()

        root = tkinter.Tk()
        root.title("Pokedex")
        root.minsize(480, 800)
        root.maxsize(480, 800)
        text = Label(root, text="WoW! So ein toller Tag!")
        text.pack()

        file = Image.open("faces/sportlehrer.jpg")
        img = ImageTk.PhotoImage(file)

        image = Label(root)
        image.photo_image = img
        image.config(image=img)
        image.pack()

        button = Button(root, text="Gesicht speichern", command=lambda: face_recognition.save_current_face(root))
        button.pack()


        def update_image():
            frame = face_recognition.get_camera_frame()
            img = face_recognition.scan_faces_in_frame(frame)
            image.photo_image = img
            image.config(image=image.photo_image)

            root.after(10, update_image)  # Führe alle 10ms aus

        update_image()
        root.mainloop()
        return

        # Funktion, um den eingegebenen Text auszugeben 
        def get_text():
            text = entry.get ()
            print("Eingegebener Text:", text)
            
        # Hauptfenster erstellen
        root = tk.Tk()
        root.title("Tkinter UI mit Hintergrundbild")
        root.geometry("400x300") # Fenstergröße
    
        # Canvas für das Hintergrundbild
        canvas = tk.Canvas(root, width=400, height=300)
        canvas.pack(fill="both", expand=True)
    
        # Hintergrundbild laden
        #bg_image = PhotoImage(file="faces/sportlehrer.jpg")
        #canvas.create_image(0, 0, image=bg_image, anchor="nw")

        # Textfeld erstellen 
        entry = tk.Entry(root)
        entry_window = canvas.create_window(200, 120, window=entry, width=200)

        # Button erstellen
        button = tk.Button(root, text="Absenden", command=get_text, font=("Arial", 12))
        button_window = canvas.create_window(200, 160, window=button, width=100)

        # Tkinter-Hauptloop starten
        root.mainloop()








        
        


pokedex = Pokedex()
pokedex.open()

