import unittest
from src.controllers.logcontroller import LogController

class LogTestCase(unittest.TestCase):
    def setUp(self):
        self.lc = LogController()
               
    def tearDown(self):
        self.lc.dispose()
        self.lc = None
     
    def test_initialized_file(self):
        with open(self.lc.filename, 'r') as f:
            self.assertEqual(f.read(), "[]")
        
        
    def test_write(self):
        self.lc.writeToLog('12:00:00', 7)
        with open(self.lc.filename, 'r') as f:
            self.assertNotEqual(f.read(), "[]")
        
    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(LogTestCase('test_initialized_file'))
        suite.addTest(LogTestCase('test_write'))
        return suite