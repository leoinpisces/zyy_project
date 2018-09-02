#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cx_Oracle
import os
import re
import jieba
import xlwt
import datetime

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
#os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.ZHS16GBK'

reload(sys)
sys.setdefaultencoding('utf8')
    
#函数-python内部用的是unicode 以utf-8解码 转换为可读的汉字
def convert(str):
    return str.decode('utf-8', 'ignore')

#函数-转换为中文操作系统可读的编码
def convert_c(str):
    return str.decode('utf-8').encode('cp936')

#函数-转换为中文操作系统可读的编码
def convert_c2(str):
    return str.decode('cp936').encode('utf-8')


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

#函数-处理主要逻辑
def main_process(cursor):
    sql = "Select mr_content From jhmr_templet_content t Where t.templet_unique_id = '45038458-2-EMR09.00.01_13'"   
    cursor.execute(sql)
    templet_content = get_content_from_lob(cursor)
    if len(templet_content) > 0:
        print (templet_content[0]).decode('gb18030')
        
        
#     file_name = (r"E:\project\emr_templet\test.emt" ).decode('utf-8').encode('cp936')
#     file = open(file_name, "a+")
#     file.write(templet_content[0])
#     file.write("\r\n")
#     file.close()

            

if __name__ == '__main__':
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        main_process(cursor)
    finally:
        close_connection(conn)
    print convert("你好，世界")