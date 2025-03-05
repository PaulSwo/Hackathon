from time import sleep
from tkinter import *
import tkinter
import os
import facerecognition
import threading
from PIL import Image, ImageDraw, ImageFont, ImageTk


"""
save_current_face
scan_faces_in_frame
add_face

get_all_faces

"""

class Pokedex:

    isFace = False
    display = None

    def check_face(self, root, face_recognition):
        while True:

            face = face_recognition.get_camera_frame()



            if hasattr(self, 'bild_label'):
                self.bild_label.config(image=face)
                self.bild_label.image = face
            else:
                self.bild_label = Label(root, image=face)
                self.bild_label.image = face
                self.bild_label.pack()


            face_infos = face_recognition.scan_faces_in_frame(face)
            face_info = face_infos[0]

            if(face_info == "No Face"):
                pass
            elif(face_info == "Unknown"):
                self.clear_screen(root)
                self.isFace = True
                self.scan_success(root, face_infos[1])
                return
            elif(face_info != "N"):
                self.clear_screen(root)
                self.isFace = True
                self.scan_found(root, face_info, face_recognition)
                return


            print(f"Name: {face_info}")
            sleep(0.05)

    def set_status(self):
        while not self.isFace:
            wait = 0.5
            for i in range(3):
                self.display.configure(text="Scanning" + (i+1)*".")
                sleep(wait)
        

    def open(self):
        face_recognition = facerecognition.FaceRecognition()

        face_recognition.setup_wincam()

        root = tkinter.Tk()
        root.title("Humandex")
        root.minsize(480, 700)
        root.maxsize(480, 700)

        
        self.display = Label(root, text="Scanning", font=("Arial", 30, "bold")) # we need this Label as a variable!
        self.display.place(x=240, y=600, anchor="center")


        t1 = threading.Thread(target=self.check_face, args=(root, face_recognition))
        t1.start()
        
        
        t2 = threading.Thread(target=self.set_status)
        t2.start()

        root.mainloop()


    
    def scan_success(self, root, image):

        # Create image label
        img = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image = img)
        label = Label(root, image=photo)
        label.image = photo  # Keep reference!
        label.pack()

        # Create text entry field
        name_input = Entry(root)
        name_input.pack()

        # Create button
        button_add = Button(root, text="Hinzufügen", command=lambda: self.add_face(name_input.get(), photo, root))
        button_add.pack()
        button_cancel = Button(root, text="Abbrechen")
        button_cancel.pack()


    def scan_found(self, root, image_name, face_recognition):

        # Create image label
        img = Image.open(f"faces\\{image_name}.png")
        photo = ImageTk.PhotoImage(image = img)
        label = Label(root, image=photo)
        label.image = photo  # Keep reference!
        label.pack()

        label = Label(root, text=f"Hallo {image_name}")
        label.pack()


        sleep(2)

        self.clear_screen(root)



    def add_face(self, name, image, root):
        print(name)
        if(len(name) > 0):
            img_path = os.path.join('faces', f"{name}.png")
            image._PhotoImage__photo.write(img_path)
            self.clear_screen(root)



    def clear_screen(self, root):
        for widget in root.winfo_children():
            widget.destroy()


pokedex = Pokedex()
pokedex.open()