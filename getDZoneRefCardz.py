#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 下载此页面的所有pdf：
# http://refcardz.dzone.com/

import time
import random
import getpass   # 隐藏密码输入
import requests
from bs4 import BeautifulSoup

LOGIN_URL = 'http://www.dzone.com/links/index.html'
STARTPAGE_URL = 'http://refcardz.dzone.com/'
se = requests.session()
user = raw_input("请输入账户名：")
pwd = getpass.getpass(prompt="请输入密码：")
login_data= {'user':user, 'password':pwd}
#se.auth = (user, pwd)
se.headers.update({'Connection': 'keep-alive',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1553.0 Safari/537.36'})
login = se.post(LOGIN_URL, login_data)      # 登陆
print login.url
print login.status_code
f = open('login.html','w')
f.write(login.text.encode(('utf8')))
f.close()
resp = se.get(STARTPAGE_URL)   # 获取RefCardz页面
f = open('startpage.html','w')
f.write(resp.text.encode(('utf8')))
f.close()
print resp.url
print resp.status_code
soup = BeautifulSoup(resp.text)   # 处理html页面，提取下载链接
count = 0
for linkblock in soup.find_all("a", class_="download-button refcardz-button"):
    time.sleep(0.5 * random.random())   # 随机休息0~0.5s
    count += 1
    link = "http://refcardz.dzone.com" + linkblock.get('href')   # 此链接会被转向
    print repr(count).ljust(5) + link
    r = se.get(link)
    r = se.get(r.url)
    print r.url
    print r.status_code
    dllink = r.headers['Location']
    print dllink