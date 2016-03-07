import argparse
import numpy as np
import cv2
import imutils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to the video file", required=True)
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["video"])

# Here are the 3 ways of background subtraction
#fgbg = cv2.BackgroundSubtractorMOG2()
fgbg = cv2.BackgroundSubtractorMOG()
#fgbg = cv2.BackgroundSubtractorGMG()

# The two points for drawing the line
(pt1, pt2) = ((110,320), (460,220))

count = 0

while(1):

    # read the frames
    _,frame = cap.read()

    frame = imutils.resize(frame, width=500)

    # smooth it
    # frame = cv2.blur(frame,(41,41))

    # convert to hsv and find range of colors
    # hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # thresh = cv2.inRange(hsv,np.array((0, 80, 80)), np.array((20, 255, 255)))
    # thresh2 = thresh.copy()

    # This is an alternative way. Simply just use BackgroundSubtractor.
    thresh = fgbg.apply(frame)
    thresh = cv2.blur(thresh,(11,11))
    (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

    # find contours in the threshold image
    #contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    #cv2.line(frame, pt1, pt2, (0, 255, 0), 2)
    count = 0

    # finding contour with maximum area and store it as best_cnt
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            count += 1

    cv2.putText(frame,"Count: %d" % count,(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)

    # Show it, if key pressed is 'Esc', exit the loop
    cv2.imshow('frame',frame)
    #cv2.imshow('thresh',thresh)
    if cv2.waitKey(33)== 27:
        break

# Clean up everything before leaving
cv2.destroyAllWindows()
cap.release()
