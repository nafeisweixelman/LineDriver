# One Script, Multiple Threads

# Calling other scripts
import cv2
import threading
import time
# Importing the necessary packages
from gpiozero import Robot
from collections import deque
from imutils.video import VideoStream
from time import sleep
import numpy as np
import imutils

exitFlag = 0

def Start():
    # Start the VideoStream
    print("Starting VideoStream..")
    vs = VideoStream(src=0).start()

    # Giving time so the camera can boot
    sleep(1)
    print("Started VideoStream, Done!")
    return vs


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
    Stop()

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

    key = cv2.waitKey(1) & 0xFF
    return Color, key, CenterX, CenterY

# Moving car forward
def ForwardCar(x):
    speed = 1
    time = x
    front.forward(speed)
    rear.forward(speed)
    sleep(time)

# Stopping Car
def Stop():
    front.stop()
    rear.stop()

# Moving directions
def Centering(x,y):
    speed = 0.5
    time = 0.1
    print("X = ",x)
    print("Y = ",y)
    if(y > 350) and ((x < 360) or (x > 240)):
        time = 1.5 * time
    if(x < 240):
        # Moving to the right to center object
        front.right(speed)
        rear.right(speed)
        sleep(1.5 * time)
        return 0
    elif(x < 270):
        # Moving to the right to center object
        front.right(speed)
        rear.right(speed)
        sleep(time)
        return 0
    elif(x > 360):
        # Moving to the left to center object
        front.left(speed)
        rear.left(speed)
        sleep(1.5 * time)
        return 0
    elif(x > 330):
        # Moving to the left to center object
        front.left(speed)
        rear.left(speed)
        sleep(time)
        return 0
    else:
        return 1

def Main():
    # Variable Declarations
    global key
    Center = 0
    Color1 = "Green"
    Color2 = "Red"
    IsGreen = 0
    IsRed = 0
    Stop = 0
    exitFlag = 0
    Stop = 0
    StartTime = time.time()
    Done = 0

    # Define the lower and upper boundaries of the color to track
    Green_Lower = (60, 100, 50)
    Green_Upper = (90, 255, 255)
    Red_Lower = (100, 180, 100)
    Red_Upper = (255, 250, 255)

    print("Starting System..")
    vs = Start()
    print("Started System, Done!")
    print("Ready")

    # Forward thread
    class Forward(threading.Thread):
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter
            self._running = True
        def run(self):
            print ("Starting " + self.name)
            ForwardCar(0.2)
            print_time(self.name, 5, self.counter)
            print ("Exiting " + self.name)

    # Stopping thread
    class Stopping(threading.Thread):
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter
            self._running = True
        def run(self):
            print ("Starting " + self.name)
            front.stop()
            rear.stop()
            print_time(self.name, 5, self.counter)
            print ("Exiting " + self.name)

    # Print function for threads
    def print_time(threadName, counter, delay):
        while counter:
            if exitFlag:
                threadName.exit()
            time.sleep(delay)
            print ("%s: %s" % (threadName, time.ctime(time.time())))
            counter -= 1

    while True:

        # Scans for green i.e. go
        if Stop == 0 or Stop == 25:
            Stop = 0
            IsGreen, key, CenterX, CenterY = Scanning(Green_Lower,Green_Upper,vs,Color1)
            if IsGreen:
                # Centering the car on the green line
                IsCenter = Centering(CenterX, CenterY)
        # Scans for red i.e. stop
        IsRed, key, CenterX, CenterY = Scanning(Red_Lower,Red_Upper,vs,Color2)

        # Stopping car
        if IsRed:
            print("Stopping")
            threadStop = Stopping(1, "Thread-Stopping", 1)
            threadStop.start()
            Stop = 1
            FinalTime = time.time() - StartTime
            print("                                             ",FinalTime)
            Done = 1
        elif Stop > 0:
            Stop = Stop + 1

        # Moving car forward
        if IsGreen and Stop == 0:
            print("Moving")
            threadForward = Forward(1, "Thread-Forward", 1)
            threadForward.start()
        if key == ord("q"):
            Done = 1

        # Exiting if the color red was found or the user presses "q"
        if(Done):
            break
    # Stopping the program
    vs.stop()
    cv2.destroyAllWindows

# Main system thread
class Script1 (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self._running = True
    def run(self):
        print ("Starting " + self.name)
        Main()
        print_time(self.name, 1, self.counter)
        print ("Exiting " + self.name)

def print_time(threadName, counter, delay):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        #print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# Declaring motors via GPIO pins
front = Robot(left=(8,7), right=(10,9))
rear = Robot(left=(19,20), right=(17,18))

# Starting the System thread
thread1 = Script1(1, "Thread-SystemStart", 1)
thread1.start()
print ("Exiting Main Thread")
