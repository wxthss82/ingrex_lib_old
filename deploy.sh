#!/bin/bash
#使用方法：
#在agentinfo.txt下第一行写用户名，第二行写密码(账户必须在挂着ss代理vps的情况下登陆过的，确保在vps上不会触发登陆验证)
#依赖
pip install pyvirtualdisplay
pip install selenium
pip install requests
sudo apt-get install xvfb
sudo apt-get install chromium-browser

# for telegram bot
#pip install nose
#pip install flaky
#pip install python-telegram-bot
pip install telegram
pip install future.utils