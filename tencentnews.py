import re

import requests
import sqlite3

import sys
import time


def main():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    conn = sqlite3.connect('jb_comment.db')

    print "Opened database successfully";

    conn.execute('''CREATE TABLE IF NOT EXISTS COMMENT
           (
           TIME             TEXT      NOT NULL,
           BODY             TEXT      NOT NULL);''')


    total = 14685
    itemsize = 50
    count = total / itemsize + 1
    commentid = 6051534826578202268
    while count >= 0:
        url = 'http://coral.qq.com/article/1199666503/comment?commentid=' + str(commentid) + '&reqnum=20&tag=&callback=mainComment&_=1459746007848'
        headers =   {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding":"gzip, deflate, sdch",
                    "Accept-Language":"en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
                    "Connection":"keep-alive",
                    "Cookie":"mobileUV=1_152ab8c96f5_45cee; pgv_pvi=8127301632; RK=HXOrmxNjW/; luin=o0498030032; lskey=00010000a3d78ebcb12e046ca7704f058684557eeade781286e246510541f1a3deda6b72efa3524ea21b95d6; ptui_loginuin=498030032; g_tk=fcdc8622cfbb22b5fb2ee6511dec7361da6b9bce; pgv_si=s9783511040; ptisp=cnc; ptcz=8e7943f980a06fc06e016134aefe6a0ce8af9620bf89efd291057b7e88acab95; pt2gguin=o0498030032; uin=o0498030032; skey=@nGQxDLaBp; uid=66753503; ad_play_index=81; pgv_info=ssid=s5135312156; ts_last=coral.qq.com/1199666503; ts_refer=www.qq.com/coral/coralBeta3/coralMainDom3.0.htm; pgv_pvid=2325485768; o_cookie=498030032; ts_uid=7546137060",
                    "Host":"coral.qq.com",
                    "Upgrade-Insecure-Requests":"1",
                    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
                     }

        body = requests.get(url, headers=headers)
        html = body.text
        commentid = re.findall("\"last\":\"(.*?)\"", html)
        commentid = str(commentid).replace('[u\'', '').replace('\']', '')
        comment = re.findall("\"content\":\"(.*?)\"", html)
        time2 = re.findall("\"timeDifference\":\"(.*?)\"", html)
        for i in range(0, len(comment)):
            comm = str(comment[i]).decode('unicode-escape')
            tim = str(time2[i]).decode('unicode-escape')
            print comm
            print tim
            conn.execute("INSERT INTO COMMENT (TIME, BODY) \
                         VALUES (?, ?);""", (tim, comm));
        conn.commit()
        print commentid
        print html
        time.sleep(2)
    conn.close()

if __name__ == '__main__':
    main()
