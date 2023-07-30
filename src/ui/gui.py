import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from camera import Camera
import os
import time

class Application(tk.Frame):
    def __init__(self, master=None, vision = None, controller = None):
        super().__init__(master)
        
        self.master = master
        self.master.title('Autonomous Driving Project')
        self.master.geometry('1100x60') # Set the size of the window
        
        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_path = os.path.join(script_dir, 'musk_image.ico')
        self.master.iconbitmap(icon_path)
        
        self.pad_x_val = 5
        self.pad_y_val = 5

        self.master = master
        self.camera = Camera()
        self.vision = vision
        self.controller = controller
        
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.toolbar = tk.Frame(self, bd=1, relief='raised')
        self.toolbar.pack(side="top", fill="x") # Make the toolbar fill the x direction

        self.bt_connect = tk.Button(self.toolbar, text="Start Self Driving", command=self.start_self_driving, height=2, width=20, font = ("Arial", 10))
        self.bt_connect.pack(side="left", padx=self.pad_x_val, pady=self.pad_y_val)

        self.select_camera = tk.Button(self.toolbar, text="Select Camera", command=self.select_camera_func, height=2, width=20, font = ("Arial", 10))
        self.select_camera.pack(side="left", padx=self.pad_x_val, pady=self.pad_y_val)

        self.display_feed = tk.Button(self.toolbar, text="Display Camera Feed", command=self.display_camera_feed, height=2, width=20, font = ("Arial", 10))
        self.display_feed.pack(side="left", padx=self.pad_x_val, pady=self.pad_y_val)

        self.chk_steering_offset = tk.Checkbutton(self.toolbar, text="Visualize Steering Offset", height=2, width=20, font = ("Arial", 10))
        self.chk_steering_offset.pack(side="left", padx=self.pad_x_val, pady=self.pad_y_val)

        self.throttle_threshold_label = tk.Label(self.toolbar, text="Throttle Threshold")
        self.throttle_threshold_label.pack(side="left", padx=self.pad_x_val, pady=self.pad_y_val)

        self.throttle_threshold_entry = tk.Entry(self.toolbar, width=10)
        self.throttle_threshold_entry.pack(side="left", padx=self.pad_x_val, pady=self.pad_y_val)

        self.stop = tk.Button(self.toolbar, text="EMERGENCY STOP", fg="red", command=self.emergency_stop, height=2, width=20, font = ("Arial", 10))
        self.stop.pack(side="left", padx=self.pad_x_val, pady=self.pad_y_val)

    def choose_source(self):
        source = messagebox.askquestion("Choose Source", "Do you want to use the onboard camera? If you select No, you will be asked to choose a file.")
        if source == "yes":
            # set your camera to use the onboard camera
            self.camera.set_source(0)  # usually 0 is the default camera
        else:
            filename = filedialog.askopenfilename()
            # set your camera to use the file
            self.camera.set_source(filename)

    def start_self_driving(self):
        print("Starting Self Driving...")
        self.choose_source()
                
        while True:
            frame = self.camera.read_frame()

            if frame is not None:
                start_time = time.time()
                processed_frame = self.vision.process_frame(frame)
                self.controller.update(processed_frame)       
            
            else:
                break

        end_time = time.time()  # end timer
        elapsed_time = end_time - start_time  # elapsed time in seconds
        print(f"The elapsed time is {elapsed_time} seconds")
        
        self.camera.release()
        

    def select_camera_func(self):
        print("Selecting camera...")
        # Add your camera selection code here

    def display_camera_feed(self):
        print("Displaying camera feed...")
        # Add your code to display camera feed here

    def emergency_stop(self):
        print("EMERGENCY STOP")
        # Add your emergency stop code here
        messagebox.showinfo("Emergency Stop", "There is no stopping.")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
