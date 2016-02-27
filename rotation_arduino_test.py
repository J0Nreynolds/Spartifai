import serial
ser = serial.Serial('dev/cu.usbmodem1411', 19200)
while True:
	print ser.readline()
