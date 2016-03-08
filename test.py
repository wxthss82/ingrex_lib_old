import ingrex
import datetime
import re
import sys
import time


class message:
    def __init__(self, time = "1989", user="__ADA__", team="RES", operation="Flipped", lng="-1", lat="-1"):
        self.time = time
        self.user = user
        self.team = team
        self.operation = operation
        self.lng = lng
        self.lat = lat

    def __str__(self):
        if self.lng != "-1":
            return '%s, %s, %s, %s, %s, %s'%(self.time, self.user, self.team, self.lng, self.lat, self.operation)
        else:
            return '%s, %s, %s, %s'%(self.time, self.user, self.team, self.operation)


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    "main function"
    field = {
        'minLngE6':115523545,
        'minLatE6':39418597,
        'maxLngE6':117005055,
        'maxLatE6':40404834,
    }
    with open('cookies') as cookies:
        cookies = cookies.read().strip()

    mints = -1;
    f = open('result.txt', 'w+')
    while True:
        intel = ingrex.Intel(cookies, field)
        result = intel.fetch_msg(mints=mints, tab='all')
        if result:
            mints = result[0][1] + 1
            # result = intel.fetch_map(['17_29630_13630_0_8_100'])
            # result = intel.fetch_portal(guid='ac8348883c8840f6a797bf9f4f22ce39.16')
            # result = intel.fetch_score()
            # result = intel.fetch_region()
            # result = intel.fetch_artifacts()
            messages = str(result).split('}}], ');
            for msg in messages:
                parts = str(msg).split(', ');
                date = datetime.datetime.fromtimestamp(int(parts[1]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                user = 'u'
                content = ""
                if re.findall(r'u\'plext\': \{u\'text\': u\'(.*?)\',', msg):
                    content = re.findall(r'u\'plext\': \{u\'text\': u\'(.*?)\',', msg)[0].decode('unicode-escape')
                team = re.findall(r'u\'team\': u\'(\w*)\'', msg)[0]
                mesg = message();
                if re.findall(r'u\'SENDER\', \{u\'plain\': u\'(\w*): \',', msg):
                    user = re.findall(r'u\'SENDER\', \{u\'plain\': u\'(\w*): \',', msg)[0]
                    mesg = message(date, user, team, content)
                if re.findall(r'u\'PLAYER\', \{u\'plain\': u\'(\w*)\',', msg):
                    user = re.findall(r'u\'PLAYER\', \{u\'plain\': u\'(\w*)\',', msg)[0]
                    # log
                    mesg = message(date, user, team, content)
                if re.findall(r'u\'latE6\': (\d*)', msg):
                    lat = re.findall(r'u\'latE6\': (\d*)', msg)[0]
                    lng = re.findall(r'u\'lngE6\': (\d*)', msg)[0]
                    mesg = message(date, user, team, content, lat, lng)

                f.writelines(str(mesg) + "\n")
            print(str(result).decode('unicode-escape'))
            time.sleep(10)

if __name__ == '__main__':
    main()
