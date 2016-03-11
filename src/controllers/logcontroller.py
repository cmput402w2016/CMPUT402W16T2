import json
import datetime

class LogController:
    def __init__(self):
        self.filename = 'log/%s.log' % datetime.datetime.now()
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
            
        data.append(self.createJSON(timestamp, count))

        data.sort(key=self.getKey, reverse=True)

        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def getKey(self, item):
        return item['time']
