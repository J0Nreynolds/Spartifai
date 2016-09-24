import serial
import time

# Serial is used to listen on usb port for Arduino information
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
