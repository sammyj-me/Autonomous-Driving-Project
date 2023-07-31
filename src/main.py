from camera import Camera
from vision import Vision
from control.controller import Controller

def main():
    
    # Init Camera and Vision
    camera = Camera()    
    vision = Vision(visualize=True)
    controller = Controller(Kp_steering=0.2, Ki_steering=0.1, Kd_steering=0.1,
                            Kp_throttle=0.2, Ki_throttle=0.1, Kd_throttle=0.1, dt=0.1)
    
    while True:
        frame = camera.read_frame()

        if frame is not None:
            processed_frame = vision.process_frame(frame)
            controller.update(processed_frame)       
        
        else:
            break
    
    camera.release()

if __name__ =="__main__":
    main()