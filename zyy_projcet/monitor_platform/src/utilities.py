#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import json
import uuid
import ssl
import httplib
import gzip
import socket
import logging
import logging.handlers
import datetime
from cStringIO import StringIO
from random import randint
import db_connector
import time
import gc


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#卫计委分配的医院编号
G_hospital_no = "400057716"
#医院名称
G_hospital_name = "重庆市中医院"

#生成日志记录对象
G_logger = logging.getLogger('monitor_logger')

#日志文件名称
G_datestr_for_log = datetime.date.today().strftime("%Y-%m-%d")
#获取脚本所在路径
log_file_path = (os.path.split(os.path.realpath(__file__))[0] + "\\log\\").decode('utf-8').encode('cp936')
#由于打包成exe后 程序的执行路径是系统的临时目录 所以还是指定好目录
if os.path.exists(r"D:\\".decode('utf-8').encode('cp936')):
    log_file_path = (r"D:\monitor_log\%s\\" % G_datestr_for_log).decode('utf-8').encode('cp936')
else:
    log_file_path = (r"C:\monitor_log\%s\\" % G_datestr_for_log).decode('utf-8').encode('cp936')

if not os.path.exists(log_file_path):
    os.makedirs(log_file_path)
log_file = log_file_path + (r"monitor_log_%s.log" % G_datestr_for_log).decode('utf-8').encode('cp936')

#日志文件handler 用于日志文件分割  按文件大小分割日志 单个日志文件大小为10M
G_log_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes = 10240*1024, backupCount = 100)

#日志格式
G_formatter = logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s')
G_log_handler.setFormatter(G_formatter)

#添加文件处理器
G_logger.addHandler(G_log_handler)

#设置日志记录基本
G_logger.setLevel(logging.DEBUG)


#函数-转换为中文操作系统可读的编码
def convert_c(text_str):
    return text_str.decode('utf-8').encode('cp936')
    

#程序运行跨天之后 重设日志路径和日志名 20180121 李浩更新
def reset_log_date():
    #引用全局变量
    global G_datestr_for_log
    global G_log_handler
    global G_logger
    global log_file
    global log_file_path
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    
    if today_str != G_datestr_for_log:
        #更新日志文件中日期相关的字符串
        log_file_path = log_file_path.replace(G_datestr_for_log, today_str.decode('utf-8').encode('cp936'))
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        log_file = log_file.replace(G_datestr_for_log, today_str.decode('utf-8').encode('cp936'))
        #更新全局日志日期字段
        G_datestr_for_log = today_str
        #设置单个日志文件大小
        log_handler_new = logging.handlers.RotatingFileHandler(log_file, maxBytes = 10240*1024, backupCount = 100)
        #日志格式
        formatter_new = logging.Formatter('%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s')
        log_handler_new.setFormatter(formatter_new)
        #移除昨天的日志handler
        G_logger.removeHandler(G_log_handler)
        G_log_handler = log_handler_new
        #更新文件处理器
        G_logger.addHandler(G_log_handler)
        #设置日志记录级别
        G_logger.setLevel(logging.DEBUG)

#首部字段
G_header_fields = ["busseID", "sendTradeNum", "senderCode", "senderName", "receiverCode", "receiverName", 
                   "intermediaryCode", "intermediaryName", "hosorgNum", "hosorgName", "systemType", 
                   "busenissType", "standardVersionCode", "clientmacAddress", "recordCount"]
#首部字段的默认值
G_header_default = ["", "", G_hospital_no, G_hospital_name, "100000001", "重庆卫计委", 
                    "", "", "001", "cqszyy", "1", 
                    "8", "version:1.0.4", "", ""]

#附加信息字段
G_addition_fields = ["curDllAddr", "receiverTradeNum", "asyncAsk", "errorCode", "callback", "correlationId", "errorMsg"]
G_addition_default = ["", "", "0", "", "", "", ""]

#一个报文最多传输200条数据 由于下标是从0开始的 故设置为199 
G_max_record = 199

