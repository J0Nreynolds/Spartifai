def main():
    pass

from clarifai.client import ClarifaiApi

import cv2
cap0 = cv2.VideoCapture(0)
ret0, frame0 = cap0.read()
cv2.imwrite('frame_capture.jpg', frame0)
# Display the resulting frame
cv2.imshow('frame', frame0)


clarifai_api = ClarifaiApi() # assumes environment variables are set.
result = clarifai_api.tag_images(open('frame_capture.jpg', 'rb'))
print result

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # When everything done, release the capture
        cap0.release()
        cap1.release()
        cv2.destroyAllWindows()
