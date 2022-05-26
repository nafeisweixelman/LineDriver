# Multiple Script, One Thread
# SystemStart script

# Calling other scripts
import OpenCV
import Turning
import Driving
import Stopping
# Importing the necessary packages
import cv2
import time

# Variable Declarations
global key
Center = 0
Color1 = "Green"
Color2 = "Red"
IsGreen = 0
IsRed = 0
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
        Stopping.Stop()
        Stop = 1
        #FinalTime = time.time() - StartTime
        #print(FinalTime)
        #Done = 1
    elif Stop > 0:
        Stop = Stop + 1

    # Moving car forward
    if IsGreen and Stop == 0:
        print("Moving")
        Driving.Forward(0.02)
    if key == ord("q"):
        Done = 1

    # Stopping if red is detected or the user presses "q"
    if(Done):
        break

# Stopping the program
vs.stop()
cv2.destroyAllWindows
