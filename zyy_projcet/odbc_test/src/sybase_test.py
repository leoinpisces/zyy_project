#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime
import pyodbc
import chardet
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

#函数-python内部用的是unicode 以utf-8解码 转换为可读的汉字
def convert(str):
    return str.decode('utf-8', 'ignore')

#函数-转换为中文操作系统可读的编码
def convert_c(str):
    return str.encode('cp936')

#获取数据库连接
def get_conn(dsn, uid, pwd):
    conn = pyodbc.connect("DSN=%s;UID=%s;pwd=%s" %(dsn, uid, pwd))
    return conn
    
if __name__ == '__main__':
    try:
        conn = get_conn("sybase_test", "sa", "cfrwhldb")
        print "sybase connect OK"
        test_cursor = conn.cursor()
        sql = "SELECT * FROM u_pat WHERE c_sfcard_no = '510221194703140044'"
        test_cursor.execute(sql)
        rows = test_cursor.fetchall()
        
        print len(test_cursor.description)
        
        if len(rows) > 0:
            for row in rows:
                print "Beging..."
                #获取字段名
                #for index in range(len(test_cursor.description)):
                #    print test_cursor.description[index][0]
                print str((row[6]).encode('utf-8','ignore'))
                
#                 print chardet.detect(str((row[6]).encode('cp936','ignore'))) #判断字符串编码 貌似不支持中文编码
        else:
            print "empty result"
        test_cursor.close()
        conn.close()
    finally:
        pass