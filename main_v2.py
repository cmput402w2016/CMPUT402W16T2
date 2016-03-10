# This version uses BackgroundSubtractorMOG to identify the moving objects

import argparse
import numpy as np
import cv2
import imutils

#construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to the video file", required=True)
args = vars(ap.parse_args())
 
cap = cv2.VideoCapture(args["video"])

# Here are the 2 ways of background subtraction
fgbg = cv2.BackgroundSubtractorMOG2()


# The two points for drawing the line
#(pt1, pt2) = ((110,320), (460,220))

min_area = 500

while(1):

    # read the frames
    _,frame = cap.read()

    # resize the frame to width of 500px
    frame = imutils.resize(frame, width=500)

    # This is an alternative way. Simply just use BackgroundSubtractor.
    thresh = fgbg.apply(frame)
    thresh = cv2.blur(thresh,(11,11)) # blur the frame. this gives better result
    (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

    # draw the counting line
    #cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

    # for each contour if the area is greater the min_area,
    # treat it as a vehicle. Then draw a rectangle on it.
    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            count += 1

    cv2.putText(frame,"Count: %d" % count,(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)

    # Display the current number of vehicles
    cv2.putText(frame,"Count: %d" % count,(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)

    # Show it, if key pressed is 'Esc', exit the loop
    #cv2.imshow('thresh',thresh)
    cv2.imshow('frame',frame)
    if cv2.waitKey(33)== 27:
        break

# Clean up everything before leaving
cv2.destroyAllWindows()
cap.release()
