from primesense import openni2
import numpy as np
import scipy.misc as misc
import os



class KinectInterface:
    def __init__(self):
        self.path = os.getcwd()
        openni2.initialize()
        self.device = openni2.Device.open_any()
        self.start_depth_stream()
        self.start_rgb_stream()

    def start_depth_stream(self):
        self.depth_stream = self.device.create_depth_stream()
        self.depth_stream.start()

    def start_rgb_stream(self):
        self.rgb_stream = self.device.create_color_stream()
        self.rgb_stream.start()

    def get_depth_img(self):
        depth_frame = self.depth_stream.read_frame()
        depth_frame_data = depth_frame.get_buffer_as_uint16()
        img  = np.frombuffer(depth_frame_data, dtype=np.uint16)
        img.shape = (1, 480, 640)#small chance these may be reversed in certain apis...This order? Really?
        #filling rgb channels with duplicates so matplotlib can draw it (expects rgb)
        img = np.concatenate((img, img, img), axis=0)
        #because the order is so weird, rearrange it (third dimension must be 3 or 4)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
        img = img[0:424, 0:512]
        return img

    def get_rgb_img(self):
        rgb_frame = self.rgb_stream.read_frame()
        rgb_frame_data = rgb_frame.get_buffer_as_uint8()
        img  = np.frombuffer(rgb_frame_data, dtype=np.uint8)
        img.shape = (1080, 1920, 3)
        return img

    def save_depth_and_color(self, iteration):
        depth_img = self.get_depth_img()
        rgb_img = self.get_rgb_img()
        misc.imsave(self.path +'/output/rgb_img_'+ str(iteration) + '.jpg', rgb_img)
        misc.imsave(self.path +'/output/depth_img_'+ str(iteration) + '.jpg', depth_img)


    def close(self):
        self.rgb_stream.close()
        self.depth_stream.close()
        openni2.unload()

#Example usage:
# kinect = KinectInterface()
# kinect.save_depth_and_color(0)
