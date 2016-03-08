"COMM monitor"
import ingrex
import time
import sys
import sqlite3

def main():
    "main function"
    reload(sys)
    sys.setdefaultencoding('utf-8')
    field = {
        # 'minLngE6':116298171,
        # 'minLatE6':39986831,
        # 'maxLngE6':116311303,
        # 'maxLatE6':39990941,
        'minLngE6':115523545,
        'minLatE6':39418597,
        'maxLngE6':117005055,
        'maxLatE6':40404834,
    }
    with open('cookies') as cookies:
        cookies = cookies.read().strip()

    conn = sqlite3.connect('test.db')


    print "Opened database successfully";

    conn.execute('''CREATE TABLE IF NOT EXISTS MESSAGE
           (GUID TEXT PRIMARY KEY     NOT NULL,
           TIME           TEXT    NOT NULL,
           PLAYER           TEXT    NOT NULL,
           TEAM           TEXT    NOT NULL,
           LAT           TEXT    NOT NULL,
           LNG           TEXT    NOT NULL,
           BODY           TEXT    NOT NULL);''')
    print "Table created successfully";

    mints = -1

    id = 1
    while True:
        intel = ingrex.Intel(cookies, field)
        result = intel.fetch_msg(mints)
        if result:
            mints = result[0][1] + 1
        for item in result[::-1]:
            message = ingrex.Message(item)
            print(u'{} {}'.format(message.time, message.text.decode('unicode-escape')))
            conn.execute("INSERT INTO MESSAGE (GUID,TIME,PLAYER,TEAM,LAT,LNG,BODY) \
                         VALUES (?,?,?,?,?,?,?);""", (message.guid,
                                                    message.time,
                                                    message.player,
                                                    message.team,
                                                    message.lat,
                                                    message.lng,
                                                    message.text));
            conn.commit()
            print "Records created successfully";

        time.sleep(10)
    conn.close()

if __name__ == '__main__':
    main()
