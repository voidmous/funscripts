#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# 下载此页面的所有pdf：
# http://refcardz.dzone.com/

import time
import random
import getpass   # 隐藏密码输入
import os
import errno
import logging
import sqlite3
import requests
from bs4 import BeautifulSoup

logging.basicConfig(filename=os.path.join(os.getcwd(), 'log.txt'),
                    level=logging.NOTSET)

PATH = 'RefCardz'
LOGIN_URL = 'http://refcardz.dzone.com/user'
STARTPAGE_URL = 'http://refcardz.dzone.com/'


# 创建文件保存目录
try:
    os.makedirs(PATH)
except OSError as exc:
    if exc.errno == errno.EEXIST and os.path.isdir(PATH):
        pass
    else:
        raise

db_filename = PATH + '/downloaded.db'
db_is_new = not os.path.exists(db_filename)
if db_is_new:
    print "创建新数据库文件，并创建新表DOWNLOADINFO"
    logging.info("创建新数据库文件，并创建新表DOWNLOADINFO")
    conn = sqlite3.connect(db_filename)
    conn.execute('''CREATE TABLE DOWNLOADINFO
        (ID INTEGER PRIMARY  KEY,
        NAME            TEXT   NOT NULL,
        PDFLINK         TEXT   NOT NULL,
        DOWNLOADED      INT    NOT NULL);''')
    print "表DOWNLOADINFO创建成功"
else:
    print "数据库文件已存在"
    logging.info("数据库文件已存在")
    conn = sqlite3.connect(db_filename)

cursor = conn.cursor()

# 创建requests会话，此会话可以保持cookie
se = requests.session()
se.headers.update({
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1553.0 Safari/537.36'})

# POST参数，通过分析LOGIN_URL得到
user = raw_input("请输入账户名：")
pwd = getpass.getpass(prompt="请输入密码：")
login_data = {'name': user, 'pass': pwd, 'op': 'Login', 'form_id': 'user_login'}

# 随意下载页面，获得cookie
se.get(STARTPAGE_URL)
resp = se.post(LOGIN_URL, data=login_data)   # 使用POST参数登录
# 登录如果成功，响应的页面应该显示用户名
# f = open('login.html', 'w')
# f.write(resp.text.encode('utf-8'))
# f.close()
# logging.info("写入login.html")
if resp.status_code == 200:
    logging.info("登录成功，转到下载页面")

# 处理RefCardz下载页面，提取下载链接
resp = se.get(STARTPAGE_URL)
soup = BeautifulSoup(resp.text)
# 此时下载的页面也应带有用户标记
# with open('refcardz.html', 'w') as f:
#    f.write(resp.text.encode('utf-8'))
#    f.close()
#    logging.info("写入refcardz.html")
count = 0
for linkblock in soup.find_all("a", class_="download-button refcardz-button"):
    time.sleep(20 * random.random())   # 随机休息20s以内
    count += 1
    # 获取文件描述作为文件名
    # onclick='download_clicked("homepage table download","Core Java Concurrency");'
    name = linkblock.get('onclick').split('"')[-2]
    print name
    link = "http://refcardz.dzone.com" + linkblock.get('href')   # 此链接会被转向
    print repr(count).ljust(5) + link
    # 提取链接的GET参数
    payload = {}   # 以字典存放参数
    tmp = link.split('?')[-1].split('&')
    for a in tmp:   # tmp形如： ["oid=rchom9965","direct=true"]
        payload[a.split('=')[0]] = a.split('=')[1]
    rp = se.get(link, params=payload)
    pdflink = rp.url
    logging.info(pdflink)
    # 如果返回的链接无法被识别，则放弃处理、记入日志并处理下一链接
    if 'pdf' not in pdflink:
        logging.info("返回pdf链接失败，请检查" + pdflink.encode('utf-8'))
        continue
    # 查询纪录数据库，检查是否为新链接
    cursor.execute("""
        SELECT * FROM DOWNLOADINFO
        """)

    recorded = 0
    downloaded = 0
    # 判断是否已经记录以及是否已经下载过
    for row in cursor.fetchall():
        if (name in row) and (pdflink in row):
            recorded = 1
            print "此链接已记录，不需重复添加"
            logging.info("此链接已记录，不需重复添加")
            if row[3] == 1:    # 已记录并且已经下载过
                downloaded = 1
    # 没记录过则添加记录
    if not recorded:
        cursor.execute("""
        INSERT INTO DOWNLOADINFO (ID, NAME, PDFLINK, DOWNLOADED)
        VALUES (NULL, ?, ?, 0)""", (name, pdflink))
        print "添加新记录"
        logging.info("添加新记录")
    if downloaded:
        continue    # 已经下载过，不再重复下载，进行下一迭代

    # 文件名形如：
    localFileName = PATH + '/' + pdflink.split('/')[-1].split('-')[0].encode('utf-8') + '-' + name + '.pdf'
    logging.info("下载并写入文件 " + localFileName.encode('utf-8'))
    r = se.get(pdflink, stream=True)
    with open(localFileName, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:   # filter out keep-alive new trunks
                f.write(chunk)
                f.flush()
    cursor.execute("""
        UPDATE DOWNLOADINFO set DOWNLOADED = 1 WHERE NAME=? OR PDFLINK=?
        """, (name, pdflink))
    conn.commit()

conn.close()