class utilities():
    
    #构造函数
    def __init__(self, private_url = "10.127.8.36", public_url = "mhis-yedi-stg1.pingan.com.cn", 
                 suburl = "/yedi-platform/biz/nhfpc/q?senderCode=", ):
        self.MAC = ""
        self.private_url = private_url
        self.suburl = suburl + G_hospital_no
        self.public_url = public_url
        self.get_MAC()
    
    
    #获取本机MAC地址
    def get_MAC(self):
        mac_num = uuid.UUID(int = uuid.getnode()).hex[-12:] 
        self.MAC = (":".join([mac_num[e:e+2] for e in range(0,11,2)])).upper()
        
    #设置公网地址
    def set_public_url(self, url):
        if url and len(url) > 0:
            self.public_url = url
    #设置专网地址
    def set_private_url(self, url): 
        if url and len(url) > 0:
            self.private_url = url
    #设置访问的子地址
    def set_sub_url(self, url):
        if url and len(url):
            self.suburl = url
        
    #使用gzip压缩
    def gzip_compress(self, raw_data):
        buff = StringIO()
        fake_file = gzip.GzipFile(mode = 'wb', fileobj = buff)
        try:
            fake_file.write(raw_data)
        finally:
            fake_file.close()
        return buff.getvalue()
    
    
    #生成交易流水号 生成规则为 时间串-医院编号-3位毫秒数-4位随机数字
    def gen_serialno(self):
        time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        serial_no = "%s-%s-%s%d" % ( time_str, G_hospital_no, str(datetime.datetime.now().microsecond)[0:3], randint(1000, 9999) )
        return serial_no
    
    #为报文填入默认值
    def fill_default(self, fields, default):
        tmp_dict = {}
        #如果字段数组和缺省值数组的长度不一致 返回none
        if len(fields) != len(default):
            return None
        for index in range(len(fields)):
            tmp_dict[fields[index]] = default[index]
        return tmp_dict
        
    
    #生成报文首部 首部的业务编码需要具体业务的对象调用时才能填入
    def gen_header(self):
        #首先填写首部的默认值 留空字段为[业务编码, 发送方交易流水号, 本机mac] 
        header_dict = self.fill_default(G_header_fields, G_header_default)
        
        if header_dict:
            #填写发送方交易流水号
            header_dict["sendTradeNum"] = self.gen_serialno()
            
            #填写本机mac
            header_dict["clientmacAddress"] = self.MAC
            try:
                #json_str = json.dumps(header_dict, sort_keys = True, indent = 4)
                #G_logger.debug(convert_c("生成报文首部:\n%s" % json_str))
                return header_dict
            except Exception,e:
                G_logger.error(convert_c(e))
        else:
            G_logger.error(convert_c("报文首部生成错误"))
            return None
    
    
    #生成报文附加信息
    def gen_addtion_info(self):
        
        addition_dict = self.fill_default(G_addition_fields, G_addition_default)
        
        if addition_dict:
            try:
                #json_str = json.dumps(addition_dict, indent = 4, sort_keys = True)
                #G_logger.debug(convert_c("生成报文附加信息:\n%s" % json_str))
                return addition_dict
            except Exception, e:
                G_logger.error(convert_c(e))
                return None
        else:
            G_logger.error(convert_c("报文附加信息生成错误"))
            return None
        
    #发送json内容给卫计委监测平台  如果network为public则使用https走公网  若为private则使用http走专网  iszip=1表明需要压缩 返回值false表明发送失败
    def data_transfer(self, json_str, net_flag = 'private', iszip = 0):
        request_headers = {"Content-Type":"text/plain", "User-Agent":"xxx"}
        #encode_str = b64encode(json_str)
        http_client = None
        #是否采用gzip压缩 对应的url是不一样的
        if iszip == 1:
            real_suburl = self.suburl + "&gzip=true"
            json_str = self.gzip_compress(json_str)
        else:
            real_suburl = self.suburl
        response = None
        #走专网的话使用http协议
        response_str = ""
        if net_flag == 'private':
            try:
                http_client = httplib.HTTPConnection(self.private_url)
                http_client.request("POST", real_suburl, json_str, request_headers)
                response = http_client.getresponse()
                response_str = response.read()
                G_logger.info(convert_c("收到回复:\n%s" % response_str))
            except Exception, e:
                G_logger.error(e)
            finally:
                if http_client:
                    http_client.close()
                    
        #走公网的话走https协议
        elif net_flag == 'public':
            try:
                http_client = httplib.HTTPSConnection(self.public_url)
                sock = socket.create_connection( (http_client.host, http_client.port), timeout = 1000 )
                http_client.sock = ssl.wrap_socket(sock, http_client.key_file, http_client.cert_file)
                http_client.request("POST", real_suburl, json_str, request_headers)
                response = http_client.getresponse()
                response_str = response.read()
                G_logger.info(convert_c("收到回复:\n%s" % response_str))
            except Exception, e:
                G_logger.error(e)
            finally:
                if http_client:
                    http_client.close()
        
        #返回发送结果
        if response and response.status == 200:
            try:
                result_dict = False                
                result_dict = json.loads(response_str, encoding="utf-8")
                try:
                    if result_dict["package"]["additionInfo"]["errorCode"] == "0":
                        return result_dict
                    else:
                        return False
                except KeyError:
                    G_logger.error(convert_c("返回数据格式错误"))
                    return False
            except Exception, e:
                G_logger.error(e)
                return False
        else:
            return False

