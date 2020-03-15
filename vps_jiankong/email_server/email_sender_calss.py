#!/usr/bin/python
# coding:utf-8
# Copyright (C) 2005-2016 All rights reserved.
# FILENAME: 	 email_sender_calss.py
# VERSION: 	 1.0
# CREATED: 	 2016-02-02 16:54
# AUTHOR:    vpsjxw.com
# DESCRIPTION:   Email服务器
#
# HISTORY:
#*************************************************************

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import smtplib
from email.mime.text import MIMEText



class email_sender_calss():
 
         

    def send_email(self,vpstype='',info=''):
        sender = '111111@163.com'
        receiver = '222222@qq.com'

        curr_time = time.strftime("%Y-%m-%d %H:%M:%S")
        subject = vpstype+' 产品列表状态 ' +curr_time

        smtpserver = 'smtp.163.com'
        username = '111111@163.com'
        password = 'xxxxx'

        str_body= 'ceshi'
        str_html = "<html><h1>"+vpstype+" 产品列表状态:</h1><br>"+info+"</html>"

        msg = MIMEText(str_html, 'html', 'utf-8')
        msg['Subject'] = subject
        msg['from'] = '111111@163.com'
        msg['to'] = '222222@qq.com'
        smtp = smtplib.SMTP(smtpserver)
        # smtp.connect(smtpserver)

        #smtp.esmtp_features["auth"]="LOGIN PLAIN"
        # smtp.esmtp_features["auth"]="LOGIN"
        smtp.esmtp_features["auth"] = "PLAIN"
        (code, resp) = smtp.login(username, password)
        if 0:
            # if code != 235:
            print("fail")
        else:
            print("success")
            result = smtp.sendmail(sender, receiver, msg.as_string())
            print result
            smtp.quit()
        pass
