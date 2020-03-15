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

url1 = 'https://my.rfchost.com/cart.php?gid=14'
url2 = 'https://my.rfchost.com/cart.php?gid=7'
url3 = 'https://my.rfchost.com/cart.php?gid=3'
url4 = 'https://my.rfchost.com/cart.php?gid=8'
url5 = 'https://my.rfchost.com/cart.php?gid=10'
url6 = 'https://my.rfchost.com/cart.php?gid=13'
url7 = 'https://my.rfchost.com/cart.php?gid=15'
url8 = 'https://my.rfchost.com/cart.php?gid=16'
try:
	all_info = {}
	notice = ''
	for i in range(1,9):
		response = requests_pkg.get(eval('url'+str(i)))
		if response is None:
			email_sender.send_email('rfchost','没抓到网页')
		else:
			response_body = response.content
	        content_type = chardet.detect(response_body)
	        if content_type['encoding'] != "UTF-8":
	            response_body = response_body.decode(content_type['encoding'], 'ignore')
	            response_body = response_body.encode("utf-8", 'ignore')

	        # 实时入库

	        html_body = response.text.encode("GBK", 'ignore')
	        #print html_body
	        searchObj = re.findall(r'<div class="price-table">(.*?)</ul>',response_body, re.S|re.I)
	        titleObj = re.search( r'<h1>(.*?)</h1>', response_body, re.S|re.I)
	        title = titleObj.group(1).strip()           
	        for item in searchObj: 
	        	name = re.search( r'<h4 id="product(.*?)-name">(.*?)</h4>', item, re.S|re.I)
	        	have = item.find('缺货中')
	        	all_info[title+name.group(2).strip()] = have
	sql1 = "select info from vps_update_info where provider = 'rfchost' Order by update_time desc limit 1"
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
		old_infos = json.loads(info[0][0])
		for item in all_info:
			if item in ava_keys:
				if all_info[item] != -1 and old_infos[item]== -1:
					notice = notice + item + ' quehuo<br>'
				elif all_info[item] == -1 and old_infos[item]!= -1:
					notice = notice + item + ' buhuo<br>'
	if notice != '':
		email_sender.send_email('rfchost',notice)
	fld_inserttime = time.strftime(
	    '%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
	sql = "insert into vps_update_info (provider,info,update_time)values('rfchost',%s, %s )"
	vals = (json.dumps(all_info),fld_inserttime)
	db_oper.exe_insert(sql, vals)
except:
	email_sender.send_email('rfchost','start rfchost failed')