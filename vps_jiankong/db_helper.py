#!/usr/bin/python
# coding:utf-8
# Copyright (C) 2005-2016 All rights reserved.
# FILENAME: 	 db_helper.py
# VERSION: 	 1.0
# CREATED: 	 2016-01-14 09:50
# AUTHOR: 	 vpsjxw.com
# DESCRIPTION:   数据入库类
#
# HISTORY:
#*************************************************************

import MySQLdb
import db_conf


class db_helper_class:

    def __init__(self):
        self.db = MySQLdb.connect(
            db_conf.db_host,
            db_conf.db_user,
            db_conf.db_passwd,
            db_conf.db_name, 
            charset="utf8")
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    #**********************************************************************
    # 描  述： 数据库查询操作
    #
    # 参  数： sql, 查询语句
    #
    # 返回值： 返回一个元组，包含受影响的行数、及fetchall()迭代器
    # 修  改： 
    #**********************************************************************
    def exe_search(self, sql):
        #受影响的行数
        line_cnt = self.cursor.execute(sql)
        return (line_cnt, self.cursor.fetchall())

    #**********************************************************************
    # 描  述： 数据库insert插入操作
    #
    # 参  数： sql, 插入格式部分
    # 参  数： vals, 插入值元组
    #
    # 返回值： 空
    # 修  改： 
    #**********************************************************************
    def exe_insert(self, sql, vals):
        self.cursor.execute(sql, vals)
        self.db.commit()

    #**********************************************************************
    # 描  述： 执行更新操作
    #
    # 参  数： sql, 更新SQL语句
    #
    # 返回值： 空
    # 修  改： 
    #**********************************************************************
    def exe_update(self, sql,vals):
        line_cnt = self.cursor.execute(sql,vals)
        return line_cnt;

    def get_cursor(self):
        return self.cursor;
    def exe_close(self):
        self.db.close()
