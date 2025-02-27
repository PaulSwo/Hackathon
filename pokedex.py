import facerecognition as fs
import ui


ui.open_ui()

# 1. Phase

# Kamera öffnen (nur mit opencv)
# Bild mit Kamera machen + speichern unter ./faces
# Kamere mit Gesichtserkennung öffnen (mit Tkinter)


# 2. Phase

# OeffneKamera() – Startet die Kamera und zeigt das Live-Bild an.
# SchliesseKamera() – Beendet die Kamera und schließt das Fenster.
# MacheFoto() – Nimmt ein Bild auf und speichert es.
# ErkenneGesicht() – Erkennt Gesichter im aktuellen Kamerabild.
# ZeigeGesichterMitBoxen() – Zeigt das Live-Bild mit markierten Gesichtern.
# SpeichereGesicht(name: str) – Speichert das erkannte Gesicht mit einem Namen in einer Datenbank.
# LadeBekannteGesichter() – Lädt die gespeicherten Gesichter in den Speicher.
# VergleicheMitBekanntenGesichtern() – Vergleicht ein erkanntes Gesicht mit den gespeicherten Gesichtern.
# GesichtserkennungAnSchalten() – Aktiviert die automatische Gesichtserkennung im Live-Feed.
# GesichtserkennungAusSchalten() – Deaktiviert die automatische Gesichtserkennung.
# SetzeVertrauensSchwelle(schwelle: float) – Legt fest, wie genau die Gesichtserkennung arbeiten soll.
# ErkenneEmotionen() – Erkennt die Emotion eines Gesichts (falls das Modell das unterstützt).
# StarteVideoAufzeichnung() – Beginnt eine Videoaufnahme.
# StoppeVideoAufzeichnung() – Stoppt die Videoaufnahme und speichert die Datei.
# WechsleKamera(kamera_index: int) – Falls mehrere Kameras verfügbar sind, kann man damit wechseln.