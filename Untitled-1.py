from tkinter import *
import tkinter
import os
import facerecognition
from PIL import Image, ImageTk

class Pokedex:
    def open(self):
        face_recognition = facerecognition.FaceRecognition()
        face_recognition.setup_wincam()

        # List of dangerous persons (for simplicity, we use IDs or names here)
        # danger_level is a string like "low", "medium", "high"
        dangerous_persons = [
            {"name": "John Doe", "danger_level": "high", "face_id": 1},  # Example person
            {"name": "Jane Smith", "danger_level": "medium", "face_id": 2}
        ]

        # Create the root window
        root = tkinter.Tk()
        root.title("Pokedex")
        root.minsize(480, 800)
        root.maxsize(480, 800)

        # Label to display the camera frame
        image = Label(root)
        image.pack()

        # Label to display danger warnings
        danger_label = Label(root, text="", font=("Helvetica", 16), fg="red")
        danger_label.pack()

        def update_image():
            frame = face_recognition.get_camera_frame()
            recognized_faces = face_recognition.scan_faces_in_frame(frame)
            
            # Check if any faces are recognized and compare with dangerous persons
            for face in recognized_faces:
                face_id = face.get("id")  # Assuming face recognition returns an ID for recognized faces
                person = next((p for p in dangerous_persons if p["face_id"] == face_id), None)
                
                if person:
                    danger_label.config(text=f"Dangerous person detected: {person['name']} (Level: {person['danger_level']})")
                    # Here you could also add additional actions such as sound alarms, etc.
                else:
                    danger_label.config(text="No dangerous persons detected")

            # Display the camera frame on the label
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            image.photo_image = img
            image.config(image=image.photo_image)

            root.after(10, update_image)  # Update the image every 10 ms

        update_image()

        # Button to save current face (add to dangerous list, etc.)
        button = Button(root, text="Save Current Face", command=lambda: face_recognition.save_current_face(root))
        button.pack()

        root.mainloop()


pokedex = Pokedex()
pokedex.open()
