"COMM monitor"
import traceback
from pyvirtualdisplay import Display
import platform

import ingrex
import time
import sys

import sqlite3
import MySQLdb

from selenium import webdriver


def main():
    "main function"
    reload(sys)
    sys.setdefaultencoding('utf-8')
    region = {
        #  Beijing Region
        'minLngE6': 115523545,
        'minLatE6': 39418597,
        'maxLngE6': 117005055,
        'maxLatE6': 40404834,
        #  China Region
        # 'minLngE6':72004000,
        # 'minLatE6':829300,
        # 'maxLngE6':137834700,
        # 'maxLatE6':55827100,
    }

    while True:
        try:
            # for virtual display, used for the system which doesn't have user interface.
            # print platform.system()
            if platform.system() == "Linux":
                display = Display(visible=0, size=(800, 600))
                display.start()

            # used for generate debug log
            chromedriver = ""
            if platform.system() == "Windows":
                chromedriver = "./chromedriver_win32.exe"
            elif platform.system() == "Linux":
                chromedriver = "./chromedriver_linux64"
            elif platform.system() == "Darwin":
                chromedriver = "./chromedriver_mac32"
            print platform.system()

            # Retrieve the agent info.
            with open('secrets.txt') as f:
                lines = f.readlines()
            username = lines[0].replace("\n", "")
            password = lines[1].replace("\n", "")

            # create chrome driver
            # get the chrome webdriver:
            # https://sites.google.com/a/chromium.org/chromedriver/downloads
            print chromedriver
            # service_log_path = "{}/chromedriver.log".format(".")
            # service_args = ['--verbose']
            # driver = webdriver.Chrome("./chromedriver_linux64")
            # driver = webdriver.Chrome(chromedriver,
            #                           service_args=service_args,
            #
            #                            service_log_path=service_log_path)
            # driver = webdriver.PhantomJS()
            # if platform.system == "Darwin":
            # driver = webdriver.PhantomJS()
            # elif platform.system == "Linux":
            driver = webdriver.PhantomJS("./phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
            driver.set_window_size(1024, 768)
            driver.get('http://www.ingress.com/intel')
            print driver.title

            # get the login page
            link = driver.find_elements_by_tag_name('a')[0].get_attribute('href')
            driver.get(link)

            # simulate manual login
            time.sleep(1)
            driver.find_element_by_id('Email').send_keys(username)
            driver.find_element_by_css_selector('#next').click()
            driver.set_page_load_timeout(20)
            time.sleep(2)
            driver.find_element_by_id('Passwd').send_keys(password)
            driver.find_element_by_css_selector('#signIn').click()

            driver.set_page_load_timeout(20)
            driver.set_script_timeout(20)
            # driver.find_element_by_id('gaia_loginform').submit()
            # time.sleep(5)

            # get the cookies
            cookie = driver.get_cookies()
            for c in cookie:
                print(c["value"])
                if len(c["value"]) > 200:
                    SACSID = c["value"]
                if len(c["value"]) == 32:
                    csrftoken = c["value"]
            f = open('./cookies', 'w+')
            # for v in cookies:
            #     f.writelines(v)
            f.write('SACSID=')
            # note: the cookie[2],[3] index number various between different browser.
            f.write(SACSID)
            f.write('; csrftoken=')
            f.write(csrftoken)
            f.write(
                '; ingress.intelmap.shflt=viz; ingress.intelmap.lat=40.0000000000000; ingress.intelmap.lng=120.00000000000000; ingress.intelmap.zoom=16')
            f.close()
        finally:
            # driver.close()
            print "exception"
            if platform.system() == "Linux":
                display.stop()
            driver.quit()

        with open('cookies') as cookies:
            cookies = cookies.read().strip()

        # Open database connection
        db = MySQLdb.connect(host="ingrex-lib.cbxixqiqoaj0.ap-northeast-1.rds.amazonaws.com", user="wangxin",
                             passwd="tsinghua", db="ingrex",  charset="utf8mb4")
        # prepare a cursor object using cursor() method
        db.set_character_set('utf8')

        cursor = db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        print "Opened database successfully";

        cursor.execute('''CREATE TABLE IF NOT EXISTS `message` (
                `guid` varchar(32) NOT NULL,
                `time` datetime NULL,
                `player` varchar(32) NULL,
                `team` varchar(32) NULL,
                `portalname` varchar(100) NULL,
                `portaladdress` varchar(100) NULL,
                `lat` int(11) NULL,
                `lng` int(11) NULL,
                `message` varchar(255) NULL,
                PRIMARY KEY (`guid`)
            ) ENGINE=InnoDB
            DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;
      ''')

        mints = -1

        while True:
            try:
                intel = ingrex.Intel(cookies, region)
                result = intel.fetch_msg(mints)
                if result:
                    mints = result[0][1] + 1
                for item in result[::-1]:
                    message = ingrex.Message(item)
                    print(mints)
                    # print(u'{} {}'.format(message.time, message.text.decode('unicode-escape')))
                    # insert into database
                    print message.portalname
                    cursor.execute("INSERT INTO message (guid,time,player,team,portalname,portaladdress,lat,lng,message) \
                                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (message.guid,
                                                                  message.time.strftime('%Y-%m-%d %H:%M:%S.%f'),
                                                                  str(message.player).decode('unicode-escape'),
                                                                  str(message.team).decode('unicode-escape'),
                                                                  message.portalname,
                                                                  str(message.portaladdress).decode('unicode-escape'),
                                                                  message.lat,
                                                                  message.lng,
                                                                  str(message.text).decode('unicode-escape')));
                    db.commit()

                time.sleep(2)
            except Exception, err:
                try:
                    exc_info = sys.exc_info()

                    try:
                        raise TypeError("Again !?!")
                    except:
                        pass

                finally:
                    traceback.print_exception(*exc_info)
                    del exc_info
                    break
                    db.close()




if __name__ == '__main__':
    main()
