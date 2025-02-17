import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 
import os

class UI:

    def __init__(self):
        self.root = Tk()
        self.root.bind('<Escape>', lambda e: destroy()) 
        self.root.title("Humandex")
        self.root.minsize(1200, 700)
        self.root.maxsize(1200, 700)

        self.image_label = Label(self.root)
        self.image_label.config(width=640, height=480)
        self.image_label.pack()

        # Create a frame for the small component
        self.small_component_frame = Frame(self.root)
        self.small_component_frame.pack(pady=10)

        # Add a text label to the small component
        self.text_label = Label(self.small_component_frame, text="A new face has been detected!")
        self.text_label.pack(side=LEFT, padx=5)

        # Add a button to the small component
        self.toggle_button = Button(self.small_component_frame, text="Add face", command=self.openAppFaceUI)
        self.toggle_button.pack(side=LEFT, padx=5)

        self.new_face_img = Label(self.small_component_frame)
        self.new_face_img.pack(side=LEFT, padx=5)

        self.small_component_frame.pack_forget()


    #sets current image from webcam
    def setImage(self, img):
        self.image_label.photo_image = img
        self.image_label.config(image=img)
        self.root.update()

    #shows component to ask if user wants to add unknown face
    def showAddFaceButton(self, img):
        self.small_component_frame.pack(pady=10)

        self.new_face_img.photo_image = img
        self.new_face_img.config(image=img)
        self.small_component_frame.update()

    #hides component above
    def hideAddFaceButton(self):
        self.small_component_frame.pack_forget()

    #opens a new window to ask for the name of the new face
    def openAppFaceUI(self):
        self.popup = Toplevel(self.root)
        self.popup.title("Add New Face")

        Label(self.popup, text="Enter name:").pack(pady=10)
        self.name_entry = Entry(self.popup)
        self.name_entry.pack(pady=10)

        self.popup_image_label = Label(self.popup)
        self.popup_image_label.pack(pady=10)
        self.popup_image_label.photo_image = self.new_face_img.photo_image
        self.popup_image_label.config(image=self.new_face_img.photo_image)

        Button(self.popup, text="Confirm", command=self.confirmNewFaceInput).pack(side=LEFT, padx=10, pady=10)
        Button(self.popup, text="Cancel", command=self.popup.destroy).pack(side=RIGHT, padx=10, pady=10)


    def confirmNewFaceInput(self):
        name = self.name_entry.get()
        if name:
            if not os.path.exists('faces'):
                os.makedirs('faces')
            img_path = os.path.join('faces', f"{name}.png")
            self.new_face_img.photo_image._PhotoImage__photo.write(img_path)

            self.addFaceCallback(name, img_path)

            self.popup.destroy()


    def destroy(self):
        root.quit()