#报文包的基类定义
class package():
    def __init__(self, body_keys, body_talbe, body_index, array_key, array_table, array_index):
        #报文首部-数据类型是字典
        self.header_dict = {}
        
        #报文附加信息-数据类型是字典
        self.addtional_dict = {}
        
        #报文体-数据类型是数组 数组元素为相应的业务数据类对象
        self.body_list = []
        
        #报文体中字段值为字符串的key 后台程序应保证值为字符串的key都在同一张表中可以取到
        self.body_keys = body_keys
        
        #报文体中字段值为字符串的key 所在的数据表
        self.body_table = body_talbe
        
        #报文体中值为字符串的key 所在的数据表的索引
        self.body_index = body_index
        
        #报文体中字段值为数组的key 每个数组元素中的所有key 构成为{值为数组的key1:[字段1,字段2...], 值为数组的key2:[字段1,字段2...]}
        self.array_key = array_key
        
        #报文体中字段值为数组的key 每个数组元素中key对应字段所在的数据表 构成为{值为数组的key:所在数据表名}
        self.array_table = array_table
        
        #报文体中字段值为数组的key 在array_table中查询的索引
        self.array_index = array_index
        
        #为值为数组的key查询子表的索引值 可能为联合主键,可能需查询多个子表
        self.array_index_value = {}
        
        #记录值为字符串的已发送的数据 按发出的报文分割 数据格式为[[已发送数据的索引1,已发送数据的索引2, ...], [已发送数据的索引1,已发送数据的索引2, ...]...]
        self.sent_body_data = []
        
        #报文体定义
        self.package = {}
        
    #设置body_index_value值 查完了主表的数据后需要调用此函数
    def set_array_index_value(self, key, value):
        self.array_index_value[key] = value
    
    #生成报文的json串 可以发送空报文
    def assemble(self):
        if len(self.header_dict) == 0 or len(self.addtional_dict) == 0:
            G_logger.error(convert_c("因相关数据为空,故无法生成报文"))
            return None
        #报文组装
        temp_dict = {}
        temp_dict["head"] = self.header_dict
        temp_dict["additionInfo"] = self.addtional_dict
        temp_dict["body"] = self.body_list
        self.package["package"] = temp_dict
        package_str = None
        
        try:
            package_str = json.dumps(self.package, indent = 4, sort_keys = True)
            G_logger.info(convert_c("生成报文:\n%s" % package_str))
            return package_str
        except Exception, e:
            G_logger.error(convert_c(e))
            return None
        
