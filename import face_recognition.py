import face_recognition
import cv2
import numpy as np

# Liste für bekannte Gesichtscodierungen und Namen
known_face_encodings = []
known_face_names = []

# Funktion, um Gesichter hinzuzufügen
def add_face(image_path, name):
    # Lade das Bild und extrahiere das Gesicht
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)

# Beispielbilder und Namen (Achte darauf, den richtigen Pfad zu den Bildern anzugeben)
add_face("C:/Users/ITLab5/Desktop/Hackathon/person1.jpg", "Max Mustermann")
add_face("C:/Users/ITLab5/Desktop/Hackathon/person2.jpg", "Erika Musterfrau")

# Lade die Kamera
video_capture = cv2.VideoCapture(0)

while True:
    # Lese ein Bild von der Webcam
    ret, frame = video_capture.read()

    # Finde alle Gesichter im Bild
    rgb_frame = frame[:, :, ::-1]  # Konvertiere das Bild von BGR zu RGB
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Vergleiche jedes erkannte Gesicht mit den bekannten Gesichtern
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unbekannt"

        # Wenn es eine Übereinstimmung gibt, verwende den Namen des übereinstimmenden Gesichts
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Zeichne ein Rechteck um das Gesicht und den Namen
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Zeige das Ergebnis
    cv2.imshow('Video', frame)

    # Beende das Programm mit der "q"-Taste
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Beende die Videoaufnahme und schließe alle Fenster
video_capture.release()
cv2.destroyAllWindows()