import json
import datetime
import time;
import os.path
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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

    def writeToLog(self, timestamp, count):

        with open(self.filename) as f:
            data = json.load(f)
        if (len(data) >= 100):
            data.pop()

        # re-post the most recent 5 packets if previously failed to post
        for i in range(0, min(5, len(data))):
            # logger.info(data[i])
            if data[i]['success'] == 0:
                if ( self._postToServer(data[i]) ):
                    data[i]['success'] = 1

        packet = self._createJSON(timestamp,count)
        if ( self._postToServer(packet) ):
            packet['success'] = 1
        else:
            packet['success'] = 0
        data.append(packet)

        data.sort(key=self._getKey, reverse=True)

        with open(self.filename, 'w') as f:
            json.dump(data, f)

        return packet

    def _postToServer(self, packet):
        # TODO: 'from' & 'to' should not be hardcoded here
        pattern = '%Y/%m/%d %H:%M:%S' # the pattern should be the same as the one on videocontroller.py
        epoch = int(time.mktime(time.strptime(packet['time'], pattern)))
        url = "http://199.116.235.225:8000/traffic"
        data = {}
        data['from'] = "c3x2wb3240dw"   # TODO
        data['to'] = "c3x2wb331v77"     # TODO
        data['key'] = "TESTING_POST"    # TODO
        data['timestamp'] = epoch
        data['value'] = packet['count']
        try:
            r = requests.post(url, json=data, timeout=5)
            if (r.status_code == 201):
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            logger.info(e)
            return False

    def _createJSON(self, time, count):
        packet = {}
        packet['time'] = time
        packet['count'] = round(count, 1)
        return packet

    def _getKey(self, item):
        return item['time']
