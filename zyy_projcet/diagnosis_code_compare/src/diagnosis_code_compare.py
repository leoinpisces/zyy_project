#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cx_Oracle
import os
import re
import datetime
import logging

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#函数-python内部用的是unicode 以utf-8解码 转换为可读的汉字
def convert(str):
    return str.decode('utf-8', 'ignore')

G_path_prefix = r"C:\code\\"

#日志相关
G_datestr_for_log = datetime.date.today().strftime("%Y-%m-%d")
logging.basicConfig(level = logging.DEBUG, 
                    format = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s', 
                    filename = (G_path_prefix + r"diagnosis_compare\log\debug_log_%s.log" % G_datestr_for_log).decode('utf-8').encode('cp936'), 
                    filemode = 'a')
G_logger= logging.getLogger('repot_logger')

class G_dict:
    #结果字典
    result_dict = {}
    #科室字典
    dept_dict = {}
    #标准诊断字典
    diagnosis_dict = {}
    #科室诊断描述计数字典 key的构成规则为 code---desc
    diagnosis_count = {}
    
class G_count:
    diagnosis_count = 0

#判断院内定制编码的正则表达式
G_custom_code_regex = re.compile(r"[A-Za-z]\d{2}\.[A-Za-z0-9]\d{4}")
#院内定制编码列表
G_custom_code_list = []

#函数-连接oracle数据库
def get_connection():
    user_name = 'jhemr'
    user_pwd = 'jhemr'
    host = '192.168.248.198'
    port = 1521
    service_name = 'JHEMRCS'
    dsn = cx_Oracle.makedsn(host, port, service_name)
    conn = cx_Oracle.connect(user_name, user_pwd, dsn)
    G_logger.info(convert("获取数据库连接成功: 服务器地址为%s,服务名为%s,端口号为%d" % (host, service_name, port)))
    return conn

    
#函数-关闭数据库连接
def close_connection(conn):
    conn.cursor().close()
    conn.close()
    G_logger.info(convert("数据库连接关闭"))


#函数-获取14年以来所有患者的出院诊断编码  诊断描述  写入结果字典和诊断描述计数字典 按科室
def get_diagnosis(cursor, dept_code):
    if dept_code == "":
        G_logger.error(convert("科室代码为空"))
        return 1
    
    sql = "select a.diagnosis_code, b.diagnosis_desc from diagnostic_category a, diagnosis b \
    where b.diagnosis_type = '3' and a.patient_id = b.patient_id and a.diagnosis_no = b.diagnosis_no and a.diagnosis_type = b.diagnosis_type \
    and b.patient_id in (select patient_id from pat_visit where dept_discharge_from = '%s' and discharge_date_time > to_date('2014/01/01', 'yyyy/mm/dd') \
    and discharge_date_time < to_date('2016/12/31', 'yyyy/mm/dd'))" % dept_code
    
    try:
        cursor.execute(sql) 
        result = cursor.fetchall()
    except cx_Oracle.DatabaseError:
        G_logger.error(convert("操作数据库失败"))
        return 1
    
    G_logger.info(sql)
    
    #相关科室诊断列表为空
    if cursor.rowcount == 0:
        try:
            G_logger.info(convert("%s诊断列表为空" % G_dict.dept_dict[dept_code]))
        except KeyError:
            G_logger.error(convert("科室字典中不存在代码为%s的字典") % dept_code)
        finally:
            return 1
    
    G_logger.info(convert("待处理总数:---%d" % cursor.rowcount))
    
    for item in result:
        if len(item) < 2:
            G_logger.error(convert("诊断编码和描述项数据长度错误"))
            
        diagnosis_code = str(item[0]).strip()
        diagnosis_desc = str(item[1]).strip()
        
        #如果结果字典中已经存在该编码
        if G_dict.result_dict.has_key(diagnosis_code):
            #如果字典中存在相应诊断描述 则只更新计数字典
            if (G_dict.result_dict[diagnosis_code]).count(diagnosis_desc) > 0:
                try:
                    G_dict.diagnosis_count[diagnosis_code + "---" + diagnosis_desc] = G_dict.diagnosis_count[diagnosis_code + "---" + diagnosis_desc] + 1
                except KeyError:
                    G_dict.diagnosis_count[diagnosis_code + "---" + diagnosis_desc] = 1
            #如果字典中没有相应诊断描述 应向字典项中添加描述 随后更新计数字典
            else:
                G_dict.result_dict[diagnosis_code] = G_dict.result_dict[diagnosis_code] + "!@!" + diagnosis_desc
                G_dict.diagnosis_count[diagnosis_code + "---" + diagnosis_desc] = 1
        #字典中不存在该诊断编码
        else:
            G_dict.result_dict[diagnosis_code] = diagnosis_desc
            G_dict.diagnosis_count[diagnosis_code + "---" + diagnosis_desc] = 1
            
    return 0

