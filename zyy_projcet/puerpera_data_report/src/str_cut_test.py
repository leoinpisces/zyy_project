#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cx_Oracle
import os
import re
import jieba
import xlwt
import datetime
from __builtin__ import file
from operator import itemgetter
from datetime import date
from xmlrpclib import DateTime

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

def remove_illegal_date(date_str):
    temp_str = date_str
    for index in range(len(temp_str)):
        if temp_str[index].isdigit():
            continue
        else:
            date_str = date_str.replace(temp_str[index], "")
    return date_str

#函数-连接oracle数据库
def get_connection():
    user_name = 'jhemr'
    user_pwd = 'jhemr'
    host = '192.168.248.198'
    port = 1521
    service_name = 'JHEMRCS'
    dsn = cx_Oracle.makedsn(host, port, service_name)
    conn = cx_Oracle.connect(user_name, user_pwd, dsn)
    return conn

    
#函数-关闭数据库连接
def close_connection(conn):
    conn.cursor().close()
    conn.close()

    
if __name__ == '__main__':    
    #conn = get_connection()
    #cursor = conn.cursor()
    #sql = "select d.mr_content from jhmr_file_content_TEXT d where d.file_unique_id = '45038458-2-342280-2-1-0-16'"
    #cursor.execute(sql)
    #result_list = get_content_from_lob(cursor)
    #print result_list[0].decode('cp936')
    #close_connection(conn)
    str = "123"
    list = str.split("_")
    print "...".join(list)
    
    
    