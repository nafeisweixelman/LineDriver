# Multiple Scripts, Multiple Threads
# Driving script

# Importing the necessary packages
from gpiozero import Robot
from time import sleep

# Declaring motors via GPIO pins
front = Robot(left=(8,7), right=(10,9))
rear = Robot(left=(19,20), right=(17,18))

# Moving car forward
def Forward(x):
    speed = 1
    time = x
    front.forward(speed)
    rear.forward(speed)
    sleep(time)
