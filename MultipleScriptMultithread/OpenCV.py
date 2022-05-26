# Multiple Threads, Multiple Threads
# OpenCV Script

# Importing the necessary packages
from collections import deque
from imutils.video import VideoStream
from time import sleep
import numpy as np
import cv2
import imutils

# Calling other scripts
import Turning
import Driving
import Stopping

# Creating Start function
def Start():
    # Start the VideoStream
    print("Starting VideoStream..")
    vs = VideoStream(src=0).start()

    # Giving time so the camera can boot
    sleep(1)
    print("Started VideoStream, Done!")
    return vs

# Scanning the colors from camera
def Scanning(Lower,Upper,vs, CheckColor):
    Color = 0
    CenterX = 0
    CenterY = 0
    radius = int(0)
    # View current frame
    frame = vs.read()

    # Analyze the color frame
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Construct the mask for the specific color
    mask = cv2.inRange(hsv, Lower, Upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Finding contours in the mask and finding the current (x,y) center
    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    center = None

    # If no color was found, stop moving
    Stopping.Stop()

    # If only one contour was found
    if len(contours) > 0:

        # Find the largest contour in mask and find the radius and object
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if radius > 30:
            # Draw the tracking circle on the object
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            # Centering object
            if CheckColor == "Green":
                Color = 1
                CenterX = (int(x))
                CenterY = (int(y))
            elif CheckColor == "Red":
                Color = 1

    # Displaying frato debug
    cv2.imshow("Camera Live Feed", frame)

    # Returning the parameters
    key = cv2.waitKey(1) & 0xFF
    return Color, key, CenterX, CenterY
