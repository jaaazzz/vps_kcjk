#!/usr/bin/python
# coding:utf-8
# Copyright (C) 2005-2016 All rights reserved.
# FILENAME: 	 email_sender_main.py
# VERSION: 	 1.0
# CREATED: 	 2016-02-02 16:53
# AUTHOR:    vpsjxw.com
# DESCRIPTION:   Email服务器
#
# HISTORY:
#*************************************************************

import sys
from email_sender_calss import email_sender_calss

if __name__ == '__main__':
    # 新建一个应用
    app = email_sender_calss()
    app.do_task()
