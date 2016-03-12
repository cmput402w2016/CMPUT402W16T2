import json
import datetime
import os.path

class LogController:
    """
    One log Controller is instantiated in the constructor of each
    video controller.
    
    The log controller builds JSON packets of data that it appends
    to a JSON dump it holds a reference to while it is being written.
    
    Every time the data is dumped, it is sorted by time so that it
    remains in the order it was written
    """
    def __init__(self):
        
        fname = '%s.log' % datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")
        #go up through controllers,src to log folder
        base_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.filename = "%s/log/%s"%(base_folder,fname)
        with open(self.filename, 'w') as f:
            json.dump([], f)

    def createJSON(self, t, c):
        j = {}
        j['time'] = t
        j['count'] = c
        return j

    def writeToLog(self, timestamp, count):
        
        with open(self.filename) as f:
            data = json.load(f)
        if (len(data) >= 100):
            data.pop()
            
        packet = self.createJSON(timestamp,count)
        #data.append(self.createJSON(timestamp,count))
        data.append(packet)

        data.sort(key=self.getKey, reverse=True)

        with open(self.filename, 'w') as f:
            json.dump(data, f)
        
        return packet

    def getKey(self, item):
        return item['time']
