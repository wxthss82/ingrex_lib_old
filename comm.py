"COMM monitor"
import traceback
from pyvirtualdisplay import Display
import platform


import ingrex
import time
import sys
import sqlite3

from selenium import webdriver

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
        # 'minLngE6':72004000,
        # 'minLatE6':829300,
        # 'maxLngE6':137834700,
        # 'maxLatE6':55827100,
    }

    # start is used for retry when exception such as cookie expired occurs.
    start = 1

    while (start == 1):
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


            # Retrieve the agent info.
            with open('AgentInfo.txt') as f:
                lines = f.readlines()
            username = lines[0].replace("\n", "")
            password = lines[1].replace("\n", "")


            # create chrome driver
            # get the chrome webdriver:
            # https://sites.google.com/a/chromium.org/chromedriver/downloads
            driver = webdriver.Chrome(chromedriver)
            # driver = webdriver.PhantomJS();
            driver.set_window_size(1024, 768)
            driver.get('http://www.ingress.com/intel')
            # print driver.title

            # get the login page
            link = driver.find_elements_by_tag_name('a')[0].get_attribute('href')
            driver.get(link)

            # simulate manual login
            time.sleep(1)
            driver.find_element_by_id('Email').send_keys(username)
            driver.find_element_by_css_selector('#next').click()
            driver.set_page_load_timeout(20)
            time.sleep(1)
            driver.find_element_by_id('Passwd').send_keys(password)
            driver.find_element_by_css_selector('#signIn').click()
            driver.set_page_load_timeout(20)
            driver.set_script_timeout(20)
            # driver.find_element_by_id('gaia_loginform').submit()
            # time.sleep(25)

            # get the cookies
            cookie = driver.get_cookies()
            for i in range(0, 6):
                print(cookie[i]["value"])
            f = open('./cookies', 'w+')
            # for v in cookies:
            #     f.writelines(v)
            f.write('SACSID=')
            f.write(cookie[2]["value"])
            f.write('; csrftoken=')
            f.write(cookie[3]["value"])
            f.write('; ingress.intelmap.shflt=viz; ingress.intelmap.lat=40.0000000000000; ingress.intelmap.lng=120.00000000000000; ingress.intelmap.zoom=16')
            f.close()
        finally:
            # driver.close()
            if platform.system() == "Linux":
                display.stop()
            driver.quit()

        start = 0

        with open('cookies2') as cookies:
            cookies = cookies.read().strip()

        # create database
        conn = sqlite3.connect('test.db')

        print "Opened database successfully";

        conn.execute('''CREATE TABLE IF NOT EXISTS MESSAGE
               (GUID TEXT PRIMARY KEY     NOT NULL,
               TIME             TEXT      NOT NULL,
               PLAYER           TEXT      NOT NULL,
               TEAM             TEXT      NOT NULL,
               LAT              TEXT      NOT NULL,
               LNG              TEXT      NOT NULL,
               BODY             TEXT      NOT NULL);''')
        print "Table created successfully";

        mints = -1

        while True:
            try:
                intel = ingrex.Intel(cookies, field)
                result = intel.fetch_msg(mints)
                if result:
                    mints = result[0][1] + 1
                for item in result[::-1]:
                    message = ingrex.Message(item)
                    print(mints)
                    # print(u'{} {}'.format(message.time, message.text.decode('unicode-escape')))
                    # insert into database
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
                    start = 1
                    break

        conn.close()


if __name__ == '__main__':
    main()
