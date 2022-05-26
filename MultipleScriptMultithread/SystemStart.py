# Multiple Scripts, Multiple Threads
# SystemStart Script

# Calling other scripts
import OpenCV
import Turning
import Driving
import Stopping
# Importing the necessary packages
import cv2
import threading
import time

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
    vs = OpenCV.Start()
    print("Started System, Done!")
    print("Ready")

    # Driving forward thread
    class Forward(threading.Thread):
        def __init__(self, threadID, name, counter):
            threading.Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.counter = counter
            self._running = True
        def run(self):
            print ("Starting " + self.name)
            Driving.Forward(0.2)
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
            Driving.front.stop()
            Driving.rear.stop()
            print_time(self.name, 5, self.counter)
            print ("Exiting " + self.name)

    # Printing the results from threads
    def print_time(threadName, counter, delay):
        while counter:
            if exitFlag:
                threadName.exit()
            time.sleep(delay)
            print ("%s: %s" % (threadName, time.ctime(time.time())))
            counter -= 1

    # Running forever
    while True:

        # Scans for green i.e. go
        if Stop == 0 or Stop == 25:
            Stop = 0
            IsGreen, key, CenterX, CenterY = OpenCV.Scanning(Green_Lower,Green_Upper,vs,Color1)
            if IsGreen:
                # Centering the car on the green line
                IsCenter = Turning.Centering(CenterX, CenterY)
        # Scans for red i.e. stop
        IsRed, key, CenterX, CenterY = OpenCV.Scanning(Red_Lower,Red_Upper,vs,Color2)

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

        # Stopping if the color red was seen or the user presses "q"
        if(Done):
            break

    # Stopping the program
    vs.stop()
    cv2.destroyAllWindows
