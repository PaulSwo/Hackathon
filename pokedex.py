from tkinter import *
import tkinter
import os
import facerecognition

class ui:
    def open(self):

        face_recognition = facerecognition.FaceRecognition()

        face_recognition.setup_wincam()

        root = tkinter.Tk()
        root.title("Pokedex")
        root.minsize(480, 800)
        root.maxsize(480, 800)




        
        root.mainloop()


pokedex = ui()
pokedex.open()