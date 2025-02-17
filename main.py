import facerecognition
import ui

frame = ui.UI()
fr = facerecognition.FaceRecognition(frame)

fr.loop()