import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk 
import tkinter
import os
from subprocess import Popen

def open_ui():
    root = tkinter.Tk()
    root.title("Pokedex")
    root.minsize(480, 800)
    root.maxsize(480, 800)

    camera_image = Label(root, text="test text")
    camera_image.config(width=200, height=200)
    camera_image.pack()