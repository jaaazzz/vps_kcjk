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

url1 = 'https://clientarea.ramnode.com/cart.php?gid=11'
url2 = 'https://clientarea.ramnode.com/cart.php?gid=15'
url3 = 'https://clientarea.ramnode.com/cart.php?gid=19'
url4 = 'https://clientarea.ramnode.com/cart.php?gid=22'
url5 = 'https://clientarea.ramnode.com/cart.php?gid=23'
url6 = 'https://clientarea.ramnode.com/cart.php?gid=24'
url7 = 'https://clientarea.ramnode.com/cart.php?gid=25'
url8 = 'https://clientarea.ramnode.com/cart.php?gid=27'
url9 = 'https://clientarea.ramnode.com/cart.php?gid=29'
url10 = 'https://clientarea.ramnode.com/cart.php?gid=30'
url11 = 'https://clientarea.ramnode.com/cart.php?gid=31'
url12 = 'https://clientarea.ramnode.com/cart.php?gid=32'
url13 = 'https://clientarea.ramnode.com/cart.php?gid=33'
url14 = 'https://clientarea.ramnode.com/cart.php?gid=34'
url15 = 'https://clientarea.ramnode.com/cart.php?gid=35'
url16 = 'https://clientarea.ramnode.com/cart.php?gid=36'
url17 = 'https://clientarea.ramnode.com/cart.php?gid=38'
url18 = 'https://clientarea.ramnode.com/cart.php?gid=40'
url19 = 'https://clientarea.ramnode.com/cart.php?gid=41'
url20 = 'https://clientarea.ramnode.com/cart.php?gid=42'
url21 = 'https://clientarea.ramnode.com/cart.php?gid=43'
url22 = 'https://clientarea.ramnode.com/cart.php?gid=44'
url23 = 'https://clientarea.ramnode.com/cart.php?gid=45'
url24 = 'https://clientarea.ramnode.com/cart.php?gid=46'
url25 = 'https://clientarea.ramnode.com/cart.php?gid=47'
url26 = 'https://clientarea.ramnode.com/cart.php?gid=49'
url27 = 'https://clientarea.ramnode.com/cart.php?gid=50'
url28 = 'https://clientarea.ramnode.com/cart.php?gid=51'
url29 = 'https://clientarea.ramnode.com/cart.php?gid=52'
url30 = 'https://clientarea.ramnode.com/cart.php?gid=53'
try:
	all_info = {}
	notice = ''
	for i in range(1,31):
		response = requests_pkg.get(eval('url'+str(i)))
		if response is None:
			email_sender.send_email('ramnode','没抓到网页')
		else:
			response_body = response.content
	        content_type = chardet.detect(response_body)
	        if content_type['encoding'] != "UTF-8":
	            response_body = response_body.decode(content_type['encoding'], 'ignore')
	            response_body = response_body.encode("utf-8", 'ignore')

	        # 实时入库

	        html_body = response.text.encode("GBK", 'ignore')
	        #print html_body
	        searchObj = re.findall(r'<div class="price-container container-with-progress-bar text-center">(.*?)</div>',response_body, re.S|re.I)
	        titleObj = re.search( r'<h2 id="headline">(.*?)</h2>', response_body, re.S|re.I)
	        title = titleObj.group(1).strip()           
	        for item in searchObj: 
	        	name = re.search( r'(.*?)<span class="price-cont">', item, re.S|re.I)
	        	have = item.find('Out of Stock')
	        	all_info[title+name.group(1).strip()] = have
	sql1 = "select info from vps_update_info where provider = 'ramnode' Order by update_time desc limit 1"
	(count,info) = db_oper.exe_search(sql1)
	if count == 0 :
		print 'init'
	elif count ==1 and info[0][0]=='':
		print 'no info'
	else:
		old_infos = json.loads(info[0][0])
		for item in all_info:

			if all_info[item] != -1 and old_infos[item]== -1:
				notice = notice + item + ' quehuo<br>'
			elif all_info[item] == -1 and old_infos[item]!= -1:
				notice = notice + item + ' buhuo<br>'
			elif old_infos.has_key(item) != True :
				notice = notice + item + 'xinchanpin'
	print 'notice='+notice
	if notice != '':
		email_sender.send_email('ramnode',notice)
	fld_inserttime = time.strftime(
	    '%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
	sql = "insert into vps_update_info (provider,info,update_time)values('ramnode',%s, %s )"
	vals = (json.dumps(all_info),fld_inserttime)
	db_oper.exe_insert(sql, vals)
except:
	email_sender.send_email('ramnode','start ramnode failed')