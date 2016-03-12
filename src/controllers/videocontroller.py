import datetime
import time

import cv2
import imutils
import numpy

from controllers.logcontroller import LogController
from models.frame import Frame

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
        self.fgbs = cv2.BackgroundSubtractorMOG()
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
        flag,img = self.capture.read()
        if not flag:
            raise Exception("Could not read video")        
        frame = Frame(img, self.fgbs)
        
        #determine if image should be returned
        if return_frame:
            return frame.drawCountVehicles()
        
        return frame.countVehicles()  
    
    
    def stopVideo(self):
        self.capture.release()

        
            
        