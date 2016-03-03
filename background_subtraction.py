# Reference: http://docs.opencv.org/master/db/d5c/tutorial_py_bg_subtraction.html
# requires opencv v3.1.0

import numpy as np
import cv2

# TODO: remove hard coded file name
cap = cv2.VideoCapture('videos/sample_video_2.mp4')

# Here are the 3 ways of background subtraction
# createBackgroundSubtractorMOG2 seems to give the best result. Need more testing.
fgbg = cv2.createBackgroundSubtractorMOG2()
#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
#fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('frame',fgmask)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
