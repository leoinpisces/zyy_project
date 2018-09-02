#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cx_Oracle
from __builtin__ import file

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

G_file_no_dict = {}
G_path_prefix = r"F:\\"

#函数-python内部用的是unicode 以utf-8解码 转换为可读的汉字
def convert(str):
    return str.decode('utf-8', 'ignore')

#函数-转换为中文操作系统可读的编码
def convert_c(str):
    return str.decode('utf-8').encode('cp936')

#函数-连接oracle数据库
def get_connection():
    user_name = 'jhemr'
    user_pwd = 'jhemr'
    host = '192.168.248.33'
    port = 1521
    service_name = 'JHEMR'
    dsn = cx_Oracle.makedsn(host, port, service_name)
    try:
        conn = cx_Oracle.connect(user_name, user_pwd, dsn)
    except cx_Oracle.DatabaseError:
        print convert("数据库连接失败")
        return 0
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


#获取给定病案号的病历文档索引号
def get_file_no(patient_id):
    from __builtin__ import str
    #sql语句
    sql = "select a.file_no, a.topic from jhmr_file_index a where a.patient_id = '%s'" % patient_id
    conn = get_connection()
    if conn != 0:
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except cx_Oracle.DatabaseError:
            print convert("sql语句执行失败")
            return 0
        result = cursor.fetchall()
        
        for row in result:
            if len( row ) == 2:
                file_uniq_no = "45038458-2-%s-2-1-0-%s" %(patient_id, str(row[0]))
                topic = str(row[1]).strip()
                G_file_no_dict[file_uniq_no] = topic
    
        close_connection(conn)
        
#获取病历内容并写入指定文件
def get_file_content():
    if len(G_file_no_dict) == 0:
        print convert("索引号列表为空")
    conn = get_connection()
    if conn != 0:
        cursor = conn.cursor()
        
    result_file_name = (G_path_prefix + r"result.txt").decode('utf-8').encode('cp936') 
    file = open( result_file_name, "a+" )
    for file_uniq_no in G_file_no_dict.keys():
        sql = "select d.mr_content from jhmr_file_content_TEXT d where d.file_unique_id = '%s'" % file_uniq_no
        #print sql
        try:
            cursor.execute(sql)
            content_list = get_content_from_lob(cursor)
        except cx_Oracle.DatabaseError:
            print convert("获取病历内容失败")
            return 0
        
        for item in content_list:
            print G_file_no_dict[file_uniq_no]
            file.write(G_file_no_dict[file_uniq_no])
            file.write("\r\n")
            item = item.decode('cp936').encode('utf-8')
            file.write(item)
            file.write("\r\n")
        
    close_connection(conn)
    file.close()

#接受单个参数 参数为病案号
if __name__ == '__main__':
    #判断是否单参数
    if len(sys.argv) == 2:
        patient_id = sys.argv[1].strip()
        get_file_no(patient_id)
        get_file_content()
    else:
        print convert("参数不正确")
    
    