#!/usr/bin/python
#coding:utf-8
# AUTHOR:    vpsjxw.com
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import chardet
import hashlib
import time
import requests
import json
import MySQLdb
import db_conf
from db_helper import db_helper_class

from bs4 import BeautifulSoup
import requests_pkg
from email_server.email_sender_calss import email_sender_calss

db_oper = db_helper_class()
email_sender = email_sender_calss()

url1 = 'https://secure.hostsolutions.ro/cart.php?gid=36'
url2 = 'https://secure.hostsolutions.ro/cart.php?gid=31'
try:
    all_info = {}
    notice = ''
    for i in range(1,3):
        response = requests_pkg.get(eval('url'+str(i)))
        if response is None:
            email_sender.send_email('hostsolutions','没抓到网页')
        else:
            response_body = response.content
            content_type = chardet.detect(response_body)
            if content_type['encoding'] != "UTF-8":
                response_body = response_body.decode(content_type['encoding'], 'ignore')
                response_body = response_body.encode("utf-8", 'ignore')

            # 实时入库
            bs_body = BeautifulSoup(response_body)
            #print html_body
            searchObj = bs_body.find_all("div", class_="product")
            titleObj = re.search( r'<h1>(.*?)</h1>', response_body, re.S|re.I)
            title = titleObj.group(1).strip()           
            for i in range(len(searchObj)):
                name = re.search( r'<div class="name">(.*?)<', str(searchObj[i]), re.S|re.I)
                have = str(searchObj[i]).find('Order Now')
                all_info[title+name.group(1).strip()] = have
    sql1 = "select info from vps_update_info where provider = 'hostsolutions' Order by update_time desc limit 1"
    (count,info) = db_oper.exe_search(sql1)
    if count == 0 :
        print 'init'
    elif count ==1 and info[0][0]=='':
        print 'no info'
    else:
        old_infos = json.loads(info[0][0])
        old_keys = set(old_infos.keys())
        new_keys = set(all_info.keys())
        add_keys = new_keys - old_keys
        del_keys = old_keys - new_keys
        ava_keys = new_keys&old_keys
        if old_keys != new_keys:
            notice = notice + 'product types and namas CHANGED<br>'
        if len(add_keys) > 0:
            for a in add_keys:
                notice = notice + a + ' ADD PRODUCT<br>'
        if len(del_keys) > 0:   
            for d in del_keys:
                notice = notice + d + ' REMOVE PRODUCT<br>'
        for item in all_info:
            if item in ava_keys:
                if all_info[item] != -1 and old_infos[item]== -1:
                    notice = notice + item + ' buhuo<br>'
                elif all_info[item] == -1 and old_infos[item]!= -1:
                    notice = notice + item + ' quehuo<br>'
    print 'notice='+notice
    if notice != '':
        email_sender.send_email('hostsolutions',notice)
    fld_inserttime = time.strftime(
        '%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
    sql = "insert into vps_update_info (provider,info,update_time)values('hostsolutions',%s, %s )"
    vals = (json.dumps(all_info),fld_inserttime)
    db_oper.exe_insert(sql, vals)
except:
    email_sender.send_email('hostsolutions','start hostsolutions failed')