import cv2
import os
import scipy.misc as misc
path = os.getcwd()
for x in xrange(15):
    rgb = cv2.imread(path + '/output/rgb_img_' + str(x) + '.jpg')
    depth = cv2.imread(path + '/output/depth_img_' + str(x) + '.jpg')
    depth_inquiry = depth.copy()
    # depth_inquiry[depth_inquiry > 180] = 0

    # Depth threshold test - gets rid of near
    depth_inquiry[depth_inquiry < 50] = 0

    # depth_inquiry[depth_inquiry > 0] = 255
    median = cv2.medianBlur(depth_inquiry,5)

    median = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
    cv2.imshow('depth', median)
    cv2.waitKey(0)

    depth_params = (424, 512)
    rgb_params = (1080, 1920)
    depth_adjusted = (rgb_params[0], depth_params[1]*rgb_params[0]/depth_params[0])
    rgb_cropped = rgb[:, rgb_params[1]/2-depth_adjusted[1]/2:rgb_params[1]/2+depth_adjusted[1]/2]

    resized_median = cv2.resize(median, (depth_adjusted[1], depth_adjusted[0]), interpolation = cv2.INTER_AREA)
    and_result = cv2.bitwise_and(rgb_cropped,rgb_cropped,mask=resized_median)
    cv2.imshow('and', and_result)
    cv2.imwrite(path +'/output/rgb_depth_adjusted_' + str(x) + '.jpg', rgb_cropped )
