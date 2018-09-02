#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import cx_Oracle
import pyodbc

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

G_DB_defaut = { "usrname":"jhemr", "pwd":"jhemr", "host":"192.168.248.198", "port":"1521", "service_name":"jhemrcs", "dsn":None }

class db_connector():
    def __init__(self, usrname = G_DB_defaut["usrname"], pwd = G_DB_defaut["pwd"], 
                 host = G_DB_defaut["host"], port = G_DB_defaut["port"], 
                 service_name = G_DB_defaut["service_name"], dsn = G_DB_defaut["dsn"], db_type = "ora"):
        #数据成员
        self.usrname = usrname
        self.pwd = pwd
        self.host = host
        self.port = port
        self.service_name = service_name
        self.dsn = dsn
        self.result_rows = None
        self.db_type = db_type
                
        #以下是私有成员
        self.__conn = None
        self.__cursor = None
        #判断数据库类型 调用相应的建连接函数
        if self.db_type == "ora":
            self.__get_oracle_connection()
        else:
            self.__get_odbc_connection()
        if self.__conn:    
            self.__cursor = self.__conn.cursor()
        
    def __del__(self):
        if self.__cursor:
            self.__cursor.close()
        if self.__conn:
            self.__conn.close()
        
    #构造oracle连接    私有函数
    def __get_oracle_connection(self):
        try:
            self.dsn = cx_Oracle.makedsn(self.host, self.port, self.service_name)
            self.__conn = cx_Oracle.connect(self.usrname, self.pwd, self.dsn)
        except cx_Oracle.DatabaseError:
            if self.__conn:
                self.__conn.close()
                
    #构造odbc连接 私有函数
    def __get_odbc_connection(self):
        try:
            #self.__conn = pyodbc.connect("DSN=%s;UID=%s;PWD=%s;CHARSET=CP850" %(self.dsn, self.usrname, self.pwd), unicode_results=True) 
            self.__conn = pyodbc.connect("DSN=%s;UID=%s;PWD=%s" %(self.dsn, self.usrname, self.pwd), unicode_results=True) 
        except pyodbc.Error:
            if self.__conn:
                self.__conn.close()
    
    #函数-从lob字段中获取内容
    def get_content_from_lob(self):
        if self.__cursor:
            result_list = []
            for row in self.__cursor:
                content_list = []
                for column in row:
                    if isinstance(column, cx_Oracle.LOB):
                        content_list.append(str(column))
                    else:
                        content_list.append(column)
                content = "".join(content_list)
                result_list.append(content)
            return result_list
        else:
            return None
    
    #函数-从lob字段中获取内容_cache用
    def cache_get_content_from_lob(self):
        if self.__cursor:
            result_list = []
            for row in self.__cursor:
                content_list = []
                
                for column in row:
                    content_list.append(str(column))
                    
                content = "".join(content_list)
                result_list.append(content)
            return result_list
        else:
            return None
    
    #获取字段名列表 必须在excute函数调用之后才能使用 不单独使用
    def get_field_names(self):
        if self.__cursor:
            field_list = []
            for index in range(len(self.__cursor.description)):
                field_list.append(self.__cursor.description[index][0])
            return field_list
        else:
            return None
    
    #执行sql语句 返回结果列表
    def get_list(self, sql, fields):
        if self.__cursor and len(sql) > 0:
            try:
                #self.__cursor.execute(sql)
                #self.result_rows = self.__cursor.fetchall()
                self.get_rows(sql)
            except Exception, e:
                return str(e)
            
            return self.__turn_dictlist(fields)
            
    #把执行结果转换成列表  构成为 [{数据行1}, {数据行2}...]
    def __turn_dictlist(self, fields):
        #20180113应对oracle只能取到大写的字段名 将本地字段传入
        #field_list = self.get_field_names()
        field_list = fields
        #组成{字段名:值}的列表
        if not field_list:
            return None
        
        result_list = []
        if self.result_rows:
            for row in self.result_rows:
                temp_dict = {}   
                for index in range(len(field_list)):
                    tmp_result = (str(row[index]).strip()).encode('utf-8','ignore')
                    #如果表中无数据 则传空值
                    if tmp_result == "None":
                        tmp_result = ""
                    temp_dict[field_list[index]] = tmp_result #一行数据
                result_list.append(temp_dict)
            return result_list
        else:
            #如果是空集也要返回结果字典 字典中每个key值是""
            temp_dict = {}
            for index in range(len(field_list)):
                temp_dict[field_list[index]] = ""
            result_list.append(temp_dict)
            return result_list

            #如果是空集返回None
            #return None
        
    #返回结果集
    def get_rows(self, sql):
        if self.__cursor and len(sql) > 0:
            self.result_rows = []
            
            #先生成查询记录数量的sql语句 因为pyodbc在处理特殊汉字字符的时候可能出现问题
            table_index = sql.find("from")
            if table_index == -1:
                table_index = sql.find("FROM")
            if table_index == -1:
                return "WrongSql"
            table_index = table_index + len("from")
            count_sql = "select count(1) from " + sql[table_index:]
            row_count = 0
            try:
                self.__cursor.execute(count_sql)
                row = self.__cursor.fetchone()
                row_count = int(row[0])
            except Exception, e:
                return str(e)
            
            #执行主sql
            try:
                self.__cursor.execute(sql)
            except Exception, e:
                return str(e)
            
            for index in range(row_count):
                try:
                    row = self.__cursor.fetchone()
                    if row:
                        self.result_rows.append(row)
                except Exception,e:
                    continue
            return self.result_rows
        else:
            return "EmptyResult"
        
    #跳过异常 继续返回结果集 直到所有结果均取出 本函数可能会死循环
    def go_on_get_rows(self):
        if self.__cursor:
            try:
                while True:
                    row = self.__cursor.fetchone()
                    if row:
                        self.result_rows.append(row)
                    else:
                        break
            except Exception, e:
                self.go_on_get_rows()
            return self.result_rows
        else:
            return "EmptyResult"
    
    #执行sql语句并提交事务
    def excute_sql(self, sql):
        if sql and len(sql) > 0:
            try:
                self.__cursor.execute(sql)
                self.__conn.commit()
                return 0
            except Exception, e:
                return str(e)
        else:
            return "WrongSQL"
                    