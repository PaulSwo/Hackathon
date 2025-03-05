import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading

# Initialisiere das Tkinter Fenster
root = tk.Tk()
root.title("Gesichtserkennung")
root.geometry("800x600")

# Initialisiere OpenCV für die Kamera
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Variablen zur Verwaltung der UI
is_recognizing = False
recognized_name = ""

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
            recognized_name = "Gesicht erkannt"  # Hier kann man auch den Namen anzeigen, wenn eine Datenbank vorhanden ist
        
        # Zeige das Bild in der Tkinter UI an
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)

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

# Funktion, um den Status der Gesichtserkennung anzuzeigen
def update_status():
    if recognized_name:
        status_label.config(text=recognized_name)
    root.after(100, update_status)

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

# Erstelle UI-Elemente
label = tk.Label(root)
label.pack()

status_label = tk.Label(root, text="Warten auf Gesicht...", font=("Arial", 14))
status_label.pack()

start_button = tk.Button(root, text="Starten", font=("Arial", 14), command=start_button_clicked)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stoppen", font=("Arial", 14), state=tk.DISABLED, command=stop_button_clicked)
stop_button.pack(pady=10)

# Update den Status in der UI
update_status()

# Hauptloop von Tkinter
root.mainloop()
