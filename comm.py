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
                             passwd="tsinghua", db="ingrex",  charset="utf8")
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        print "Opened database successfully";

        cursor.execute('''CREATE TABLE IF NOT EXISTS MESSAGE
            (
                GUID TEXT NOT NULL,
                TIME DATETIME NOT NULL,
                PLAYER TINYTEXT NOT NULL,
                TEAM TINYTEXT NOT NULL,
                PORTALNAME TINYTEXT NOT NULL,
                PORTALADDRESS TINYTEXT NOT NULL,
                LAT MEDIUMTEXT NOT NULL,
                LNG MEDIUMTEXT NOT NULL,
                BODY TEXT NOT NULL
            );''')

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
                    cursor.execute("INSERT INTO MESSAGE (GUID) \
                                 VALUES (%s)", (message.guid
                                                                  ));
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
