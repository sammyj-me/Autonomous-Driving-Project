from camera import Camera
from vision import Vision
# from control.controller import Controller

import time

# Calibration
# Understand input frame:
#   - Look for White lines
#   - Span of white lines at base of screen
#   - Following contour up the screen
#   - Since lines are the same distance, can get scale of pixels

# Init Camera and Vision
camera = Camera("test assets\Straight + Curve Cropped.mp4") # Path to source
vision = Vision()
# controller = Controller()

start_time = time.time()

while True:
    frame = camera.read_frame()
    
    if frame is not None:
        processed_frame = vision.process_frame(frame)
        # controller.update(processed_frame)

    else:
        break

end_time = time.time()  # end timer

elapsed_time = end_time - start_time  # elapsed time in seconds

print(f"The elapsed time is {elapsed_time} seconds")

camera.release()