import cv2
import numpy as np

cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(2)

while(True):
    # Capture frame-by-frame
    ret0, frame0 = cap0.read()
    ret1, frame1 = cap1.read()
    small0 = cv2.resize(frame0, (0,0), fx=0.3, fy=0.3)
    small1 = cv2.resize(frame1, (0,0), fx=0.3, fy=0.3)

    # Our operations on the frame come here
    #gray1 = cv2.cvtColor(small0, cv2.COLOR_BGR2GRAY)
    #gray2 = cv2.cvtColor(small1, cv2.COLOR_BGR2GRAY)

    both = np.hstack((small0,small1))

    # Display the resulting frame
    cv2.imshow('frame', both)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap0.release()
cap1.release()
cv2.destroyAllWindows()
