import cv2

class Camera:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        
    def read_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            return None
        
    def release(self):
        self.cap.release()