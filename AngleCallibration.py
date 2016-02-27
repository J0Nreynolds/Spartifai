#Get width

setwidth = 1920
setviewangle = 84.1

#get angle data form arduino
import serial
import time
ser = serial.Serial('/dev/cu.usbmodem1411', 19200)
x = int(ser.readline())
print x
i = 1
while x < 180:
    if int(ser.readline()) - x >= 15:
        print "%d I hate jews" % i
        x = int(ser.readline())
        i = i+1
    print x
