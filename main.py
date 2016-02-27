def main():
    pass

from clarifai.client import ClarifaiApi
from matplotlib import pyplot as plt
import numpy as np
import cv2
import pdb
cap0 = cv2.VideoCapture(1)

ret0, frame0 = cap0.read()
cv2.imwrite('frame_capture0.jpg', frame0)
# Display the resulting frame
cv2.imshow('frame0', frame0)


clarifai_api = ClarifaiApi() # assumes environment variables are set.

result0 = clarifai_api.tag_images(open('frame_capture0.jpg', 'rb'))
print result0

continueInput = raw_input("Say yes for picture 2")
while continueInput != "yes":
  continueInput = raw_input("Say yes for picture 2")

ret1, frame1 = cap0.read()
cv2.imwrite('frame_capture1.jpg', frame1)
cv2.imshow('frame1', frame1)

result1 = clarifai_api.tag_images(open('frame_capture1.jpg', 'rb'))
print result1

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=5)
# pdb.set_trace()
disparity = stereo.compute(cv2.imread('frame_capture0.jpg',0),cv2.imread('frame_capture1.jpg',0))
plt.imshow(disparity,'gray')
plt.show()

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # When everything done, release the capture
        cap0.release()
        cap1.release()
        cv2.destroyAllWindows()
