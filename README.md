# LineDriver
Fully autonomous line following robot

This was coded usig a Raspberry Pi 4, which would use the Pi Camera to control four L298N wheel controllers.
The camera would take the color feed from the camera, and follow the line of any color, but would stop if a red object was seen.
This can be attributed similar to a street light, red means stop, and green means go.

The following steps are needed for implimentation:
1. In order to run this code, you need to install OpenCV and the required support software for it.
2. You can follow this tutorial, I recommend installing the full package and not the pip version.
https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/
3. For our code, we had to enter the Python Virtual Environment by using the "workon cv" command at terminal.
4. In order to use the GPIOZero class, you will have to install that directly into the Virtual Environment.
5. Then to run the code, browse to the file directory to the right folder and run the python scripts.
