# Multiple Scripts, Multiple Threads
# Stopping Script

# Importing the necessary packages
from time import sleep

# Calling other scripts
import Driving

# Stopping Car
def Stop():
    Driving.front.stop()
    Driving.rear.stop()
