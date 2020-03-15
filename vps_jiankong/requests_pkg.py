#!/usr/bin/python
# coding:utf-8
# Copyright (C) 2005-2016 All rights reserved.
# FILENAME: 	 requests_pkg.py
# VERSION: 	 1.0
# CREATED: 	 2016-01-14 20:25
# AUTHOR: 	 vpsjxw.com
# DESCRIPTION:   requests类的包裹器
#
# HISTORY:
#*************************************************************
import time
import requests
from random_useragent import getRandomUA


def get(url, max_try=3, timeout=120):
    try_count = 0
    while True:
        h_heads = getRandomUA()
        my_proxies={"http":"http://127.0.0.1:1081","https":"https://127.0.0.1:1081"}
        my_proxies1={"http":"http://222.85.50.177:808"}
        my_proxies2={"https":"http://114.239.127.14:61234"}
        try_count += 1
        if try_count >= max_try:
            return None
        try:
            #resp = requests.get(url, headers=h_heads,proxies=my_proxies1, timeout=timeout)
            resp = requests.get(url, headers=h_heads, timeout=timeout)
            if resp:
                return resp
            else:
                # if try_count >= max_try:
                #     return None
                time.sleep(3)
        except Exception,e:  
            print Exception,":",e
            pass
