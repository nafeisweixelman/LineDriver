# Multiple Scripts, Multiple Threads
# ThreadingStart Script

# Importing the necessary packages
import threading
import time
import SystemStart

exitFlag = 0

# Creating the script call thread
class Script1 (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self._running = True
    def run(self):
        print ("Starting " + self.name)
        SystemStart.Main()
        print_time(self.name, 1, self.counter)
        print ("Exiting " + self.name)

# Printing the results from threads
def print_time(threadName, counter, delay):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        #print ("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# Starting the system thread
thread1 = Script1(1, "Thread-SystemStart", 1)
thread1.start()
print ("Exiting Main Thread")
