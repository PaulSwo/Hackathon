import tkinter as tk
import cv2
from PIL import Image, ImageTk

# Funktion zum Starten der Kamera
def start_camera():
    # Kamera öffnen (0 ist meist die eingebaute Kamera)
    cap = cv2.VideoCapture(0)
    
    def update_frame():
        # Kamera-Bild einlesen
        ret, frame = cap.read()
        if ret:
            # Bild von BGR zu RGB konvertieren
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Bild zu ImageTk konvertieren
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            # Label im Tkinter Fenster aktualisieren
            lbl_img.imgtk = imgtk
            lbl_img.configure(image=imgtk)
        
        # Funktion alle 10ms wieder aufrufen
        lbl_img.after(10, update_frame)

    # Frame-Update starten
    update_frame()

# Tkinter Fenster erstellen
root = tk.Tk()
root.title("Live Kamera Bild")

# Label für die Anzeige des Kamerabildes
lbl_img = tk.Label(root)
lbl_img.pack()

# Button zum Starten der Kamera
btn_start = tk.Button(root, text="Kamera starten", command=start_camera)
btn_start.pack()

# Fenster starten
root.mainloop()
