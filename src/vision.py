import cv2
import numpy as np

class Vision:
    def __init__(self):
        return
    
    def process_frame(self, frame): # the meat and potatoes     
        
        # apply vision algorithm
        offset_from_center = self._calculate_offset(frame)
        # radius_of_curve = self._calculate_radius(frame)
        
        return { # return as library
            'offset': offset_from_center,
            # 'radius': radius_of_curve,
        }
    
    def _calculate_offset(self, frame):
        
        # Load image and convert to grayscale
        image = frame
        image = cv2.resize(image, (1600,900))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Cut the image in half horizontally
        height, width = gray.shape
        lower_half = gray[height//2:]
        
        # Threshold the lower half of the image
        _, thresholded = cv2.threshold(lower_half, 150, 255, cv2.THRESH_BINARY)

        # Create an image SPECIFICALLY for thresholding contours
        contour_image = np.zeros_like(image.shape, dtype=np.uint8)
        contour_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to get a binary image
        _, contour_image = cv2.threshold(contour_image, 150, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        area_threshold = 200
        height_threshold = 300
        horizontal_threshold = 0.1
        angle_threshold = 45
        angle_threshold_rad = np.deg2rad(angle_threshold)
        
        # Create a blank image to draw the contours on
        contour_image = np.zeros_like(image)
        
        lines = None
        offset_from_center = 0
        
        # Iterate over the contours
        for i, contour in enumerate(contours):
            # Get the bounding box of the contour
            x, y, w, h = cv2.boundingRect(contour)
            
            # Check if the contour touches the bottom of the image and is big enough
            if y + h == lower_half.shape[0] \
            and cv2.contourArea(contour) > area_threshold \
            and h > height_threshold:
                
                # Fit a polynomial to the contour
                contour = contour.reshape(-1, 2)
                poly_params = np.polyfit(contour[:, 1], contour[:, 0], 2)
                poly = np.poly1d(poly_params)
               
                # Calculate the derivative of the polynomial to get its slope
                poly_derivative = poly.deriv()
                
                # Ignore the contour if the polynomail fits to horizontal, i.e., the slope is close to zero at y = 0
                slope_at_y0 = poly_derivative(0)
                if abs(slope_at_y0) < horizontal_threshold:  # Adjust this threshold as needed
                    continue
                
                # Ignore the contour if the bounding box is more than half the image size
                if w > image.shape[1] / 2 or h > image.shape[0] / 2:
                    # print("Ignoring large bounding box")
                    continue
                
                cv2.drawContours(image[height//2:], [contour], -1, (0, 255, 0), 3)
                        
                cv2.drawContours(contour_image, contours, -1, (255), 1) # for houghline transform
                
                # Apply Canny Edge Detection
                edges = cv2.Canny(contour_image, 50, 150, apertureSize=3)
                
                # Use Hough Line Transform
                lines = cv2.HoughLinesP(edges, 1, np.pi/180, 110, minLineLength=10, maxLineGap=250)

                # Draw detected lines
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    angle = np.arctan2(y2 - y1, x2 - x1)  # Compute the angle of the line
                    if abs(angle) >= angle_threshold_rad:  # Check if the angle is within the threshold
                        cv2.line(contour_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                         
        #-------------------------------
        
        # find lane lines on left and right hand side of frame
        # find left lane line pixel position
        # find right lane line pixel position
        # find middle point between left and right pixel position
        
        if lines is not None:
            left_lines = []  # lines on the left side of the image
            right_lines = []  # lines on the right side of the image
            for line in lines:
                for x1, y1, x2, y2 in line:
                    slope = (y2-y1)/(x2-x1)
                    if slope < 0:  # left lane has a negative slope
                        left_lines.append((x1, y1))
                        left_lines.append((x2, y2))
                    else:  # right lane has a positive slope
                        right_lines.append((x1, y1))
                        right_lines.append((x2, y2))
            
            if left_lines: # Fit a polynomial to the points in the left lane                
                left_line_points = np.array(left_lines)
                poly_left = np.poly1d(np.polyfit(left_line_points[:, 1], left_line_points[:, 0], 2))
                
            if right_lines: # Fit a polynomial to the points in the right lane
                right_line_points = np.array(right_lines)
                poly_right = np.poly1d(np.polyfit(right_line_points[:, 1], right_line_points[:, 0], 2))
                
            # Calculate the y-coordinate at the car's position
            y_value = lower_half.shape[0]

            # Calculate the x-coordinates of the left and right polynomials at the y-coordinate
            x_left = poly_left(y_value)
            x_right = poly_right(y_value)

            # Calculate the middle point of the lane
            lane_middle_point = (x_left + x_right) / 2

            # Calculate the center of the image
            image_center = width / 2

            # The offset of the car from the center of the lane is the difference
            # between the lane middle point and the image center
            offset_from_center = image_center - lane_middle_point

            if offset_from_center > 10:  # adjust the threshold as needed
                position_status = "Too far right"
            elif offset_from_center < -10:  # adjust the threshold as needed
                position_status = "Too far left"
            else:
                position_status = "Centered"
            
            # Put text
            cv2.putText(
                image,  # image where to put the text
                position_status,  # text
                (10, 50),  # bottom-left corner of the text in the image (in pixels)
                cv2.FONT_HERSHEY_SIMPLEX,  # font type
                1,  # font scale
                (0, 255, 0),  # font color in BGR
                2,  # thickness of the lines used to draw a text
                cv2.LINE_AA  # line type
            )
            
            # Print the offset
            print("Offset from the middle of the lane: {:.2f} pixels".format(offset_from_center))
        
        # For Visualization/Testing:
        minimap = cv2.resize(contour_image, (640, 360)) # Resize the warped contour image to create the minimap
        image_with_minimap = image.copy() # Create a copy of the original image to paste the minimap onto
        image_with_minimap[0:minimap.shape[0], -minimap.shape[1]:] = minimap # Paste the minimap onto the copy of the original image
        image_with_minimap = cv2.resize(image_with_minimap, (1280,720))      
                
        # Display the image
        cv2.imshow('image', image_with_minimap)
        cv2.waitKey()
        # cv2.destroyAllWindows()
        
        return offset_from_center