#载入科室字典文件
def load_dict(dict_name):
    dict_path = (G_path_prefix + r"diagnosis_compare\dict\%s.txt" % dict_name).decode('utf-8').encode('cp936')
    G_logger.info(convert("开始载入字典文件: ") + dict_path)
    dict_file = open(dict_path)
    temp_dict = {}
    
    for line in dict_file:
        line = line.strip()
        if line == "" or line.count(",") == 0:
            G_logger.error(convert("字典项错误: " + line))
            continue
        #不处理注释掉的行
        if line.count("#") > 0:
            continue
        split_list = line.split(",")
        if len(split_list) < 2:
            G_logger.error(convert("字典项错误: " + line))
            continue
        split_list[0] = split_list[0].strip()
        split_list[1] = split_list[1].strip()
        temp_dict[split_list[0]] = split_list[1]
    
    G_logger.info(convert("字典长度为: ") + str(len(temp_dict)))
    
    #字典名称为dept_dict时载入科室字典
    if dict_name == "dept_dict":
        G_logger.info(convert("科室字典载入完成"))
        G_dict.dept_dict = temp_dict
    elif dict_name == "diagnosis_dict":
        G_logger.info(convert("诊断字典载入完成"))
        G_dict.diagnosis_dict = temp_dict

#函数-提取医院自定义的诊断字典项
def get_custom_code():
    if len(G_dict.diagnosis_dict) == 0:
        G_logger.error(convert("诊断字典长度为空"))
        return
    custom_file = open(G_path_prefix + r"diagnosis_compare\result\custom_code.txt", 'a+')
    standard_file = open(G_path_prefix + r"diagnosis_compare\result\standard_code.txt", 'a+')
    key_list = G_dict.diagnosis_dict.keys()
    for key in key_list:
        if len(G_custom_code_regex.findall(key)) > 0:
            custom_file.write(key + "," + convert(G_dict.diagnosis_dict[key]) + "\r")
        else:
            standard_file.write(key + "," + convert(G_dict.diagnosis_dict[key]) + "\r")
            
    custom_file.close()
    standard_file.close()

#将结果写入相应文件名的文件 
def write_result(dept_code):
    if len(G_dict.result_dict) == 0:
        G_logger.error(convert(G_dict.dept_dict[dept_code] + "的科室诊断字典为空"))
        return
    file_path = G_path_prefix + (r"diagnosis_compare\result\%s.txt" % G_dict.dept_dict[dept_code]).decode('utf-8').encode('cp936')
    
    try:
        temp_file = open(file_path, 'a+')
        G_logger.info(convert("准备写入%s的科室结果字典" % G_dict.dept_dict[dept_code]))
    except IOError:
        G_logger.error(convert("%s的结果字典文件打开失败" % G_dict.dept_dict[dept_code]))
    
    count = 0  
    keys = G_dict.diagnosis_count.keys()
    for key in keys:
        count = count + G_dict.diagnosis_count[key]
    G_logger.info(convert("诊断描述总数为: %d" % count))
    G_count.diagnosis_count = G_count.diagnosis_count + count
    
    #遍历结果字典
    keys = G_dict.result_dict.keys()
    try:
        for key in keys:
            try:
                temp_file.write(convert("标准诊断编码:---") + key + convert("---对应的标准诊断描述:---") + G_dict.diagnosis_dict[key] + "\r" + convert("对应的科室诊断描述:") + "\r")
            except KeyError:
                G_logger.error(convert("未在字典中找到诊断编码:---") + key + convert("---对应的诊断描述:---") + G_dict.result_dict[key])
                continue
            
            desc_list = G_dict.result_dict[key].split("!@!")
            for item in desc_list:
                #先判断是否标准诊断描述 若是 直接写入出现次数
                try:
                    if item == G_dict.diagnosis_dict[key]:
                        temp_file.write(convert("标准诊断描述出现%d次" % G_dict.diagnosis_count[key + "---" + item]) +"\r")
                        continue
                except KeyError:
                    G_logger.error(convert("未在出现计数字典中找到诊断描述:---%s" % item))
                    continue
                
                
                temp_file.write(convert(item) + "---" + convert("出现次数:---"))
                
                #写入该诊断描述出现的次数
                try:
                    temp_file.write(str(G_dict.diagnosis_count[key + "---" + item]) + "\r")
                except KeyError:
                    G_logger.error(convert("未在出现计数字典中找到诊断描述:---%s" % item))
                    
            temp_file.write("\r\n")
    finally:
        temp_file.close()        
    
#函数-提取病历中的诊断
def get_result(cursor):
    if len(G_dict.dept_dict) == 0:
        G_logger.error(convert("科室字典为空"))
        return
    
    #遍历科室字典 调用get_diagnosis
    dept_list = G_dict.dept_dict.keys()
    for dept_code in dept_list:
        G_dict.result_dict = {}
        G_dict.diagnosis_count = {}
        #取回该科室14年至今所有出院诊断的描述
        if get_diagnosis(cursor, dept_code) == 0:
            if len(G_dict.result_dict) == 0:
                G_logger.error(convert(G_dict.dept_dict[dept_code] + " 科室诊断获取失败"))
                continue
            else:
                write_result(dept_code)
        else:
            continue
        

if __name__ == '__main__':
    try:
        conn = get_connection()
        cursor = conn.cursor()
    except cx_Oracle.DatabaseError:
        G_logger.error(convert("数据库连接错误"))
        sys.exit()
        
    load_dict("diagnosis_dict")
    load_dict("dept_dict")
    get_result(cursor)
    
    try:
        close_connection(conn)
    except cx_Oracle.DatabaseError:
        G_logger.error(convert("数据库连接关闭失败"))
        sys.exit()
    G_logger.info(convert("处理的诊断总数为:%d" % G_count.diagnosis_count))
    print convert("处理完成")
    

