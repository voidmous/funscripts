#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# 分析页面得到pdf下载链接并存入MakeUseOf_CheatSheet/pdflinks.txt
# 然后可外部或内部调用curl下载
# 不支持分析文件名

import time
import random
import os
import requests
from bs4 import BeautifulSoup

# 创建文件下载目录
path = 'MakeUseOf_CheatSheet'
os.system('mkdir -p '+ path)

startPageURL = "http://www.makeuseof.com/pages/downloads"
se = requests.session()
se.headers.update({'Connection': 'keep-alive',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1553.0 Safari/537.36'})

resp = se.get(startPageURL)
soup = BeautifulSoup(resp.text)
count = 0
# 为了保证健壮性，搜索连续标签”section > a > img”，再返回父节点，得到链接。
for atag in soup.select("section > a > img"):
    time.sleep(0.5 * random.random())
    count += 1
    pagelink = atag.parent.get("href")
    rp = se.get(pagelink)
    sp = BeautifulSoup(rp.text).select("aside > div > section > a")
    s = sp[0]
    pdflink = s.get("href")
    f = open(path + '/pdflinks.txt', 'a')
    f.write('url = "' + pdflink + '"\n')
    f.close()

# 调用curl下载文件
# 貌似在python中调用curl下载比较慢，不如外部执行
#os.system('cd ' + path + ';curl -O -K pdflinks.txt') 
