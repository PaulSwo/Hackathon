import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 
import os

class UI:

    def __init__(self):
        self.root = Tk()
        self.root.bind('<Escape>', lambda e: self.destroy()) 
        self.root.title("Humandex")
        self.root.minsize(480, 800)
        self.root.maxsize(480, 800)

        self.image_label = Label(self.root)
        self.image_label.pack()

        self.small_component_frame = Frame(self.root)
        self.small_component_frame.lift(self.image_label)
        self.small_component_frame.config(width=480, height=200)
        self.small_component_frame.pack(pady=10)

        self.small_component_info = Frame(self.small_component_frame)
        self.small_component_info.config(width=480, height=70)
        self.small_component_info.pack(pady=10)

        self.text_label = Label(self.small_component_info, text="A new face has been detected!")
        self.text_label.pack(side=LEFT, padx=5)

        self.toggle_button = Button(self.small_component_info, text="Add face", command=self.openAppFaceUI)
        self.toggle_button.config(width=50, height=3)
        self.toggle_button.pack(side=LEFT, padx=5)

        self.new_face_img = Label(self.small_component_frame)
        self.new_face_img.pack()

        self.listButton = Button(self.root, text="View humans", command=self.openListView)
        self.listButton.pack(side=RIGHT, padx=5)

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
        self.name_entry.bind("<Button-1>", lambda e:self.open_touch_keyboard())
        
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
            self.popup_image_label.photo_image._PhotoImage__photo.write(img_path)

            self.addFaceCallback(name, img_path)

            self.popup.destroy()


    def openListView(self):
        self.listViewPopup = Toplevel(self.root)
        self.listViewPopup.title("List of Known Faces")

        frame = Frame(self.listViewPopup)
        frame.pack()

        # Load images from the 'faces' directory
        faces_dir = 'faces'
        images = [f for f in os.listdir(faces_dir) if os.path.isfile(os.path.join(faces_dir, f))]

        # Place images in a grid layout
        for index, image_file in enumerate(images):
            img_path = os.path.join(faces_dir, image_file)
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.ANTIALIAS)  # Resize image to fit in the grid
            photo = ImageTk.PhotoImage(img)

            label = Label(frame, image=photo)
            label.image = photo  
            label.grid(row=(index // 4) * 2, column=index % 4, padx=10, pady=10)

            name = Label(frame, text=image_file.split(".")[0])
            name.grid(row=(index // 4) * 2 + 1, column=index % 4, padx=10, pady=10)

    def open_touch_keyboard(event):
        os.system("matchbox-keyboard")