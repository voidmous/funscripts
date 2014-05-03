#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 知乎测试
# http://www.zhihu.com/

import time
import random
import getpass   # 隐藏密码输入
import requests
from bs4 import BeautifulSoup

LOGIN_URL = 'http://www.zhihu.com/#signin'
STARTPAGE_URL = 'http://www.zhihu.com/'
se = requests.session()
user = raw_input("请输入账户名：")
pwd = getpass.getpass(prompt="请输入密码：")
login_data= {'user':user, 'password':pwd}
#se.auth = (user, pwd)
se.headers.update({'Host': 'www.zhihu.com',
                   'Connection': 'keep-alive',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1553.0 Safari/537.36'})
login = se.post(LOGIN_URL, login_data)      # 登陆
#login = se.post(LOGIN_URL)
print login.url
print login.status_code
