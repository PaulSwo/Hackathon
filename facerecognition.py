import face_recognition
import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 
import os
from subprocess import Popen
#from picamera2 import Picamera2

class FaceRecognition:

    faces_folder = "faces"

    known_face_encodings = []
    known_face_names = []

    def __init__(self):

        for filename in os.listdir(self.faces_folder):
            self.add_face(filename.split(".")[0], os.path.join(self.faces_folder, filename))

        face_recognition.cpus = -1

    def setup_picam(self):
        self.is_on_pi = True
        self.camera = Picamera2()
        self.camera.start(show_preview=False)

    def setup_wincam(self):
        self.is_on_pi = False
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            print("Camera could not be opened")
            exit()


    def add_face(self, name, image_path):
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]

        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(name)

    def addFaceCallback(self, name, img_path):
        self.add_face(name, img_path)
        

    def get_camera_frame(self):
        # Grab a single frame of video
        if self.is_on_pi:
            frame = self.camera.capture_array()
        else:
            ret, frame = self.camera.read()
        # change this based on camera position
        frame = cv2.flip(frame, 1)

        if not self.is_on_pi:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        photo_img = self.convertImage(frame)

        return photo_img
    
    def scan_faces_in_frame(self, frame):
        frame = self.photoimage_to_array(frame)
        face_locations = []
        face_encodings = []
        face_names = []
        
        frame_size = 0.25

        #contains face encodings that are not known to make them addable
        unknown_face_encodings = []

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=frame_size, fy=frame_size)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        code = cv2.COLOR_BGR2RGB
        rgb_small_frame = cv2.cvtColor(rgb_small_frame, code)
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = ""

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]

            if name == "":
                unknown_face_encodings.append(face_encoding)
                name = "Unknown " + str(len(unknown_face_encodings))

            face_names.append(name)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert back to BGR for OpenCV
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top = top * int(1 / frame_size) - 20
            right = right * int(1 / frame_size) + 20
            bottom = bottom * int(1 / frame_size) + 20
            left *= int(1 / frame_size)

            # save cutout frame of first recognized face
            cutout_frame = frame[top: bottom, left: right]
            self.current_face = self.convertImage(cutout_frame)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (166, 8, 239), 2)

            # Draw a label with a name below the face
            #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (166, 8, 239), 1)

        #convert image so tkinter can display it
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert back to BGR for OpenCV
        photo_img = self.convertImage(frame)

        return photo_img


    def convertImage(self, image):
        img = Image.fromarray(image)
        photo_img = ImageTk.PhotoImage(image=img)
        return photo_img
    
    def photoimage_to_array(self, photo_image):
        # Convert PhotoImage to PIL Image
        pil_image = ImageTk.getimage(photo_image)
        # Convert PIL Image to NumPy array
        numpy_array = np.array(pil_image)
        return numpy_array
    

    def save_current_face(self, root):
        self.openAppFaceUI(root)

    
    def openAppFaceUI(self, root):
        self.popup = Toplevel(root)
        self.popup.minsize(480, 600)
        self.popup.maxsize(480, 600)
        self.popup.title("Add New Face")
        self.popup.protocol("WM_DELETE_WINDOW", self.closeNewFaceInput)

        Label(self.popup, text="Enter name:").pack(pady=10)
        self.name_entry = Entry(self.popup)
        
        self.name_entry.pack(pady=10)
        self.name_entry.focus()
        
        self.popup_image_label = Label(self.popup)
        self.popup_image_label.pack(pady=10)
        self.popup_image_label.config(width=300, height=300)
        self.popup_image_label.photo_image = self.current_face
        self.popup_image_label.config(image=self.current_face)

        Button(self.popup, text="Confirm", command=self.confirmNewFaceInput).pack(side=LEFT, padx=10, pady=10)
        Button(self.popup, text="Cancel", command=self.closeNewFaceInput).pack(side=RIGHT, padx=10, pady=10)

       # self.open_virtual_keyboard()

    def closeNewFaceInput(self):
        # self.close_virtual_keyboard()
        self.popup.destroy()

    def confirmNewFaceInput(self):
        self.close_virtual_keyboard()
        name = self.name_entry.get()
        if name:
            if not os.path.exists('faces'):
                os.makedirs('faces')
            img_path = os.path.join('faces', f"{name}.png")
            self.popup_image_label.photo_image._PhotoImage__photo.write(img_path)

            self.addFaceCallback(name, img_path)

            self.popup.destroy()

    def open_virtual_keyboard(self):
        self.keyboard = Popen(["onboard"])

    def close_virtual_keyboard(self):
        if self.keyboard: 
            self.keyboard.terminate()


    def get_all_faces(self):
        return [f for f in os.listdir(self.faces_folder) if os.path.isfile(os.path.join(self.faces_folder, f))]