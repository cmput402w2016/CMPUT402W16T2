import math

import cv2
import imutils

import numpy as np
import settings


MIN_AREA = 500

class Frame():
    """
    Takes a given image with a background subtractor and provides
    all the functions required to count the vehicles in the frame
    for the CLI or drawCountVehicles can be called for the GUI
    that returns a marked up image with cars highlighted and a count
    displayed.
    """
    def __init__(self, img, background_subtractor, blob_detector):
        #blob detector is passed in so it is not recreated for each frame
        
        # still unsure if reducing resolution aids in image identification
        image = imutils.resize(img, width=500)
        
        self.image = img
        self.fgbs = background_subtractor
        self.detector = blob_detector
        self.subtracted = self._subtractImage()
        
   
    def _subtractImage(self):
        """
        Increases contrast with histogram equalization and then applies
        the background subtractor using a heavy blurring filter to merge vehicles
        into a single detectable blob. Image thesholding is then applied using
        Otsu to autocalculate the binary image
        """
        sub = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        sub = cv2.equalizeHist(sub)
        sub = self.fgbs.apply(sub)
        sub = cv2.blur(sub,(20,20)) # blur the frame. this gives better result
        _, sub = cv2.threshold(sub, 150, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        thresh, sub = cv2.threshold(sub, 150, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return sub
    
    def analyzeFrame(self, old_keypoints, world):
        """
        The primary class function. Given the parsed world coordinates from the command line,
        the old_keypoints that the previous frame passed to run_Interval, and the new image,
        the function first detects new keypoints. Then for each point it determines if there
        is another pixel within the proximity that it belongs to the same vehicle. If it
        can detect such a point, it calculates the trajectory, and increments the world_direction
        count accordingly. Keypoints that cannot be trajectoried are evenly distributed among
        the average counts so that the overall counts can still be meaningfully divided by the
        number of frames.
        """
        averages_dict = {}
        for k in world.keys():
            averages_dict[k] = 0
        
        def sortInWorld(angle, world):
            """
            given an angle, decomposes the world coordinates to increment the proper value of the dictionary
            """
            for k in world.keys():
                anglerange = k.replace('(',"").replace(")","").\
                    replace("'","").split(',')
                min = int(anglerange[0])
                max = int(anglerange[1])
                if (min <= angle) and (angle < max):
                    averages_dict[k] += 1
        
        count = 0
        keypoints = self.detector.detect(self.subtracted)
        lines = []
        
        if (old_keypoints is not None) and len(old_keypoints):
            #Not all keypoints will have a direction, in this case, they
            # are randomly distributed to all gropus 
            freeze_keys = world.keys()
            key_cycler = 0
            for kp in keypoints:
                parray = np.array([k.pt for k in old_keypoints])
                p0 = np.array(kp.pt)          
                old_point = self.find_nearest(parray, kp.pt)
                #if the keypoint can be associated with an already detected
                #vehicle, detect its motion and sort it into the averages count
                dist = np.linalg.norm(p0-old_point)
                #do not track stationary vehicles
                if (dist > settings.MIN_DIST) and (dist < settings.MAX_DIST):
                    angle = self.angle_between(old_point,p0)
                    sortInWorld(angle, world)
                    lines.append([(int(old_point[0]),int(old_point[1])),
                                  (int(p0[0]), int(p0[1])), round(angle, 0)])
                else:
                    key = freeze_keys[key_cycler]
                    averages_dict[key] += 1
                    key_cycler = (key_cycler + 1) % len(freeze_keys)
        if settings.DEBUG:
            im_with_keypoints = cv2.drawKeypoints(self.subtracted, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)        
            #=======================================================================
            # cv2.putText(im_with_keypoints ,"Count: %d" % len(),(10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2) 
            # cv2.imshow('keypoints', im_with_keypoints)
            #=======================================================================
            for l in lines:
                cv2.line(im_with_keypoints, l[0],l[1], (0,255,0), 3 )
                #write the angle next to the end point of the line
                cv2.putText(im_with_keypoints, str(l[2]), l[1], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100,100,100),2)
            
            
            cv2.imshow("keypoints", im_with_keypoints)
            cv2.waitKey(0)
        
        
        return (keypoints, averages_dict)
    
    #===========================================================================
    # def _getContours(self):
    #     # Applies contouring to subtracted image to identify areas of interest
    #     thresh = cv2.blur(self.subtracted,(20,20)) # blur the frame. this gives better result
    #     _, thresh = cv2.threshold(self.subtracted, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #     (contours, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    #         cv2.CHAIN_APPROX_SIMPLE)
    #     return contours
    #===========================================================================
    
    def find_nearest(self, points, coord):
        """Element in nd array `points` closest to the scalar value coord.
        Assumes that points is a non-empty list
        """
        p = points[np.sum(np.square(np.abs(points-coord)),1).argmin()]
        return p
    
    def angle_between(self, p1, p2):
        """
        calculates the trajectory of 2 points from p1 to p2
        recalculates with 0 as it is on unit circle and in deg
        """
        deltax = p2[1] - p1[1]
        deltay = p2[0] - p1[0]
        trajectory = math.atan2(deltay, deltax) * 180/np.pi
        trajectory = (trajectory - 90) % 360
        return trajectory