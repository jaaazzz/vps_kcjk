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
import requests_cfpass_pkg
from email_server.email_sender_calss import email_sender_calss

db_oper = db_helper_class()
email_sender = email_sender_calss()
file = '/var/www/wordpress/20180907.txt'
#openvz linux
url1 = 'https://billing.virmach.com/cart.php?gid=1'
url1_aff = 'http://t.cn/RsVlGQE'
#kvm ssd windows 
url2 = 'https://billing.virmach.com/cart.php?gid=18'
url2_aff = 'http://t.cn/RsVOdOX'
#storage
url3 = 'https://billing.virmach.com/cart.php?gid=29'
url3_aff = 'http://t.cn/RsVlQ8b'
vps_info = {
        "Micro+": {
            'id': 'OVZ 192M内存小鸡',
            'price':'$1/月',
            'link':'地址:'+url1_aff
        },
        "Value+": {
            'id': 'OVZ 512M内存小鸡',
            'price':'$2.25/月',
            'link':'地址:'+url1_aff
        },
        "Elite+": {
            'id': 'OVZ 1G内存VPS',
            'price':'$4/月',
            'link':'地址:'+url1_aff
        },
        "Pro+": {
            'id': 'OVZ 2G内存VPS',
            'price':'$7/月',
            'link':'地址:'+url1_aff
        },
        "Enterprise+": {
            'id': 'OVZ 8G内存VPS',
            'price':'$12/月',
            'link':'地址:'+url1_aff
        },
        "SSD256": {
            'id': 'KVM&SSD VPS配置：1H/256M/10G SSD',
            'price':'$1.25/月',
            'link':'地址:'+url2_aff
        },
        "SSD512": {
            'id': 'KVM&SSD VPS配置：1H/512M/15G SSD/DDos防御',
            'price':'$2.5/月',
            'link':'地址:'+url2_aff
        },
        "SSD1G": {
            'id': 'KVM&SSD VPS配置：1H/1G/25G SSD/DDos防御/windows',
            'price':'$5/月',
            'link':'地址:'+url2_aff
        },
        "SSD2G": {
            'id': 'KVM&SSD VPS配置：2H/2G/40G SSD/DDos防御/windows',
            'price':'$10/月',
            'link':'购买地址:'+url2_aff
        },
        "SSD4G": {
            'id': 'KVM&SSD VPS配置：3H/4G/60G SSD/DDos防御/windows',
            'price':'$20/月',
            'link':'地址:'+url2_aff
        },
        "SSD8G": {
            'id': 'KVM&SSD VPS配置：4H/8G/100G SSD/DDos防御/windows',
            'price':'$40/月',
            'link':'地址:'+url2_aff
        },
        "SSD16G": {
            'id': 'KVM&SSD VPS配置：6H/16G/250G SSD/DDos防御/windows',
            'price':'$80/月',
            'link':'地址:'+url2_aff
        },
        "SSD32G": {
            'id': 'KVM&SSD VPS配置：8H/32G/500G SSD/DDos防御/windows',
            'price':'$160/月',
            'link':'地址:'+url2_aff
        },
        "STORAGE-500G": {
            'id': 'KVM&SSD VPS配置：1H/512M/500G/5T流量/G口',
            'price':'$3.5/月',
            'link':'地址:'+url3_aff
        },
        "STORAGE-1T": {
            'id': 'KVM&SSD VPS配置：1H/1G/1T/10T流量/G口',
            'price':'$7/月',
            'link':'地址:'+url3_aff
        },
        "STORAGE-2T": {
            'id': 'KVM&SSD VPS配置：2H/2G/2T/20T流量/G口',
            'price':'$14/月',
            'link':'地址:'+url3_aff
        },
        "STORAGE-4T": {
            'id': 'KVM&SSD VPS配置：1H/4G/4T/40T流量/G口',
            'price':'$28/月',
            'link':'地址:'+url3_aff
        }
    }
try:
    response1 = requests_cfpass_pkg.get(url1)
    response2 = requests_cfpass_pkg.get(url2)
    response3 = requests_cfpass_pkg.get(url3)
    if response1 is None or response2 is None or response3 is None:
        email_sender.send_email('virmach','没抓到网页')
    else:
        #print response.text.encode("GBK", 'ignore')
        response_body = response1.content+response2.content+response3.content
        content_type = chardet.detect(response_body)
        if content_type['encoding'] != "UTF-8":
            response_body = response_body.decode(content_type['encoding'], 'ignore')
            response_body = response_body.encode("utf-8", 'ignore')

        # 实时入库

        #html_body = response.text.encode("GBK", 'ignore')
        #print html_body
        searchObj = re.findall(r'<div class="panel panel-default">(.*?)</a>',response_body, re.S|re.I)
        all_info = {}
        notice = ''
        qq_notice = '## Virmach 补货通知 ##\n'
        for item in searchObj: 
            #print item
            name_tmp = re.search( r'<h3 class="text-info" style="margin-top:0px">(.*?)</h3>', item, re.S|re.I)
            name = re.sub(r'<small>(.*?)</small>','',name_tmp.group(1))
            have = item.find('Order Now')
            if item.find('-1 Available') != -1 or  item.find('0 Available') != -1 :
                have = -1
            all_info[name.strip()] = have
        #print all_info

        sql1 = "select info from vps_update_info where provider = 'virmach' Order by update_time desc limit 1"
        (count,info) = db_oper.exe_search(sql1)
        print info
        #print '11'+info[0][0]
        if count == 0 :
            print 'init'
        elif count ==1 and info[0][0]=='':
            print 'no info'
        else:
            old_infos = json.loads(info[0][0])
            for item in all_info:

                if all_info[item] != -1 and old_infos[item]== -1:
                    notice = notice + item + ' buhuo<br>'
                    qq_notice = qq_notice + vps_info[item]['id']+'\n'+vps_info[item]['price']+'  '+vps_info[item]['link']
                elif all_info[item] == -1 and old_infos[item]!= -1:
                    notice = notice + item + ' quehuo<br>'
                elif old_infos.has_key(item) != True :  
                    notice = notice + item + 'xinchanpin'
            if set(old_infos.keys()) != set(all_info.keys()):
                notice = notice + item + '产品类型名发生变化'
        print 'notice='+notice
        if qq_notice != '## Virmach 补货通知 ##\n':
            with open(file, 'a+') as f:
                 f.write(qq_notice+'\n')  
        if notice != '':
            email_sender.send_email('virmach',notice)
        fld_inserttime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))
        sql = "insert into vps_update_info (provider,info,update_time)values('virmach',%s, %s )"
        vals = (json.dumps(all_info),fld_inserttime)
        db_oper.exe_insert(sql, vals)
except :
    email_sender.send_email('virmach','start virmach failed')