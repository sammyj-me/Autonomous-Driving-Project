# About
This is an Autonomous driving project that uses Computer Vision Algorithms, Python, Path Planning
and real-world hardware to self direct an RC car around a running track.

# Skills
- ROS Nav Stack ROS Plugins?
- C++ & Python for real-time embedded control
- Signal Processing Techniques
- Motion Planning & Control Algorithms

# Vision Algorithm Breakdown:
- Collect and Process Images from Camera
    - https://www.youtube.com/watch?v=KdYz77p6NfM
    - Track MUST take up 2/3 of the screen
    - Good lighting helps
- For each Frame:
    - Collect Encoder Data (Real Time Velocity)
    - Line paths are determined from vision algorithm
    - Throttle PID is Calculated
    - Steering PID is Calculated
        - Get Current Steering Angle...? By PID?
        - Look at angle of each line path (use one)
            - Probabilistic Hough Transform
            - Radon Transform
            - Curvature Scale Space
            - Polynomial Fitting          --> Chose this
            - Sliding Window Approach
        - Calculate Lateral Error
            - The distance from the center of the car to the center of the path defined by lines
            - Center of the car to the center of the path is a pre-measured distance. For example: The USA highway system has lines spaced 12 feet apart.
        - Curve Handling
        - Update steering angle plan to servo
    - Throttle is Set
    - Steering is Set
    - Listen for Bluetooth commands 
    - Perfom Vision SLAM based on encoder distance travelled + recognized visual features.


# From Found Implementation (see above):
    Objective:
        - The objective of this project was to design and develop a software that identifies the lane lines on the road from an FPV video stream of a vehicle.
        - The ultimate goal was not only to annotate the lane (drivable area) in a given frame, but also to compute the radius of curvature and vehicle offset from the lane centre.
        - Additional effort was made to mark the lane lines as well and to demonstrate some of the prominent intermediate steps of the processing pipeline such as thresholding, warping and lane detection.

    Source Video:
    - The source video used for this implementation includes an asphalt road with concrete patches present at certain portions.
    - The lanes are marked with solid yellow markings at the road bounds and dashed white markings at each individual lane separation, which vary in their curvature throughout the video.
    - This calls for implementing a sophisticated algorithm with inherent intelligence to track lane lines in successive frames that makes use of both colour and gradient information for the lane detection task.

    Implementation:
    - First, the input frame was undistorted based on the intrinsic parameters of the camera (obtained through calibration).
        - 

    - Next, the undistorted frame was thresholded with a combination of thresholding techniques.
        - These included absolute gradients in x and y directions, magnitude gradient, direction gradient applied to grayscale transformed frame and colour threshold applied to the S channel of the HSL transformed frame.
    - Next, the thresholded binary image was warped by applying a perspective transform in order to get a bird’s eye view of the road, which would make lane detection easier.
    - Next, the lane lines had to be detected, which was achieved in two ways.
        - The first technique basically involved performing an uninformed search to detect the lane lines, which was employed in the first few frames and when no lines were detected in the previous frame.
        - The idea was to detect the lane lines by thoroughly analysing the histogram of the lower half image and detecting the peaks to infer the starting points for the left and right lines, followed by sliding a number of windows to further detect the lane lines till the end of the frame and fit a polynomial function to both the detected lines.
        - The second technique basically involved performing an informed search in the neighbourhood of previously detected lane lines, which was employed once the algorithm had enough confidence from prior knowledge.
    - The idea was to retrieve the coefficients of previously fit polynomials and search in the neighbourhood of that reference to detect the lane lines.
    - Finally, a new polynomial function was fit to both the detected lines.
    - Finally, the detected lanes were transformed back onto the original (undistorted) image and annotated respectively.
    - Meanwhile, the radius and offset information was computed by analysing the polynomials fit to each of the two lane lines.
    - While the radius was deduced by averaging the radius of left and right lane polynomials, the offset, on the other hand, was computed by subtracting the frame width from the lane centre location at the bottom of the image.

# Hardware Breakdown:
- Off the shelf RC Car
- Raspberry PI
- Raspberry PI BlueTooth Module
- 3D printed Camera/PI Mount
- Wiring to Steering Servo
- Wiring to Throttle (ESC)

# UI Breakdown:
- TKinter
    - Run Mode
        - Control Car Throttle/Steering with WASD
    - Autonomous Mode
        - Start 
            - Car runs on VISION ALGORITHM
        - Threshold for Max Throttle
        - STOP
    - Retry Connection (Button) to Bluetooth Signal Control
