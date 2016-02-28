from kinect_interface import KinectInterface
import scipy.misc as misc
import os
#Get width

setwidth = 1920
setviewangle = 84.1

#get angle data from arduino
import serial
import time
kinect = KinectInterface()
ser = serial.Serial('/dev/cu.usbmodem1411', 9600)

# i = 1
# while x < 180:
#     if int(ser.readline()) - x >= 15:
#         print "%d I hate jews" % i
#         x = int(ser.readline())
#         i = i+1
#     print int(ser.readline())

done = False

x = int(ser.readline())
kinect.save_depth_and_color(x/15)
while not done:
    x = int(ser.readline())
    print x
    if x%15 ==0:
        kinect.save_depth_and_color(x/15)
    if x >= 180:
        done = True
