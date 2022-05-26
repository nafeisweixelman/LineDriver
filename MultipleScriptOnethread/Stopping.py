# Multiple Script, One Thread
# Stopping script

# Importing the necessary packages
from time import sleep

# Calling other scripts
import Driving

# Stopping Car
def Stop():
    Driving.front.stop()
    Driving.rear.stop()
