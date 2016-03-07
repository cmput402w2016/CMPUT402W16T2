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
(pt1, pt2) = ((110,320), (460,220))

while(1):

    # read the frames
    _,frame = cap.read()

    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (31, 31), 0)
    if firstFrame is None:
		firstFrame = gray
		continue

    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 0:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)


    # Show it, if key pressed is 'Esc', exit the loop
    cv2.imshow('thresh',thresh)
    cv2.imshow('frame',frame)
    if cv2.waitKey(33)== 27:
        break

# Clean up everything before leaving
cv2.destroyAllWindows()
cap.release()
