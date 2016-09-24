#Get width

setwidth = 1920
setviewangle = 84.1

#get angle data form arduino
import serial
import time
ser = serial.Serial('/dev/cu.usbmodem1411', 19200)
x = int(ser.readline())
print x

# Prints every 15 degrees.
# Used to calibrate beginnning and end of rotation.
done = False
while not done:
    x = int(ser.readline())
    if x%15 ==0:
        print str(x/15)
    if x >= 180:
        done = True

    print int(ser.readline())
ser.close()
