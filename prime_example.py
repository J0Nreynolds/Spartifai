from primesense import openni2
import pdb
import numpy as np
import matplotlib.pyplot as plt


def print_frame(frame_data, thisType):
    #need to know what format to get the buffer in:
    # if color pixel type is RGB888, then it must be uint8, 
    #otherwise it will split the pixels incorrectly
    img  = np.frombuffer(frame_data, dtype=thisType)
    whatisit = img.size
    #QVGA is what my camera defaulted to, so: 1 x 240 x 320
    #also order was weird (1, 240, 320) not (320, 240, 1)
    if whatisit == (640*480*1):#QVGA
        #shape it accordingly, that is, 1048576=1024*1024
        img.shape = (1, 480, 640)#small chance these may be reversed in certain apis...This order? Really?
        #filling rgb channels with duplicates so matplotlib can draw it (expects rgb)
        img = np.concatenate((img, img, img), axis=0)
        #because the order is so weird, rearrange it (third dimension must be 3 or 4)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
    elif whatisit == (640*480*3):
        #color is miraculously in this order
        img.shape = (480, 640, 3)
    else:
        print "Frames are of size: ",img.size

    #images still appear to be reflected, but I don't need them to be correct in that way
    print img.shape
    #need both of follwoing: plt.imShow adds image to plot
    plt.imshow(img)
    #plt.show shows all the currently added figures
    plt.show()


openni2.initialize()     # can also accept the path of the OpenNI redistribution

dev = openni2.Device.open_any()
file = open('prime_example_output.txt', 'w')
print dev.get_sensor_info(openni2.SENSOR_DEPTH)

depth_stream = dev.create_depth_stream()
depth_stream.start()
frame = depth_stream.read_frame()
frame_data = frame.get_buffer_as_uint16()
print_frame(frame_data, np.uint16)


depth_stream.stop()

openni2.unload()