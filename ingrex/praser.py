"Ingrex praser deal with message"
import re
from datetime import datetime, timedelta

import pytz


class Message(object):
    "Message object"
    def __init__(self, raw_msg):
        try:
            self.raw = raw_msg
            self.guid = raw_msg[0]
            self.timestamp = raw_msg[1]
            seconds, millis = divmod(raw_msg[1], 1000)
            tz = pytz.timezone('Asia/Shanghai')
            time = datetime.fromtimestamp(seconds, tz) + timedelta(milliseconds=millis)
            # print raw_msg
            self.time = time.strftime('%Y/%m/%d %H:%M:%S:%f')[:-3]
            self.text = raw_msg[2]['plext']['text']
            self.markup = raw_msg[2]['plext']['markup']
            self.team = ""
            self.player = ""
            if str(self.text).startswith("[secure]"):
                self.player = self.markup[1][1]['plain'].replace(":", "")
                self.team = self.markup[1][1]['team']
            self.player = self.markup[0][1]['plain'].replace(":", "")
            self.team = self.markup[0][1]['team']
            self.markup = ''.join(str(e) for e in self.markup)
            # self.portal = self.markup[2]

            self.lat = "-1"
            self.lng = "-1"
            self.portal = ""
            self.portalname = ""
            self.portaladdress = ""
            if re.findall(r'u\'latE6\': (\d*)', self.markup):
                self.lat = re.findall(r'u\'latE6\': (\d*)', self.markup)[0]
                self.lng = re.findall(r'u\'lngE6\': (\d*)', self.markup)[0]
                self.portal = Portal(raw_msg[2]['plext']['markup'][2][1])
                self.portalname = self.portal.name
                self.portaladdress = self.portal.address
        except Exception:
            print raw_msg


class Portal(object):
    def __init__(self, raw_portal):
        self.address = raw_portal['address']
        self.latE6 = raw_portal['latE6']
        self.lngE6 = raw_portal['lngE6']
        self.name = raw_portal['name']
        self.plain = raw_portal['plain']
        self.team = raw_portal['team']

class Link(object):
    def __init__(self, markup):
        self.text = markup[1]  # create or destory
        self.portalfrom = Portal(markup[2])
        self.portalto = Portal(markup[4])

class Field(object):
    def __init__(self, markup):
        self.text = markup[1] # create or destory
        self.portalat = Portal(markup[2])
        self.crease = markup[3]
        self.amount = markup[4]
        self.unit = markup[5]




