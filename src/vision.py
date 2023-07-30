import cv2
import numpy as np

class Vision:
    def __init__(self):
        self.lane_width = 33
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
        image = cv2.resize(image, (900,540))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Cut the image in half horizontally
        height, width = gray.shape
        lower_half = gray[height//2:]
        
        # Threshold the lower half of the image
        _, thresholded = cv2.threshold(lower_half, 150, 255, cv2.THRESH_BINARY)

        contour_image = np.zeros_like(image.shape, dtype=np.uint8)

        contour_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding to get a binary image
        _, contour_image = cv2.threshold(contour_image, 150, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        area_threshold = 200
        height_threshold = 300
        horizontal_threshold = 0.1
        angle_threshold = 65
        angle_threshold_rad = np.deg2rad(angle_threshold)
        
        # Create a blank image to draw the contours on
        contour_image = np.zeros_like(image)
        
        polynomial_list = []
        
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
                                
                # Check if the polynomial intersects the sides of the frame
                x_at_y0 = poly(0)
                x_at_yheight = poly(lower_half.shape[0])
                if x_at_y0 < 0 or x_at_y0 > width or x_at_yheight < 0 or x_at_yheight > width:
                    continue  # Skip this polynomial
                
                # Calculate the derivative of the polynomial to get its slope
                poly_derivative = poly.deriv()
                
                # Ignore the curve if it's horizontal, i.e., the slope is close to zero at y = 0
                slope_at_y0 = poly_derivative(0)
                if abs(slope_at_y0) < horizontal_threshold:  # Adjust this threshold as needed
                    continue
                
                # Ignore the bounding box if it is more than half the image size
                if w > image.shape[1] / 2 or h > image.shape[0] / 2:
                    # print("Ignoring large bounding box")
                    continue
                
                # Generate x and y values for the polynomial
                y_values = np.linspace(0, lower_half.shape[0], num=5)
                x_values = poly(y_values)
                
                polynomial_list.append((x_values,y_values))
                
            

                # Draw the polynomial on the original image
                for x, y in zip(x_values, y_values):                    
                    
                    # Compute the x values of the polynomial at the 5 y coordinates
                    # x_values = poly(y_values)
                    
                    
                    # Compute the (x, y) coordinates in the birds-eye view
                    # Here, we just flip the y coordinate because in image coordinates, y increases downwards
                    birds_eye_x, birds_eye_y = x, lower_half.shape[0] - (-y)

                    # Plot the point on the top-down 2D plane
                    cv2.circle(contour_image, (int(birds_eye_x + 0.5), int(birds_eye_y + 0.5)), 10, (0, 255, 0), -1)
                    cv2.circle(image, (int(x + 0.5), int(height//2 + y + 0.5)), 10, (0, 255, 0), -1)
                    cv2.drawContours(image[height//2:], [contour], -1, (0, 255, 0), 3)

        # print("polynomials:")
        # print(polynomial_list)
        
        cv2.drawContours(contour_image, contours, -1, (255), 1) # for houghline transform
        
        # Apply Canny Edge Detection
        edges = cv2.Canny(contour_image, 50, 150, apertureSize=3)
        
        # Use Hough Line Transform
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=10, maxLineGap=250)

        # Draw detected lines
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1)  # Compute the angle of the line
            if abs(angle) <= angle_threshold_rad:  # Check if the angle is within the threshold
                cv2.line(contour_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        
        # Resize the warped contour image to create the minimap
        minimap = cv2.resize(contour_image, (640, 360))

        # Create a copy of the original image to paste the minimap onto
        image_with_minimap = image.copy()

        # Paste the minimap onto the copy of the original image
        image_with_minimap[0:minimap.shape[0], -minimap.shape[1]:] = minimap

        image_with_minimap = cv2.resize(image_with_minimap, (1280,720))
        # Display the image
        # cv2.imshow('image', image_with_minimap)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        
        #-------------------------------
        
        # find lane lines on left and right hand side of frame
        # find left lane line pixel position
        # find right lane line pixel position
        # find middle point between left and right pixel positoin
        
        
        # find difference between middle point and true middle 'x' coordinate of frame
            # this is the offset
                
        offset_from_center = 0
        return offset_from_center
    
    def _calculate_radius(self, frame):
        
        return radius_of_curve