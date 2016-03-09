"Ingrex praser deal with message"
import re
from datetime import datetime, timedelta

import pytz


class Message(object):
    "Message object"
    def __init__(self, raw_msg):
        self.raw = raw_msg
        self.guid = raw_msg[0]
        self.timestamp = raw_msg[1]
        seconds, millis = divmod(raw_msg[1], 1000)
        tz = pytz.timezone('Asia/Shanghai')
        time = datetime.fromtimestamp(seconds, tz) + timedelta(milliseconds=millis)
        self.time = time.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]
        self.text = raw_msg[2]['plext']['text']
        self.markup = raw_msg[2]['plext']['markup']
        self.player = "__ADA__"
        if self.markup:
            self.player = self.markup[0][1]['plain']
        self.markup = ''.join(str(e) for e in self.markup)
        # self.portal = self.markup[2]

        self.lat = "-1"
        self.lng = "-1"
        if re.findall(r'u\'latE6\': (\d*)', self.markup):
            self.lat = re.findall(r'u\'latE6\': (\d*)', self.markup)[0]
            self.lng = re.findall(r'u\'lngE6\': (\d*)', self.markup)[0]

        self.type = raw_msg[2]['plext']['plextType']
        self.team = raw_msg[2]['plext']['team']
