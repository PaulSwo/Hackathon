import face_recognition
import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 
import os

class FaceRecognition:

    faces_folder = "faces"

    known_face_encodings = []
    known_face_names = []

    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        if not self.video_capture.isOpened():
            print("Camera could not be opened")
            exit()

        for filename in os.listdir(self.faces_folder):
            self.add_face(filename.split(".")[0], os.path.join(self.faces_folder, filename))


    def add_face(self, name, image_path):
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]

        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(name)
        

    def get_frame(self):
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        frame_size = 0.33

        # Grab a single frame of video
        ret, frame = self.video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
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
                name = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top = top * int(1 / frame_size) - 20
            right = right * int(1 / frame_size) + 20
            bottom = bottom * int(1 / frame_size) + 20
            left *= int(1 / frame_size)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 255, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (0, 0, 0), 1)

        #convert image so tkinter can display it
        array_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(array_img)
        photo_img = ImageTk.PhotoImage(image=img)

        return photo_img
        

    def release(self):
        self.video_capture.release()
        cv2.destroyAllWindows()