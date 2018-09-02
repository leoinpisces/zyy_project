#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cx_Oracle
import os
import re
import xlwt
import datetime

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#函数-连接oracle数据库
def get_connection():
    user_name = 'jhemr'
    user_pwd = 'jhemr'
    host = '192.168.248.33'
    port = 1521
    service_name = 'JHEMR'
    dsn = cx_Oracle.makedsn(host, port, service_name)
    conn = cx_Oracle.connect(user_name, user_pwd, dsn)
    return conn

#函数-关闭数据库连接
def close_connection(conn):
    conn.cursor().close()
    conn.close()
    
#函数-从lob字段中获取内容
def get_content_from_lob(cursor):
    result_list = []
    for row in cursor:
        content_list = []
        for column in row:
            if isinstance(column, cx_Oracle.LOB):
                content_list.append(str(column))
            else:
                content_list.append(column)
        content = "".join(content_list)
        result_list.append(content)
    return result_list

if __name__ == '__main__':
    pass