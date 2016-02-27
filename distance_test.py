import cv2
import numpy as np
from matplotlib import pyplot as plt

cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(2)

ret0, frame0 = cap0.read()
ret1, frame1 = cap1.read()

small0 = cv2.resize(frame0, (0,0), fx=0.3, fy=0.3)
small1 = cv2.resize(frame1, (0,0), fx=0.3, fy=0.3)
cv2.imwrite('frame_left.jpg', small0)
cv2.imwrite('frame_right.jpg', small1)
imgL = cv2.imread('frame_left.jpg',0)
imgR = cv2.imread('frame_right.jpg',0)

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=5)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()
