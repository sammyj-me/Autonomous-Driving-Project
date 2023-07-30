from camera import Camera
from vision import Vision
from control.controller import Controller
from ui.gui import Application
import tkinter as tk

def main():
    
    # Init Camera and Vision
    camera = Camera()
    vision = Vision()
    controller = Controller()
    
    root = tk.Tk()
    app = Application(master = root, camera = camera, vision = vision, controller = controller)
    app.mainloop()

if __name__ =="__main__":
    main()