# This version uses first frame as a reference and then cv2.absdiff(firstFrame, gray)
# to find the difference.

import argparse
import numpy as np
import cv2
import imutils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, help="path to the video file", required=True)
args = vars(ap.parse_args())

cap = cv2.VideoCapture(args["video"])

firstFrame = None

# The two points for drawing the line
# (pt1, pt2) = ((110,320), (460,220))
min_area = 200

while(1):

    # read the frames
    _,frame = cap.read()

    # resize the frame to width of 500px
    frame = imutils.resize(frame, width=500)

    # convert frame to gray color and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # check if current frame is the first one
    if firstFrame is None:
		firstFrame = gray
		continue

    # find the difference between current frame and the first frame
    frameDelta = cv2.absdiff(firstFrame, gray)

    # get the contours of moving vehicles
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    try:
        (_, contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
    except:
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