#生成报文包并发送的基类定义 如果该业务单次数据量较大 bussiness_spcial应传入"top xx" xx为单次处理的记录数
class package_process():
    def __init__(self, business_id, bussiness_spcial = ""):
        self.package = None
        self.bussiness_id = business_id
        self.bussiness_spcial = bussiness_spcial
        self.utilities_obj = utilities()
        
    #传入待发送的报文    
    def set_package(self, package):
        self.package = package
        
    #生成值为字符串的key的查询语句 返回值为字符串
    def gen_body_sql(self):
        if len(self.package.body_keys) == 0 or self.package.body_table == "":
            G_logger.error(convert_c("值为字符串的key的相关数据有问题"))
            return None
        sql = "select " + self.bussiness_spcial + " "
        length = len(self.package.body_keys)
        for index in range( 0, length ):
            if (length - 1) == index:
                sql = sql + self.package.body_keys[index] + " "
            else: 
                sql = sql + self.package.body_keys[index] + ", "
        #sybase数据库的order by newid 可以随机选取数据
        #sql = sql + "from " + self.package.body_table + " where sentflag = '0' or sentflag is null order by newid()"
        #改用oracle数据库 一次最多处理40万条数据 超出容易内存溢出
        sql = sql + "from " + self.package.body_table + " where rownum < 400001 and (sentflag = '0' or sentflag is null)"
        #sql = sql + "from " + self.package.body_table + " where sentflag = '0' or sentflag is null"
        return sql
    
    #生成值为数组的key的查询语句 由于一个body内可能有多个值为数组的key 所以返回值为数组
    def gen_array_sql(self):
        if len(self.package.array_key) == 0 or len(self.package.array_table) == 0 or len(self.package.array_index) == 0:
            #G_logger.debug(convert_c("值为数组的key的相关数据为空"))
            return None
        #sql语句字典 构成为{子表名1:查询sql语句1, 子表名2:查询sql语句2}
        sql_dict = {}
        
        for item in self.package.array_key.keys():
            sql = "select "
            length = len(self.package.array_key[item])
            for index in range( 0, length ):
                if ( length -1 ) != index:
                    sql = sql + self.package.array_key[item][index] + ", "
                else:
                    sql = sql + self.package.array_key[item][index] + " "
            sql = sql + "from " + self.package.array_table[item] + " where " 
            
            #填写主键名与值
            try:
                for index in range(len(self.package.array_index[item])):
                    if index != 0:
                        sql = sql + "and "
                    sql = sql + "%s = '%s' " % (self.package.array_index[item][index], 
                                                self.package.array_index_value[item][index])
            except IndexError:
                return None
            
            sql_dict[item] = sql
            G_logger.debug(convert_c("生成子表查询sql语句:\n%s" % sql))
        return sql_dict
        
    #从数据库中提取数据
    def get_data_fromDB(self, dbconnector):
        if dbconnector:
            #需返回的结果集 元素个数应与self.sent_body_data和self.sent_array_data相同
            record_list = []
            #暂存的结果集 每一个temp_list对应于一个报文
            temp_list = []
            #暂存的body已发送结果集
            temp_body_list = []
            #暂存的array已发送结果集
            #temp_array_dict = {}
            
            body_sql = self.gen_body_sql()
            #body_sql = "select  medicalNum, billNum, medicalType, treatDate, endemicArea, 
            #deptNum, deptName, outpatientNumber, specialpatientID, reservationType, referral, 
            #siType, doctorName, credentialType, credentialNum, name, gender, birthday, race, 
            #homeAddress, companyName, sumMoney, updateBy, invoiceNO, directServiceMark, email, 
            #linkmanName, linkmanMobile, guardianName, guardianIdType, guardianIdNo, remark from 
            #V_Q299 where medicalNum = '912588343' and billNum = '2018010316:07:41'"
            
            body_rows = dbconnector.get_rows(body_sql)
            G_logger.debug(convert_c("执行sql语句:\n%s" % body_sql))
            
            if type(body_rows) == type('error'):
                G_logger.error(convert_c("从数据库中获取数据失败, 错误信息为:%s" % body_rows))
                return None
            
            #20180113 尝试解决oracle字段大写的问题
            #body_fields = dbconnector.get_field_names()
            body_fields = self.package.body_keys
            
            #计数器一个报文body中的记录不能超过G_max_record规定的数量
            counter = 0 
            
            for row in body_rows:
                #一个temp_dict就是一个报文body数组元素
                temp_dict = {}
                
                #先填值为字符串的key值
                for index in range(len(body_fields)):
                    temp_dict[body_fields[index]] = (str(row[index])).encode('utf-8','ignore')
                    if temp_dict[body_fields[index]] == "None":
                        temp_dict[body_fields[index]] = ""
                    #gc.collect()
                
                #记录主表中已发送的数据 可能为联合主键
                temp_body_index_value = []    
                for index in range(len(self.package.body_index)):
                    temp_body_index_value.append( (temp_dict[self.package.body_index[index]]).decode('utf-8', 'ignore') )
                    #gc.collect()
                temp_body_list.append( temp_body_index_value )

                #在填从body表中查出来的 用于查询子表的index的值
                for key in self.package.array_index.keys():
                    union_key_list = self.package.array_index[key]
                    temp_array_index_value = []
                    
                    try:
                        for index in range( len(union_key_list) ):
                            temp_array_index_value.append( (temp_dict[ self.package.array_index[key][index] ]).decode('utf-8','ignore') )
                            #gc.collect()
                    except Exception, e:
                        G_logger.error(convert_c(str(e)))
                        return None
                    
                    self.package.set_array_index_value( key, temp_array_index_value )
                    
                #查询子表 先生成查询子表的sql语句集   如果不需要查询相关子表 则无需查询  array_sql_dict为None
                array_sql_dict = self.gen_array_sql()
                if array_sql_dict:
                    #查询相关子表中的数据
                    for key in array_sql_dict.keys():
                        tmp_list = dbconnector.get_list(array_sql_dict[key], self.package.array_key[key])
                        
                        if type(tmp_list) == type('error'):
                            G_logger.error(convert_c("从数据库中获取数据失败, 错误信息为:%s" % tmp_list))
                            return None
                        #如果相关字段为空就不上传
                        if tmp_list != None:
                            temp_dict[key] = tmp_list
                        
                counter = counter + 1
                #如果超过了最大记录数 就重新封包
                if counter > G_max_record:
                    record_list.append(temp_list)
                    self.package.sent_body_data.append(temp_body_list)
                    #self.package.sent_array_data.append(temp_array_dict)
                    #清零
                    temp_list = []
                    temp_body_list = []
                    #temp_array_dict = {}
                    counter = 0
                    
                temp_list.append(temp_dict)
            
            #写入最后一个temp_list
            record_list.append(temp_list)
            self.package.sent_body_data.append(temp_body_list)
            #self.package.sent_array_data.append(temp_array_dict)
            
            #record_list中的每一个元素就是一个package中的body
            return record_list 
    
    #发送报文    
    def sent_package(self):
        #如果设置了报文包
        if self.package:
            #dbconn = db_connector.db_connector(dsn = "sybase", usrname = "sa", pwd = "cfrwhldb", db_type = "sybase")
            #使用oracle数据库
            dbconn = db_connector.db_connector()
            record_list = self.get_data_fromDB(dbconn)
            if record_list:
                for index in range(len(record_list)):
                    #填充报文体
                    self.package.body_list = record_list[index]
                    #不发送空报文
                    if len(self.package.body_list) < 1:
                        continue
                    #生成首部字典并填写业务号
                    self.package.header_dict = self.utilities_obj.gen_header()
                    try:
                        #填入首部的业务号
                        self.package.header_dict["busseID"] = self.bussiness_id
                        self.package.header_dict["recordCount"] = str(len(self.package.body_list))
                    except KeyError:
                        G_logger.error(convert_c("首部字段错误"))
                    
                    self.package.addtional_dict = self.utilities_obj.gen_addtion_info()
                    json_str = self.package.assemble()
                    #如果报文发送成功 则标记已发送的数据
                    result_dict = self.utilities_obj.data_transfer(json_str, 'private', 1)
                    if result_dict:
                        self.update_sent_flag(index, dbconn, result_dict)
            else:
                G_logger.error(convert_c("结果集为空"))
    
    #标记已发送的数据
    def update_sent_flag(self, index, dbconn, result_dict):
        if dbconn:
            body_list = None
            try:
                body_list = self.package.sent_body_data[index]
            except IndexError:
                G_logger.error(convert_c("标记已发送数据时发生越界错误"))
                return None
            
            #2018-01-13记录发送及接收流水号
            receiverTradeNum = ""
            sendTradeNum = ""
            try:
                receiverTradeNum = result_dict["package"]["additionInfo"]["receiverTradeNum"]
                sendTradeNum = result_dict["package"]["head"]["sendTradeNum"]
            except KeyError:
                G_logger.error(convert_c("标记接收/发送流水号时出现结果报文越界错误"))
                return None
            
            #bodylist的构成为[[联合主键1,联合主键2...],[联合主键1,联合主键2...],[联合主键1,联合主键2...]....]
            for item_list in body_list:
                sql = "update %s set sentflag = '1' , sendTradeNum = '%s', receiverTradeNum = '%s' where " % (self.package.body_table, sendTradeNum, receiverTradeNum)
                #有些业务可能使用联合主键 
                for inner_index in range(len(item_list)):
                    if inner_index != 0:
                        sql = sql + "and "
                    #处理索引值为null的情况 2018-03-31李浩添加
                    if item_list[inner_index] == '':
                        sql = sql + "%s is null " % self.package.body_index[inner_index]
                    else:
                        sql = sql + "%s = '%s' " % (self.package.body_index[inner_index], item_list[inner_index])
                #print sql
                excute_result = dbconn.excute_sql(sql)
                if type(excute_result) == type('error'):
                    G_logger.error(convert_c("执行sql语句失败:\n%s\n错误信息为:\n%s" % (sql, excute_result) ))
                else:
                    G_logger.debug(convert_c("执行sql语句成功:\n%s" % sql))
            
if __name__ == '__main__':
    pass
#     test_obj = utilities()
#     test_json = json_test.gen_test_json()
#     test_json = test_obj.gzip_compress(test_json)
#     print sys.getsizeof(test_json)
#     test_obj.gen_header()
#     test_obj.gen_addtion_info()
#     test_obj.data_transfer(test_json, 'public', 1)