import unittest
from src.controllers.logcontroller import LogController

class LogTestCase(unittest.TestCase):
    def setUp(self):
        worldarg = "0;180=c3x2wb3240dw;c3x2wb331v77,180;360=c3x2wb331v77;c3x2wb3240dw"
        world = {}
        worldargs = worldarg.split(",")
        for data in worldargs:
            angles,coords = data.split("=")
            world[str(tuple(angles.split(';')))] = str(tuple(coords.split(';')))
        self.lc = LogController(world)
               
    def tearDown(self):
        self.lc.dispose()
        self.lc = None
     
    def test_initialized_file(self):
        with open(self.lc.filename, 'r') as f:
            self.assertEqual(f.read(), "[]")
        
        
    def test_write(self):
        self.lc.writeToLog('12:00:00', {"('0','180')":5.0,"('180','360')":1.0})
        with open(self.lc.filename, 'r') as f:
            self.assertEqual(f.read(), '[{"count": 5.0, "to": " c3x2wb331v77", "from": "c3x2wb3240dw", "success": 1, "time": "12:00:00"}, {"count": 1.0, "to": " c3x2wb3240dw", "from": "c3x2wb331v77", "success": 1, "time": "12:00:00"}')
        
    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(LogTestCase('test_initialized_file'))
        suite.addTest(LogTestCase('test_write'))
        return suite