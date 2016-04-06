import json
import datetime
import time;
import os.path
import requests
import logging

import settings

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
    def __init__(self, world):

        fname = '%s.log' % datetime.datetime.now().strftime("%Y_%m_%d %H_%M_%S")
        self.world_dict = world
        #go up through controllers,src to log folder
        #try except
        base_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.filename = "%s/log/%s"%(base_folder,fname)
        try:
            with open(self.filename, 'w') as f:
                json.dump([], f)
        except:
            raise Exception("could not resolve log file path name")
            
    def writeToLog(self, timestamp, averages):
        
        with open(self.filename) as f:
            data = json.load(f)
        if (len(data) >= 100):
            data.pop()

        #k is the angle coordinates as the key in world, v is the average count
        for k,v in averages.iteritems():
            packet = self._createJSON(timestamp, k, v)
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
        """
        Writes a single packet to the team 1 server
        """
        pattern = settings.DATE_PATTERN 
        epoch = int(time.mktime(time.strptime(packet['time'], pattern)))
        url = settings.POST_URL
        data = {}
         
        data['from'] = packet['from']
        data['to'] = packet['to']
        data['key'] = "TESTING_POST"
        data['timestamp'] = epoch
        data['value'] = packet['count']
        r = requests.post(url, json=data)
        # logger.info(r.json())
        if (r.status_code == 201):
            return True
        else:
            return False

    def _createJSON(self, time, key, count):
        packet = {}
        packet['time'] = time
        packet['count'] = round(count, 1)
        from_coord, to_coord = self.world_dict.get(key).replace('(',"")\
            .replace(')',"").replace("'","").split(',')
        
        packet['from'] = from_coord
        packet['to'] = to_coord
        return packet

    def _getKey(self, item):
        return item['time']
