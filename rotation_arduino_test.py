import serial
ser = serial.Serial('COM4', 19200)
while True:
	print ser.readline()
