from time import sleep
from tkinter import *
import tkinter
import os
import facerecognition
import threading


"""
save_current_face
scan_faces_in_frame
add_face

get_all_faces

"""

class Pokedex:

    isFace = False
    display = None

    def check_face(self, root, face_recognition, canvas):
        while True:
            face = face_recognition.get_camera_frame()
            canvas.create_image(0, 65, anchor=NW, image=face)

            face_info = face_recognition.scan_faces_in_frame(face)

            if(face_info == "No Face"):
                pass
            elif(face_info == "Unknown"):
                face_recognition.save_current_face(root)
                #canvas.destroy()
                self.isFace = True
                #self.scan_success(canvas, face_recognition)
                return

            print(face_info)
            sleep(0.05)

    def set_status(self):
        while not self.isFace:
            wait = 0.5
            for i in range(3):
                self.display.configure(text="Scanning" + (i+1)*".")
                sleep(wait)
        
        self.display.destroy()


    def open(self):
        face_recognition = facerecognition.FaceRecognition()

        face_recognition.setup_wincam()

        root = tkinter.Tk()
        root.title("Humandex")
        root.minsize(480, 700)
        root.maxsize(480, 700)

        canvas = Canvas(root, width=480, height=700)
        canvas.pack()
        
        self.display = Label(root, text="Scann", font=("Arial", 30, "bold")) # we need this Label as a variable!
        self.display.place(x=240, y=600, anchor="center")

        self.display.configure(text="Scanning...")

        #Button(frame, text="10p", command=lambda: add(.1)).grid(row=3, column=1)


        #self.create_rounded_rect(canvas, 50, 50, 300, 300, radius=50, border=20, color="red")

        #Button(root, text="Confirm", command=face_recognition.confirmNewFaceInput).pack(side=LEFT, padx=10, pady=10)
        #Button(root, text="Cancel", command=face_recognition.closeNewFaceInput).pack(side=RIGHT, padx=10, pady=10)

        t1 = threading.Thread(target=self.check_face, args=(root, face_recognition, canvas))
        t1.start()
        
        
        t2 = threading.Thread(target=self.set_status)
        t2.start()

        root.mainloop()


    
    def scan_success(self, canvas, face_recognition):
        Label(canvas, text="Enter name:").pack(pady=20)
        face_recognition.name_entry = Entry(canvas)
        
        face_recognition.name_entry.pack(pady=10)
        face_recognition.name_entry.focus()

        face_recognition.popup_image_label = Label(canvas)
        face_recognition.popup_image_label.pack(pady=10)
        face_recognition.popup_image_label.config(width=300, height=300)  
        face_recognition.popup_image_label.photo_image = face_recognition.get_camera_frame()
        face_recognition.popup_image_label.config(image=face_recognition.get_camera_frame())

        Button(canvas, text="Confirm", command=face_recognition.confirmNewFaceInput).pack(side=LEFT, padx=10, pady=10)
        Button(canvas, text="Cancel", command=face_recognition.closeNewFaceInput).pack(side=RIGHT, padx=10, pady=10)

pokedex = Pokedex()
pokedex.open()