from primesense import openni2
import pdb
import numpy as np
import matplotlib.pyplot as plt
import cv2

#Show a frame using OpenNI2 frame data
def print_frame(frame_data, arrayType):
    # Must specify the arraytype -
    # RGB frames are in uint8 (RGB channels are from 0-255)
    # Depth frames are in uint16
    img  = np.frombuffer(frame_data, dtype=arrayType)
    if img.size == (640*480*1):
        img.shape = (1, 480, 640)
        img = np.concatenate((img, img, img), axis=0)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
        img = img[0:424, 0:512]

    elif img.size == (1920*1080*3):
        img.shape = (1080, 1920, 3)
    else:
        print "Frames are of size: ",img.size
    print img.shape
    cv2.imwrite('file.jpg', img)
    plt.imshow(img)



openni2.initialize()

dev = openni2.Device.open_any()
#file = open('prime_example_output.txt', 'w')
#print dev.get_sensor_info(openni2.SENSOR_DEPTH)

fig = plt.figure()
a=fig.add_subplot(1,2,1)
depth_stream = dev.create_depth_stream()
depth_stream.start()
depth_frame = depth_stream.read_frame()
depth_frame_data = depth_frame.get_buffer_as_uint16()
print_frame(depth_frame_data, np.uint16)

b= fig.add_subplot(1,2,2)
video_stream = dev.create_color_stream()
video_stream.start()
rgb_frame = video_stream.read_frame()
rgb_frame_data = rgb_frame.get_buffer_as_uint8()
print_frame(rgb_frame_data, np.uint8)

#plt.show shows all the currently added figures
plt.show()

video_stream.stop()
depth_stream.stop()

openni2.unload()
