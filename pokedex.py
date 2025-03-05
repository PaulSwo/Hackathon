import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import time
import facerecognition
import numpy as np
import time


class Pokedex:
    def open(self):
        self.face_recognition = facerecognition.FaceRecognition()
        self.face_recognition.setup_wincam()

        self.root = tk.Tk()
        self.root.title("Pokédex")
        self.root.geometry("500x600")
        self.root.configure(background='#E74C3C')

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')

        self.scan_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(self.scan_frame, text="Scan")

        self.gallery_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(self.gallery_frame, text="Galerie")

        self.setup_styles()
        self.setup_scan_page()
        self.setup_gallery_page()

        self.root.mainloop()

    def setup_styles(self):
        style = ttk.Style()
        style.configure('Custom.TFrame', background='#E74C3C')
        style.configure('TButton', font=("Arial", 12, "bold"), background='#FFD700', foreground='black')

    def setup_scan_page(self):
        frame = tk.Frame(self.scan_frame, bg='black', width=400, height=250, relief=tk.RIDGE, borderwidth=10)
        frame.pack(pady=10)
        frame.pack_propagate(False)

        self.image_label = tk.Label(frame, bg='black')
        self.image_label.pack(expand=True, fill='both', padx=10, pady=10)

        self.status_label = tk.Label(self.scan_frame, text="Bereit zum Scannen", 
                                     font=("Arial", 12, "bold"), fg='white', bg='#E74C3C')
        self.status_label.pack(pady=5)

        scan_button = tk.Button(self.scan_frame, text="🔍 SCAN", command=self.scan_face, bg='#FFD700', fg='black', font=("Arial", 12, "bold"))
        scan_button.pack(pady=10)

        self.update_image()

    def scan_face(self):
        self.status_label.config(text="Scanne...")
        frame = self.face_recognition.get_camera_frame()
        photo_frame = self.face_recognition.scan_faces_in_frame(frame)
        self.face_recognition.save_current_face(self.root)
        self.status_label.config(text="Gesicht gespeichert!")
        self.update_gallery()

    def update_image(self):
        frame = self.face_recognition.get_camera_frame()
        img = self.face_recognition.scan_faces_in_frame(frame)
        self.image_label.photo_image = img
        self.image_label.config(image=self.image_label.photo_image)
        self.root.after(10, self.update_image)

    def setup_gallery_page(self):
        gallery_canvas = tk.Canvas(self.gallery_frame, width=450, height=350, bg='#E74C3C')
        gallery_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.gallery_frame, orient=tk.VERTICAL, command=gallery_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        gallery_canvas.configure(yscrollcommand=scrollbar.set)
        gallery_canvas.bind('<Configure>', lambda e: gallery_canvas.configure(scrollregion=gallery_canvas.bbox("all")))
        gallery_canvas.bind_all("<MouseWheel>", lambda event: gallery_canvas.yview_scroll(-1*(event.delta//120), "units"))

        self.gallery_container = tk.Frame(gallery_canvas, bg='#E74C3C')
        gallery_canvas.create_window((0, 0), window=self.gallery_container, anchor="nw")

        refresh_button = tk.Button(self.gallery_frame, text="🔄 Galerie aktualisieren", command=self.update_gallery)
        refresh_button.pack(side=tk.BOTTOM, pady=5)

        self.update_gallery()

    def update_gallery(self):
        for widget in self.gallery_container.winfo_children():
            widget.destroy()

        saved_images_path = "faces/"
        if not os.path.exists(saved_images_path):
            os.makedirs(saved_images_path)

        image_files = [f for f in os.listdir(saved_images_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        for i, image_file in enumerate(image_files):
            img_path = os.path.join(saved_images_path, image_file)
            try:
                img = Image.open(img_path)
                img.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(img)

                # Frame für jedes Bild + Buttons
                img_frame = tk.Frame(self.gallery_container, bg='#E74C3C')
                img_frame.pack(pady=5, padx=10, anchor="w")

                # Bild
                img_label = tk.Label(img_frame, image=photo, bg='#E74C3C')
                img_label.image = photo  
                img_label.pack(side=tk.LEFT, padx=5)

                # Button-Container
                btn_frame = tk.Frame(img_frame, bg='#E74C3C')
                btn_frame.pack(side=tk.LEFT, padx=5)

                # Löschen-Button 🗑️
                button_del = tk.Button(btn_frame, text="🗑️", command=lambda path=img_path: self.delete_image(path))
                button_del.pack(side=tk.TOP, pady=2)

                # Bearbeiten-Button ✏️
                button_ed = tk.Button(btn_frame, text="✏️", command=lambda path=img_path: self.edit_image(path))
                button_ed.pack(side=tk.TOP, pady=2)

                button_i = tk.Button(btn_frame, text="ℹ️", command=lambda path=img_path: self.info_image(path))
                button_i.pack(side=tk.TOP, pady=2)

                # Dateiname
                filename_label = tk.Label(img_frame, text=image_file, bg='#E74C3C', fg='white')
                filename_label.pack(side=tk.LEFT, padx=10)
            except Exception as e:
                print(f"Fehler beim Laden des Bildes {image_file}: {e}")


    def delete_image(self, path):
        os.remove(path)
        self.update_gallery()  # Galerie neu laden

    def edit_image(self, path):
        self.popup = tk.Tk()
        self.popup.title("name")
        self.popup.geometry("200x100")

        self.label = tk.Label(self.popup, text="name eingeen")
        self.label.pack()

        self.input = tk.Entry(self.popup)
        self.input.pack()

        self.button = tk.Button(self.popup, text="submit", command=lambda: self.rename_image(path, self.input.get()))
        self.button.pack()

    def rename_image(self, old_path, new_name):
        folder, old_name = os.path.split(old_path)  # Verzeichnis und Dateiname trennen
        old_name_without_ext, ext = os.path.splitext(old_name)  # Name & Extension trennen
        print("path old: ", old_path, " new name: ", new_name)
        if new_name:  # Falls der User nicht abbricht
            new_path = os.path.join(folder, new_name + ext)  # Neuer Dateipfad
            print("Folder: ", folder, "new path: ", new_path)
            if not os.path.exists(new_path):  # Prüfen, ob Name schon existiert
                os.rename(old_path, new_path)
                self.update_gallery()  # Galerie aktualisieren
        
        self.popup.destroy()


    def info_image(self, path_img):
        print("öffne info")
        self.info_popup = tk.Toplevel()  # Besser als ein neues Tk-Fenster
        self.info_popup.title("Bildinfo")
        self.info_popup.geometry("300x300")

        file = Image.open(path_img)
        img_info = ImageTk.PhotoImage(file)

        self.image_label_info = tk.Label(self.info_popup, image=img_info)
        self.image_label_info.image = img_info  # Referenz speichern!
        self.image_label_info.pack()


        text_path = path_img.replace("faces/", "txt/").replace(".png", ".txt")
        with open(text_path, "r", encoding="utf-8") as file:
            text = file.read()

        textfeld = tk.Text(self.info_popup, wrap="word", height=15, width=50, font=("Arial", 12))
        textfeld.pack()
        
        textfeld.insert("1.0", text)
        print("schließe print")



pokedex = Pokedex()
pokedex.open()