"COMM monitor"
import traceback
from pyvirtualdisplay import Display


import ingrex
import time
import sys
import sqlite3

from selenium import webdriver

def main():
    "main function"
    reload(sys)
    sys.setdefaultencoding('utf-8')


    #get the chrome webdriver:
    #https://sites.google.com/a/chromium.org/chromedriver/downloads
    display = Display(visible=0, size=(400, 300))
    display.start()
    service_log_path = "{}/chromedriver.log".format(".")
    service_args = ['--verbose']
    i = 1
    while (i <= 44):
        driver = webdriver.Chrome("./chromedriver_mac32",
        service_args=service_args,
        service_log_path=service_log_path)
        # driver = webdriver.PhantomJS();
        driver.set_window_size(1024, 768)
        driver.get('http://order.mi.com/site/login?redirectUrl=http://item.mi.com/buyphone/mi5')
        print driver.title
        # time.sleep(1)
        driver.find_element_by_id('username').send_keys("wx_1989518" + str(i) + "@163.com")
        driver.find_element_by_id('pwd').send_keys("abc123")
        driver.save_screenshot('./shot.png')
        # time.sleep(1)
        driver.find_element_by_id("login-button").click()
        driver.set_page_load_timeout(20)
        driver.set_script_timeout(20)
        # driver.find_element_by_id('gaia_loginform').submit()
        # time.sleep(5)
        driver.save_screenshot('./shot3.png')
        if driver.find_elements_by_class_name("J_stepItem"):
            driver.find_elements_by_class_name("J_stepItem")[0].click()
            driver.find_elements_by_class_name("J_stepItem")[2].click()
        i+=1

if __name__ == '__main__':
    main()
