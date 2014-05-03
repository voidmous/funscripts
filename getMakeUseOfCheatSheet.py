#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import time
import random
import os
import errno
import requests
from bs4 import BeautifulSoup

# 创建文件下载目录
# http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
path = 'MakeUseOf_CheatSheet'
try:
    os.makedirs(path)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(path):
        pass
    else:
        raise


startPageURL = "http://www.makeuseof.com/pages/downloads"
se = requests.session()
se.headers.update({'Connection': 'keep-alive',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1553.0 Safari/537.36'})

resp = se.get(startPageURL)
soup = BeautifulSoup(resp.text)
count = 0
# 为了保证健壮性，搜索连续标签”div >section > a > img”，再返回父节点，得到链接。
for atag in soup.select("div > section > a > img"):
    time.sleep(0.5 * random.random())
    count += 1
    pagelink = atag.parent.get("href")
    filename = atag.parent.parent.h1.contents[0]   # 以h1标题作为文件名
    print filename
    rp = se.get(pagelink)
    sp = BeautifulSoup(rp.text).select("aside > div > section > a")
    # 得到包含下载链接的a标签列表
    s = sp[0]
    pdflink = s.get("href")
    print u"处理第" + repr(count).center(5) + u"条链接：" + pdflink
    # 下载文件并写入文件夹MakeUseOf_CheatSheet
    # 参考http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
    # localFileName = "MakeUseOf_CheatSheet/" + pdflink.split('/')[-1]
    localFileName = path + '/' + filename + '.pdf'
    r = se.get(pdflink, stream=True)
    with open(localFileName, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:   # filter out keep-alive new trunks
                f.write(chunk)
                f.flush()
    f.close()
