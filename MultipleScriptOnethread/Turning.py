# Multiple Script, One Thread
# Turning Script

# Importing the necessary packages
from time import sleep

# Calling other scripts
import Driving

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
        Driving.front.right(speed)
        Driving.rear.right(speed)
        sleep(1.5 * time)
        return 0
    elif(x < 270):
        # Moving to the right to center object
        Driving.front.right(speed)
        Driving.rear.right(speed)
        sleep(time)
        return 0
    elif(x > 360):
        # Moving to the left to center object
        Driving.front.left(speed)
        Driving.rear.left(speed)
        sleep(1.5 * time)
        return 0
    elif(x > 330):
        # Moving to the left to center object
        Driving.front.left(speed)
        Driving.rear.left(speed)
        sleep(time)
        return 0
    else:
        return 1
