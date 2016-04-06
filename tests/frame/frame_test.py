import unittest

import cv2

import numpy as np
from src.models.frame import Frame


class FrameTestCase(unittest.TestCase):
    def setUp(self):
        image1 = cv2.imread('3cars.jpg')
        image2 = cv2.imread('0cars.JPG')
        fgbs = cv2.BackgroundSubtractorMOG()
        params = cv2.SimpleBlobDetector_Params()
        params.filterByColor = True
        params.blobColor = 255
        params.filterByConvexity = True
        params.minConvexity = 0.87
        
        detector = cv2.SimpleBlobDetector(params)
        self.frame = Frame(image1, fgbs, detector)
        self.frame2 = Frame(image2, fgbs, detector)
        worldarg = "0;180=c3x2wb3240dw;c3x2wb331v77,180;360=c3x2wb331v77;c3x2wb3240dw"
        world = {}
        worldargs = worldarg.split(",")
        for data in worldargs:
            angles,coords = data.split("=")
            world[str(tuple(angles.split(';')))] = str(tuple(coords.split(';')))
        self.world = world
        
    def tearDown(self):
        self.frame.dispose()
        self.frame = None
        
        
    def test_count_vehicles(self):  
        keypoints,_ = self.frame.analyzeFrame(None, self.world)
        self.assertAlmostEqual(len(keypoints),3, delta=1)
        
    def test_count_no_vehicles(self):
        keypoints,_ = self.frame2.analyzeFrame(None, self.world)
        self.assertAlmostEqual(len(keypoints),0, delta=1)    
                               
    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(FrameTestCase('test_count_vehicles'))
        return suite