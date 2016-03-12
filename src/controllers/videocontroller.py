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
    """
    A class for managing a traffic camera feed.
    Initializing will create itself a log file
    
    Provides the function runInfinite that can
    cycle through the frames of a stationary traffic
    camera feed and write the average number of cars
    detected over the Time Interval once at the end
    of every interval
    """
    def __init__(self, video_path):
        self.capture = cv2.VideoCapture(video_path)
        self.lc = LogController()
        self.fgbg = cv2.BackgroundSubtractorMOG()
        
 
    def runInfinite(self,tkroot=None):
        """
        A function that can take a TkHelperWindow and send
        it processed frames to display. The infinite loop is
        killed by the play button within the gui or EOF 
        """
        while(True):
            try:
                average = self._runInterval(tkroot)
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                
                self.lc.writeToLog(timestamp,average)                
                packet = "%s          %.1f" %(timestamp, average)
   
                if tkroot is not None:             
                    tkroot.addLog(packet)
                    #retrieve pause signal from button press in tk
                    # will only be caught after Time interval elapses
                    play = tkroot.runUpdate()
                    if not(play):
                        break
                #===============================================================
                # else:
                #     print(packet)
                #===============================================================
            except:
                break
        
    def _runInterval(self,tkroot):
        """
        A gui function that runs a 10 second interval
        and returns a computed average.
        
        Supplying tkroot will run calls to update the picture
        shown inside tkroot, an instance of TkWindowViewer
        Leaving it as null will just return the average which
        is faster and uses less space in memory
        """
        running_count = 0
        frames_run = 0
        timeout = time.time() + TIME_INTERVAL
        if tkroot is not None:      
            while time.time() < timeout:
                (frame,count) = self._runIteration(return_frame=True)
                #send frame to gui
                tkroot.setDisplayImg(frame)
                tkroot.runUpdate()
                running_count += count
                frames_run += 1
        else:
            while time.time() < timeout:
                count = self._runIteration()
                running_count += count
                frames_run += 1
        #compute average over interval
        interval_average = float(running_count) / float(frames_run)
        
        return interval_average
    
    
    def _runIteration(self, return_frame=False):
        """
        The function of the controller that processes
        the next frame of the video and calculates the number
        of vehicles. It only processes a single image and therefore
        must be called inside a loop like runinterval
        
        The flag return_frame can turned on to return the frame
        with the detected vehicles and a summary count drawn
        """
        flag,frame = self.capture.read()
        if not flag:
            raise Exception("Could not read video")        
        frame = imutils.resize(frame, width=500)
        # This is an alternative way. Simply just use BackgroundSubtractor.
        thresh = self.fgbg.apply(frame)
        thresh = cv2.blur(thresh,(11,11)) # blur the frame. this gives better result
        (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

        # for each contour if the area is greater the min_area,
        # treat it as a vehicle. Then draw a rectangle on it.
        count = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > MIN_AREA:
                if return_frame:
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                count += 1
        #cv2.imshow('thresh',thresh)
        
        if not(return_frame):
            return count
        
        cv2.putText(frame,"Count: %d" % count,(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)   
        return(frame, count)
    
    
    
    def stopVideo(self):
        self.capture.release()

        
            
        