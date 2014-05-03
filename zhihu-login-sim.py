#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 知乎模拟登陆测试
# http://www.zhihu.com/

# import time
# import random
import getpass   # 隐藏密码输入
import requests
from bs4 import BeautifulSoup

LOGIN_URL = 'http://www.zhihu.com/'
HEADERS = {
    'Host': 'www.zhihu.com',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Referer': 'http://www.zhihu.com/',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    'Origin': 'http://www.zhihu.com',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1553.0 Safari/537.36'
}


def login(login_url, headers, login_data):
    se = requests.session()
    se.headers.update(headers)
    tmp = se.get(login_url)   # 获取登陆页面html和cookie，准备登陆
    # 搜索登陆表单，准备提取_xsrf值
    # 页面中有三个_xsrf且均相同
    with open('main.html', 'w') as f:
        f.write(tmp.text.encode('utf-8'))
        f.close()
    xsrf = BeautifulSoup(tmp.text).find("input", attrs={"name": "_xsrf"}).get("value")
    # 表单参数包括email, password, _xsrf和rememberme
    login_data["_xsrf"] = xsrf   # 存入xsrf值
    print login_data
    resp = se.post(login_url, data=login_data)
    print resp.url
    with open('login.html', 'w') as f:
        f.write(resp.text.encode('utf-8'))
        f.close()

    return resp


if __name__ == "__main__":
    email = raw_input("请输入邮箱：")
    password = getpass.getpass(prompt="请输入密码：")
    rememberme = 'y'
    login_data = {'email': email, 'password': password, 'rememberme': rememberme}
    login(LOGIN_URL, HEADERS, login_data)
    # resp = se.get(STARTPAGE_URL)
    # print resp.url
    # print resp.status_code
