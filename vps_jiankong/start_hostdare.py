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
import requests_pkg
from email_server.email_sender_calss import email_sender_calss

db_oper = db_helper_class()
email_sender = email_sender_calss()
#国内优化KVM
url1 = 'https://manage.hostdare.com/cart.php?gid=16'
#亚洲优化KVM
url2 = 'https://manage.hostdare.com/cart.php?gid=13'

try:
    response1 = requests_pkg.get(url1)
    response2 = requests_pkg.get(url2)
    if response1 is None or response2 is None :
        email_sender.send_email('hostdare','没抓到网页')
    else:
        #print response.text.encode("GBK", 'ignore')
        response_body = response1.content+response2.content
        content_type = chardet.detect(response_body)
        if content_type['encoding'] != "UTF-8":
            response_body = response_body.decode(content_type['encoding'], 'ignore')
            response_body = response_body.encode("utf-8", 'ignore')

        # 实时入库

        #html_body = response.text.encode("GBK", 'ignore')
        #print html_body
        searchObj = re.findall(r'<div class="product clearfix"(.*?)</div>',response_body, re.S|re.I)
        all_info = {}
        notice = ''
        for item in searchObj: 
            #print item
            name = re.search( r'<span id="product(.*?)-name">(.*?)</span>', item, re.S|re.I)
            have = item.find('Available')
            all_info[name.group(2).strip()] = have
        #print all_info

        sql1 = "select info from vps_update_info where provider = 'hostdare' Order by update_time desc limit 1"
        (count,info) = db_oper.exe_search(sql1)
        #print '11'+info[0][0]
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
                        notice = notice + item + ' quehuo<br>'
                    elif all_info[item] == -1 and old_infos[item]!= -1:
                        notice = notice + item + ' buhuo<br>'
        print 'notice='+notice
        if notice != '':
            email_sender.send_email('hostdare',notice)
        fld_inserttime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
        sql = "insert into vps_update_info (provider,info,update_time)values('hostdare',%s, %s )"
        vals = (json.dumps(all_info),fld_inserttime)
        db_oper.exe_insert(sql, vals)
except:
    email_sender.send_email('hostdare','start hostdare failed')