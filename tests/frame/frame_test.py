import unittest

import cv2

import numpy as np
from src.models.frame import Frame


class FrameTestCase(unittest.TestCase):
    def setUp(self):
        image = cv2.imread('3cars.jpg')
        fgbs = cv2.BackgroundSubtractorMOG()
        self.frame = Frame(image, fgbs)
        
    def tearDown(self):
        self.frame.dispose()
        self.frame = None
        
        
    def test_count_vehicles(self):
        self.assertAlmostEqual(self.frame.countVehicles(),
                                3,
                                delta=1)
        
    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(FrameTestCase('test_count_vehicles'))
        return suite