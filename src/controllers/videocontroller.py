import datetime
import time
import math
import cv2
import imutils
import numpy

from controllers.logcontroller import LogController
from models.frame import Frame
import settings


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
    def __init__(self, video_path, world):
        self.world = world
        self.capture = cv2.VideoCapture(video_path)
        self.lc = LogController(world)
        self.fgbs = cv2.BackgroundSubtractorMOG2(history=1000,
                                   varThreshold = 500,
                                   bShadowDetection = False)
        self.detector = self._buildBlobDetector()
        
    def runInfinite(self,tkroot=None):
        """
        Runs the video in sets of intervals computing and logging averages
        after TIME_INTERVAL seconds.
        """
        while(True):
            try:
                averages = self._runInterval()
                timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            
                if not settings.DEBUG:    
                    self.lc.writeToLog(timestamp,averages)                
                
   
                #===============================================================
                # if tkroot is not None:             
                #     tkroot.addLog(packet)
                #     #retrieve pause signal from button press in tk
                #     # will only be caught after Time interval elapses
                #     play = tkroot.runUpdate()
                #     if not(play):
                #         break
                #===============================================================

            except:
                break
        
    def _runInterval(self):
        """
        A gui function that runs a TIME_INTERVAL interval
        and returns a dictionary using the same keys as
        the command args in --world to provide the average
        count of traffic detected moving in the world directions
        """    

        frames_run = 0
        #reinitialize the traffic counts
        averages = {}
        for k in self.world.keys():
            averages[k] = 0
                
        previous_keypoints = None
        
        timeout = time.time() + TIME_INTERVAL

        while time.time() < timeout:
            iterDict = self._runIteration(previous_keypoints)
            
            
            previous_keypoints = iterDict['keypoints']
            averages_dict = iterDict['averages']
            frames_run += 1    
            for k,v in averages_dict.iteritems():
                averages[k] += v
           
        
        #compute average over interval
        for k in self.world.keys():
            averages[k] = math.ceil(averages[k] / float(frames_run))
        
        return averages
    
    
    def _runIteration(self, previous_keypoints, return_frame=False):
        """
        The function of the controller that processes
        the next frame of the video and calculates the number
        of vehicles. It only processes a single image and therefore
        must be called inside a loop like runinterval
        
        The flag return_frame can turned on to return the frame
        with the detected vehicles and a summary count drawn
        """

        frame = self._getFrame()

        keypoints, averages = frame.analyzeFrame(previous_keypoints, self.world)  
        
        return {'keypoints':keypoints, 'averages':averages}
    
    
    def _getFrame(self):
        flag,img = self.capture.read()
        if not flag:
            raise Exception("Could not read video")        
        frame = Frame(img, self.fgbs, self.detector)
        return frame
    
    def _buildBlobDetector(self):
        """
        creates a blob detector that can be used to identify the relevant
        blobs of a background subtracted image. Algorithm can be improved
        by supplying a truly empty frame to better remove noise.
        """
        params = cv2.SimpleBlobDetector_Params()
        
        params.filterByColor = True
        params.blobColor = 255
        params.filterByConvexity = True
        params.minConvexity = 0.87
        
        return cv2.SimpleBlobDetector(params)
    
    def stopVideo(self):
        self.capture.release()

        
            
        