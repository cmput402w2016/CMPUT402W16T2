import json
import datetime

class LogController:
    def __init__(self):
        self.filename = 'log/%s.log' % datetime.datetime.now()
        with open(self.filename, 'w') as f:
            json.dump({}, f)
        self.count = -1

    def createJSON(self, t, c):
        data = {}
        data['time'] = t
        data['count'] = c
        return {self.count:data}

    def writeToLog(self, timestamp, count):
        self.count += 1

        with open(self.filename) as f:
            data = json.load(f)

        data.update(self.createJSON(timestamp, count))

        with open(self.filename, 'w') as f:
            json.dump(data, f)
