import facerecognition
import ui

fr = facerecognition.FaceRecognition()

frame = ui.UI(fr)

frame.showUI()