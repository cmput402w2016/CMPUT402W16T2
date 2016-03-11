import json
import datetime
import os.path

class LogController:
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
