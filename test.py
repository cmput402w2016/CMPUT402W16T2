import numpy as np
import cv2

# TODO: remove hard coded file name
cap = cv2.VideoCapture('videos/sample_video_3.mp4')

# Here are the 3 ways of background subtraction
# createBackgroundSubtractorMOG2 seems to give the best result. Need more testing.
fgbg = cv2.BackgroundSubtractorMOG2(history=1000,
                                   varThreshold = 500,
                                   bShadowDetection = False)
#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
#fgbg = cv2.bgsegm.createBackgroundSubtractorGMG()

while(1):
    ret, frame = cap.read()
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.equalizeHist(frame)

    fgmask = fgbg.apply(frame)
    fgmask = cv2.blur(fgmask, (10,10))
    ret,fgmask =cv2.threshold(fgmask, 150, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    params = cv2.SimpleBlobDetector_Params()
    
    params.filterByColor = True
    params.blobColor = 255
    params.filterByConvexity = True
    params.minConvexity = 0.87
    
    
    detector = cv2.SimpleBlobDetector(params)
    keypoints = detector.detect(fgmask)
    count = len(keypoints)
    im_with_keypoints = cv2.drawKeypoints(fgmask, keypoints,np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.putText(im_with_keypoints ,"Count: %d" % count,(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2) 


    cv2.imshow('frame',frame)
    cv2.imshow('orig', im_with_keypoints)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
    
    
