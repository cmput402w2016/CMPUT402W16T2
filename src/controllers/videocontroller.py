import cv2
import time
import imutils
import numpy

TIME_INTERVAL = 10
MIN_AREA = 500

class VideoController:
    def __init__(self, video_path):
        self.capture = cv2.VideoCapture(video_path)
        self.running_average = 0
        self.fgbg = cv2.BackgroundSubtractorMOG2()
        
    def runInfinite(self,tkroot):
        while(True):
            try:
                (frame,count) = self.runIteration()
                tkroot.setDisplayImg(frame)
                play = tkroot.runUpdate()
                if not(play):
                    break
            except:
                break
        
    def runInterval(self):
        pass
    
    def runIteration(self):
        flag,frame = self.capture.read()
        return (frame, flag)
        if not flag:
            raise Exception("Could not read video")
        
        frame = imutils.resize(frame, width=500)

        # This is an alternative way. Simply just use BackgroundSubtractor.
        thresh = self.fgbg.apply(frame)
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
            if area > MIN_AREA:
                (x, y, w, h) = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                count += 1
    
       
        # Display the current number of vehicles in red
        cv2.putText(img=frame,text="Count: %d" % count,org=(10,20),fontFace=cv2.FONT_HERSHEY_SIMPLEX,fontScale= 0.5,color=(0,0,255),thickness=2)
        cv2.imshow('',frame)
        
        return(frame, count)
    
    def stopVideo(self):
        self.capture.release()
        
    def resetAverage(self):
        self.running_average = 0
        
            
        