from primesense import openni2
import numpy as np
import matplotlib.pyplot as plt


def print_frame(frame_data, thisType):
    #need to know what format to get the buffer in:
    # if color pixel type is RGB888, then it must be uint8,
    #otherwise it will split the pixels incorrectly
    img  = np.frombuffer(frame_data, dtype=thisType)
    whatisit = img.size
    #QVGA is what my camera defaulted to, so: 1 x 480 x 640
    #also order was weird (1, 480, 640) not (640, 480, 1)
    if whatisit == (640*480*1):#QVGA
        img.shape = (1, 480, 640)
        #This order? Really? ^
        #shape it accordingly
        img = np.concatenate((img, img, img), axis=0)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
    elif whatisit == (640*480*3):
        img.shape = (480, 640, 3)
        #these are, what is it, normalizsed?
    else:
        print "Frames are of size: ",img.size
    #images still appear to be reflected, but I don't need them to be correct in that way
    print img.shape
    #need both of follwoing: plt.imShow adds image to plot
    plt.imshow(img)
    #plt.show shows all the currently added figures
    #plt.show()
    plt.pause(0.1)
    plt.draw()
    plt.close()

openni2.initialize()     # can also accept the path of the OpenNI redistribution

dev = openni2.Device.open_any()
#print dev.get_sensor_info()

depth_stream = dev.create_depth_stream()
depth_stream.start()
frame = depth_stream.read_frame()
frame_data = frame.get_buffer_as_uint16()
dt = np.uint16

print_frame(frame_data, dt)

depth_stream.stop()

openni2.unload()
