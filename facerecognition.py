import face_recognition
import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 
import os
from picamera2 import Picamera2

class FaceRecognition:

    faces_folder = "faces"

    known_face_encodings = []
    known_face_names = []

    def __init__(self, frame):
        
        self.setup_picam()

        for filename in os.listdir(self.faces_folder):
            self.add_face(filename.split(".")[0], os.path.join(self.faces_folder, filename))

        self.frame = frame

        self.frame.addFaceCallback = self.addFaceCallback

        face_recognition.cpus = 8

    def setup_picam(self):
        self.camera = Picamera2()
        self.camera.start(show_preview=False)

    def setup_wincam(self):
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
        

    def loop(self):
        while True:
            img = self.get_frame()
            self.frame.setImage(img)

        self.frame.destroy()

    def get_frame(self):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        frame_size = 0.25

        # Grab a single frame of video
        #ret, frame = self.camera.read()
        frame = self.camera.capture_array()

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

        if(len(unknown_face_encodings) == 0):
            self.frame.hideAddFaceButton()


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top = top * int(1 / frame_size) - 20
            right = right * int(1 / frame_size) + 20
            bottom = bottom * int(1 / frame_size) + 20
            left *= int(1 / frame_size)


            if(len(unknown_face_encodings) > 0):
                if name == "Unknown 1":
                    cutout_frame = frame[top: bottom, left: right]
                    #array_img = cv2.cvtColor(cutout_frame, cv2.COLOR_BGR2RGBA)
                    self.frame.showAddFaceButton(self.convertImage(cutout_frame))

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 255, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

        #convert image so tkinter can display it
        #array_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        photo_img = self.convertImage(frame)

        return photo_img


    def convertImage(self, image):
        img = Image.fromarray(image)
        photo_img = ImageTk.PhotoImage(image=img)
        return photo_img