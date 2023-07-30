import cv2

class Camera:
    def __init__(self, source=0):
        self.source = source
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise IOError("Cannot open video source.")
    
    def set_source(self, source):
        self.source = source
        self.cap.release()    
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise IOError("Cannot open video source.")
        
    def read_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None
        
    def release(self):
        self.cap.release()