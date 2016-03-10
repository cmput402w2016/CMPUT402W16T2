import json
import datetime

class LogController:
    def __init__(self):
        self.file = open('log/%s.log' % datetime.datetime.now(), 'w')

    def createJSON(self, t, c):
        data = {}
        data['time'] = t
        data['count'] = c
        return json.dumps(data)

    def writeToLog(self, timestamp, count):
        with self.file as f:
            f.write(self.createJSON(timestamp, count))
