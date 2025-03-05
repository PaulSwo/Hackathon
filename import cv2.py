import cv2
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import threading
import numpy as np
import os
import pickle

# Initialisiere das Tkinter Fenster
root = tk.Tk()
root.title("Gesichtserkennung")
root.geometry("800x600")

# Initialisiere OpenCV für die Kamera
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Daten für gespeicherte Gesichter
faces_data = {}
if os.path.exists('faces_data.pkl'):
    with open('faces_data.pkl', 'rb') as f:
        faces_data = pickle.load(f)

# Variablen zur Verwaltung der UI
is_recognizing = False
recognized_name = ""
name_to_add = None

# Funktion zur Gesichtserkennung
def face_recognition():
    global is_recognizing, recognized_name

    while is_recognizing:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Konvertiere das Bild in Graustufen
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detektiere Gesichter im Bild
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        # Wenn Gesichter erkannt werden
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Überprüfe, ob es ein bekanntes Gesicht ist
            face_id, confidence = recognize_face(gray[y:y+h, x:x+w])
            if face_id is not None:
                recognized_name = face_id
            else:
                recognized_name = "Unbekannt"
        
        # Zeige das Bild in der Tkinter UI an
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)

# Funktion zur Gesichtserkennung anhand eines gespeicherten Gesichts
def recognize_face(face_roi):
    # Wandle das Gesicht in einen Vektor um (z.B. durch Histogrammvergleich oder LBPH)
    face_roi = cv2.resize(face_roi, (200, 200))
    face_vector = np.array(face_roi).flatten()
    
    for name, saved_face in faces_data.items():
        saved_vector = np.array(saved_face).flatten()
        # Berechne den Abstand (Vertrauen) zwischen den Gesichtern
        distance = np.linalg.norm(saved_vector - face_vector)
        if distance < 100:  # Schwellwert, um ein Gesicht als bekannt zu erkennen
            return name, distance
    
    return None, None

# Funktion zum Hinzufügen eines neuen Gesichts mit Namen
def add_new_face(name, face_roi):
    face_roi = cv2.resize(face_roi, (200, 200))
    faces_data[name] = face_roi
    with open('faces_data.pkl', 'wb') as f:
        pickle.dump(faces_data, f)

# Funktion zum Starten der Gesichtserkennung
def start_recognition():
    global is_recognizing
    is_recognizing = True
    threading.Thread(target=face_recognition, daemon=True).start()

# Funktion zum Stoppen der Gesichtserkennung
def stop_recognition():
    global is_recognizing
    is_recognizing = False
    cap.release()
    cv2.destroyAllWindows()

# Funktion für den UI-Button zum Starten der Erkennung
def start_button_clicked():
    start_recognition()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)

# Funktion für den UI-Button zum Stoppen der Erkennung
def stop_button_clicked():
    stop_recognition()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# Funktion für den UI-Button zum Hinzufügen eines neuen Gesichts
def add_face_button_clicked():
    global name_to_add
    name_to_add = simpledialog.askstring("Name eingeben", "Bitte geben Sie den Namen der Person ein:")
    if name_to_add:
        status_label.config(text=f"Bitte Gesicht für {name_to_add} aufnehmen...")

# Funktion zum Verarbeiten des Gesichts und Speichern
def capture_face():
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            add_new_face(name_to_add, face_roi)
            status_label.config(text=f"Gesicht für {name_to_add} gespeichert!")
            break

# Funktion, um den Status der Gesichtserkennung anzuzeigen
def update_status():
    if recognized_name:
        status_label.config(text=f"Erkannt: {recognized_name}")
    root.after(100, update_status)

# Erstelle UI-Elemente
label = tk.Label(root)
label.pack()

status_label = tk.Label(root, text="Warten auf Gesicht...", font=("Arial", 14))
status_label.pack()

start_button = tk.Button(root, text="Starten", font=("Arial", 14), command=start_button_clicked)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stoppen", font=("Arial", 14), state=tk.DISABLED, command=stop_button_clicked)
stop_button.pack(pady=10)

add_face_button = tk.Button(root, text="Neues Gesicht hinzufügen", font=("Arial", 14), command=add_face_button_clicked)
add_face_button.pack(pady=10)

capture_face_button = tk.Button(root, text="Gesicht speichern", font=("Arial", 14), state=tk.DISABLED, command=capture_face)
capture_face_button.pack(pady=10)

# Update den Status in der UI
update_status()

# Hauptloop von Tkinter
root.mainloop()
