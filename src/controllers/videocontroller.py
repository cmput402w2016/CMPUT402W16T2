import time
import datetime

import cv2
import imutils
import numpy

from src.controllers.logcontroller import LogController

#the run interval before logging in seconds
TIME_INTERVAL = 5
MIN_AREA = 500

class VideoController:
    def __init__(self, video_path):
        self.capture = cv2.VideoCapture(video_path)
        self.running_average = 0
        self.lc = LogController()
        self.fgbg = cv2.BackgroundSubtractorMOG()
        
    def runInfinite(self,tkroot):
        """
        A function that can take a TkHelperWindow and send
        it processed frames to display. The infinite loop is
        killed by the play button within the gui or EOF 
        """
        while(True):
            try:
                average = self.runInterval(tkroot)
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                
                self.lc.writeToLog(timestamp,average)                
                packet = timestamp + " "*10 + str(average)
                tkroot.addLog(packet)
                
                #retrieve pause signal from button press in tk
                # will only be caught after Time interval elapses
                play = tkroot.runUpdate()
                if not(play):
                    break
            except:
                break
        
    def runInterval(self,tkroot):
        """
        A gui function that runs a 10 second interval
        and returns a computed average while updating the gui root
        """
        running_count = 0
        frames_run = 0
        timeout = time.time() + TIME_INTERVAL
        while time.time() < timeout:
            (frame,count) = self.runIteration()
            #send frame to gui
            tkroot.setDisplayImg(frame)
            tkroot.runUpdate()

            running_count += count
            frames_run += 1
        #compute average over interval
        interval_average = running_count // frames_run
        
        return interval_average
    
    
    def runIteration(self):
        flag,frame = self.capture.read()
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
        #cv2.imshow('thresh',thresh)
        
        cv2.putText(frame,"Count: %d" % count,(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)

            
        return(frame, count)
    
    def stopVideo(self):
        self.capture.release()
        
    def resetAverage(self):
        self.running_average = 0
        
            
        