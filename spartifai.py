from kinect_interface import KinectInterface
import tag_handler
import say

import scipy.misc as misc
import os
#Get width
path = os.getcwd()

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
angle = 15
mins = [0]*int(180/angle + 1)
done = False
x = int(ser.readline())
kinect.save_depth_and_color(x/angle)
while not done:
    x = int(ser.readline())
    print x
    if x%angle ==0:
        mins[int(x/angle)] = kinect.save_depth_and_color(int(x/angle))
    if x >= 180:
        done = True

minVal = mins[0]
minIndex = 0
for index, distance in enumerate(mins):
    if distance < min:
        minVal = distance # in millimeters
        minIndex = index

tag_handler.main(path)
hour = tag_handler.put_time_in_hours(minIndex/12.0)
say.say("Additionally, we detect the nearest object is " + str((float(minVal)/10.0)) + " centimeters away from you at your %s-o-clock." % int(hour))
