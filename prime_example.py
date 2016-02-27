from primesense import openni2
import pdb
import numpy as np
import matplotlib.pyplot as plt

openni2.initialize()     # can also accept the path of the OpenNI redistribution

dev = openni2.Device.open_any()
file = open('prime_example_output.txt', 'w')
print dev.get_sensor_info()

depth_stream = dev.create_depth_stream()
depth_stream.start()
frame = depth_stream.read_frame()
frame_data = frame.get_buffer_as_uint16()
pdb.set_trace()

dataString = str(frame_data)
file.write(dataString)


depth_stream.stop()

openni2.unload()