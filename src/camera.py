import cv2
from tkinter import messagebox, filedialog

class Camera:
    def __init__(self):
        self.set_source()
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise IOError("Cannot open video source.")
        
    def set_source(self):
        self.source = messagebox.askquestion("Choose Source", "Do you want to use the onboard camera? If you select No, you will be asked to choose a file.")
        if self.source == "yes":
            # set your camera to use the onboard camera
            self.source = 0  # usually 0 is the default camera
        else:
            self.filename = filedialog.askopenfilename()
            # set your camera to use the file
            self.source = self.filename
        
    def read_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None
        
    def release(self):
        self.cap.release()