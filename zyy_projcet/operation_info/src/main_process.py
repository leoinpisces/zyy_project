#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import cx_Oracle
import os
import re
import xlwt
import datetime
import logging
import db_connector

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

#相关文件的路径前缀
G_path_prefix = r"F:\project\zyy_projcet\operation_info\\"

#日志相关
G_datestr_for_log = datetime.date.today().strftime("%Y-%m-%d")
logging.basicConfig(level = logging.DEBUG, 
                    format = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s', 
                    filename = (G_path_prefix + r"log\debug_log_%s.log" % G_datestr_for_log).decode('utf-8').encode('cp936'), 
                    filemode = 'a')
G_logger= logging.getLogger('repot_logger')

#判断日期格式的正则表达式
G_date_re = re.compile(r'\d{4}/\d{2}/\d{2}')

#手术日期判断正则表达式 匹配的日期格式形如 "yyyy-mm-dd hh" 是否同一台手术在时间判断上精确到小时
G_opdate_re = re.compile(r'\d{4}-\d{2}-\d{2}\s\d{2}')

#手术信息
class operation_info:
    patient_id = ""         #患者住院号
    name = ""               #患者姓名
    operation_grade = ""    #手术级别
    wound_grade = ""        #切口等级
    operator = ""           #术者
    operation_code = ""     #手术编码
    heal = ""               #愈合情况
    anaesthesia_method = "" #麻醉方式
    dept_name = ""          #科室名称
    dept_code = ""          #科室代码
    operation_date = ""     #手术日期
    discharge_date = ""     #出院日期
    operation_desc = []     #手术操作 统一台次的手术描述

#手术信息字典 key为患者住院号 value为operation_info对象构成的列表
G_operation_info = {}

#按科室计统计手术人次  字典的构成是 科室名称:手术人次
G_mantime_dept = {}

#按科室计统计手术人数 字典的构成是 科室名称:手术人数
G_mancount_dept = {}

#按手术级别统计手术人次 字典
G_mantime_opgrade = {}

#按手术级别统计手术人数 字典的构成是 手术级别:手术人次
G_mancount_opgrade = {}

#按科室统计手术级别人次  key是科室名称，手术级别统计放在列表里面作为value 零级手术用元素0统计 以此类推
G_mantime_op_dept = {}

#函数-python内部用的是unicode 以utf-8解码 转换为可读的汉字
def convert(str):
    return str.decode('utf-8', 'ignore')

#函数-转换为中文操作系统可读的编码
def convert_c(str):
    return str.decode('utf-8').encode('cp936')

def get_info_fromdb(cursor, begin_str = datetime.date.today().strftime("%Y/%m/%d"), end_str = (datetime.date.today() + datetime.timedelta(1)).strftime("%Y/%m/%d")):
    #从数据库中提取数据
    sql = "select a.patient_id, b.name, a.operation_desc, a.operating_grade, a.wound_grade, a.operator, \
    a.operation_code, a.heal, a.anaesthesia_method, a.operation_dept_code, d.dept_name, a.operating_date, c.discharge_date_time \
    from operation a, pat_master_index b, pat_visit c, dept_dict d \
    where c.discharge_date_time > to_date('%s', 'yyyy/mm/dd') \
    and c.discharge_date_time < to_date('%s', 'yyyy/mm/dd') \
    and a.patient_id = c.patient_id \
    and c.patient_id = b.patient_id \
    and a.operation_dept_code = d.dept_code" % (begin_str, end_str)
    
    #sql = "select a.patient_id, b.name, a.operation_desc, a.operating_grade, a.wound_grade, a.operator, \
    #a.operation_code, a.heal, a.anaesthesia_method, e.operation_dept_code, d.dept_name, e.operating_date, c.discharge_date_time \
    #from report.r_operation_doct a, report.r_pat_master_index b, report.r_pat_visit c, dept_dict d, operation e \
    #where c.discharge_date_time > to_date('%s', 'yyyy/mm/dd') \
    #and c.discharge_date_time < to_date('%s', 'yyyy/mm/dd') \
    #and a.patient_id = c.patient_id \
    #and c.patient_id = b.patient_id \
    #and a.patient_id = e.patient_id \
    #and a.operation_code = e.operation_code \
    #and e.operation_dept_code = d.dept_code" % (begin_str, end_str)
    
    G_logger.info(convert("执行SQL语句:" + sql))
    
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
    except cx_Oracle.DatabaseError:
        G_logger.error(convert("数据库操作失败"))
        return 0
    
    return result

#对提取出来的数据进行合并 写入手术信息记录
def data_process(result):
    if len(result) == 0:
        G_logger.info(convert("没有符合条件的数据"))
        return 0
    
    for item in result:
        if len(item) < 13:
            continue
        #先把数据取出来放在临时对象里面 后面进行分析
        tmp_obj = operation_info()
        tmp_obj.operation_desc = [] #每次都必须归零 否则可能
        tmp_obj.patient_id = str(item[0]).strip() 
        tmp_obj.name = str(item[1]).strip()
        tmp_operation_desc = str(item[2]).strip()
        tmp_obj.operation_grade = str(item[3]).strip()
        tmp_obj.wound_grade = str(item[4]).strip()
        if tmp_obj.wound_grade == "None":
            tmp_obj.wound_grade = "未填写"
        tmp_obj.operator = str(item[5]).strip()
        if tmp_obj.operator == "None":
            tmp_obj.operator = "未填写"
        tmp_obj.operation_code = str(item[6]).strip()
        tmp_obj.heal = str(item[7]).strip()
        if tmp_obj.heal == "None":
            tmp_obj.heal = "未填写"
        tmp_obj.anaesthesia_method = str(item[8]).strip()
        if tmp_obj.anaesthesia_method == "None":
            tmp_obj.anaesthesia_method = "未填写"
        tmp_obj.dept_code = str(item[9]).strip()
        tmp_obj.dept_name = str(item[10]).strip()
        tmp_obj.operation_date = str(item[11]).strip()
        tmp_obj.discharge_date = str(item[12]).strip()
        
        
        #标识位 标识该患者一天内有多台手术
        is_multi_op = True
        
        #如果手术字典中已有该患者的住院号 则需判断是否同一台手术(术者相同且手术时间相同)
        if G_operation_info.has_key(tmp_obj.patient_id):          
            for operation in G_operation_info[tmp_obj.patient_id]:
                #同一个患者同一台手术有多个手术操作
                date_slice = G_opdate_re.findall(operation.operation_date)
                if len(date_slice) < 1:
                    G_logger.error(convert_c("日期格式错误:%s" % operation.operation_date))
                    continue
                tmp_date_slice = G_opdate_re.findall(tmp_obj.operation_date)
                if len(tmp_date_slice) < 1:
                    G_logger.error(convert_c("日期格式错误:%s" % tmp_date_slice.operation_date))
                    continue
                
                #print date_slice, tmp_date_slice
                #if (operation.operator == tmp_obj.operator) and ( date_slice == tmp_date_slice): 
                #是否同一台手术只判断手术时间(精确到小时)
                if date_slice == tmp_date_slice:
                    operation.operation_desc.append(tmp_operation_desc)
                    is_multi_op = False
                    break
            #将该患者的手术信息记录遍历查询完 发现同一个患者住院期间有多台手术
            if is_multi_op:
                tmp_obj.operation_desc.append(tmp_operation_desc) #将手术操作描述记入对象实例中
                (G_operation_info[tmp_obj.patient_id]).append(tmp_obj) #将对象实例记入该病人名下
        #没有相应住院号的手术记录
        else:
            tmp_op_list = []
            tmp_obj.operation_desc.append(tmp_operation_desc)
            tmp_op_list.append(tmp_obj)
            G_operation_info[tmp_obj.patient_id] = tmp_op_list

#写入结果excel手术信息sheet的第一行
def write_excel_firstline(sheet):
    sheet.write(0, 0, convert_c("病案号"))
    sheet.write(0, 1, convert_c("患者姓名"))
    sheet.write(0, 2, convert_c("手术描述"))
    sheet.write(0, 3, convert_c("手术级别"))
    sheet.write(0, 4, convert_c("切口级别"))
    sheet.write(0, 5, convert_c("术者"))
    sheet.write(0, 6, convert_c("手术编码"))
    sheet.write(0, 7, convert_c("切口愈合等级"))
    sheet.write(0, 8, convert_c("麻醉方式"))
    sheet.write(0, 9, convert_c("手术科室"))
    sheet.write(0, 10, convert_c("手术日期"))
    sheet.write(0, 11, convert_c("出院日期"))
    
    return sheet

#转换手术级别
def int_grade2str_grade(int_grade):
    tmp_str = ""
    if int_grade == "1":
        tmp_str = "一级手术"
    elif int_grade == "2":
        tmp_str = "二级手术"
    elif int_grade == "3":
        tmp_str = "三级手术"
    elif int_grade == "4":
        tmp_str = "四级手术"
    else:
        tmp_str = "零级手术"
    return tmp_str

#根据手术级别返回列表索引
def grade2index(int_grade):
    if int_grade == "1":
        return 1
    elif int_grade == "2":
        return 2
    elif int_grade == "3":
        return 3
    elif int_grade == "4":
        return 4
    else:
        return 0


#将手术人次和手术人数写入excel 可变参数 传入的字典 其key应该是一致的
def maninfo_write(sheet, *man_dict_list):
    keys = (man_dict_list[0]).keys()
    #0行已经写了表头 所以从1行开始
    line_index = 1
    
    #合计值 有多少种统计口径 sum列表中就有多少元素
    sum = []
    for i in range(len(man_dict_list)):
        sum.append(0)
        
    for key in keys:
        sheet.write(line_index, 0, convert_c(key))
        for i in range(len(man_dict_list)):
            #i从0开始 但0列已经写了项目名称了 所以写成i+1
            try:
                sheet.write(line_index, i + 1, (man_dict_list[i])[key])
            except KeyError:
                G_logger.error(convert_c("元素%s在记录表%s中不存在" % (key, man_dict_list[i].name)))
            
            #统计某指标的合计
            sum[i] += (man_dict_list[i])[key]
        line_index += 1
        
    sheet.write(line_index, 0, convert_c("合计"))
    for i in range(len(man_dict_list)):
        #第0列已经写了项目名称了所以从第i+1列开始
        sheet.write(line_index, i + 1, sum[i])
    
#数据统计并写excel的函数
def statistics_write():
    tmp_keys = G_operation_info.keys()
    if len(tmp_keys) == 0:
        return
    #写结果到excel
    try:
        #创建excel
        result_xls = xlwt.Workbook(encoding='cp936')
        sheet = result_xls.add_sheet(convert_c("手术信息"), cell_overwrite_ok = True)
        sheet = write_excel_firstline(sheet)
        
        #写完首行后 置行索引为1
        line_index = 1
        #遍历手术操作信息
        for patient_id in tmp_keys:
            dept_set = set()
            opgrade_set = set()
            for operation in G_operation_info[patient_id]:
                opgrade = int_grade2str_grade(operation.operation_grade)
                sheet.write(line_index, 0 , operation.patient_id)
                sheet.write(line_index, 1 , convert_c(operation.name))
                sheet.write(line_index, 2 , convert_c("!@!".join(operation.operation_desc)))
                sheet.write(line_index, 3 , convert_c(opgrade))
                sheet.write(line_index, 4 , convert_c(operation.wound_grade))
                sheet.write(line_index, 5 , convert_c(operation.operator))
                sheet.write(line_index, 6 , convert_c(operation.operation_code))
                sheet.write(line_index, 7 , convert_c(operation.heal))
                sheet.write(line_index, 8 , convert_c(operation.anaesthesia_method))
                sheet.write(line_index, 9 , convert_c(operation.dept_name))
                sheet.write(line_index, 10 , convert_c(operation.operation_date))
                sheet.write(line_index, 11 , convert_c(operation.discharge_date))
                line_index = line_index + 1 
                
                #按科室和手术级别统计人次
                if G_mantime_dept.has_key(operation.dept_name):
                    G_mantime_dept[operation.dept_name] += 1
                else:
                    G_mantime_dept[operation.dept_name] = 1
                
                if G_mantime_opgrade.has_key(opgrade):
                    G_mantime_opgrade[opgrade] += 1
                else:
                    G_mantime_opgrade[opgrade] = 1
                    
                #按科室统计手术级别的人次  grade2index可以保证index不会越界
                index = grade2index(operation.operation_grade)
                if G_mantime_op_dept.has_key(operation.dept_name):
                    (G_mantime_op_dept[operation.dept_name])[index] =  (G_mantime_op_dept[operation.dept_name])[index] + 1
                else:
                    tmp_list = [0, 0, 0, 0, 0]
                    tmp_list[index] = 1
                    G_mantime_op_dept[operation.dept_name] = tmp_list
                    
                #记录此患者的手术科室和手术级别  每一个operation_info 对象都对应一对手术科室和手术级别
                dept_set.add(operation.dept_name)
                opgrade_set.add(opgrade)
            
            #统计手术人数 同一个患者在同一个科室做了多次手术 人数只能算1个 所以要用set来去重计算 手术级别人数的类似
            for item in dept_set:
                if G_mancount_dept.has_key(item):
                    G_mancount_dept[item] += 1
                else:
                    G_mancount_dept[item] = 1
                    
            for item in opgrade_set:
                if G_mancount_opgrade.has_key(item):
                    G_mancount_opgrade[item] += 1
                else:
                    G_mancount_opgrade[item] = 1
        
        #写入手术人数和手术人次
        sheet = result_xls.add_sheet(convert_c("按科室统计"), cell_overwrite_ok = True)
        sheet.write(0, 0, convert_c("科室名称"))
        sheet.write(0, 1, convert_c("手术人次"))
        sheet.write(0, 2, convert_c("手术人数"))
        maninfo_write(sheet, G_mantime_dept, G_mancount_dept)
        
        sheet = result_xls.add_sheet(convert_c("按手术级别统计"), cell_overwrite_ok = True)
        sheet.write(0, 0, convert_c("手术级别"))
        sheet.write(0, 1, convert_c("手术人次"))
        sheet.write(0, 2, convert_c("手术人数"))
        maninfo_write(sheet, G_mantime_opgrade, G_mancount_opgrade)
        
        #按科室统计手术级别 写入excel
        sheet = result_xls.add_sheet(convert_c("按科室统计手术级别"), cell_overwrite_ok = True)
        sheet.write(0, 0, convert_c("科室名称"))
        sheet.write(0, 1, convert_c("零级手术"))
        sheet.write(0, 2, convert_c("一级手术"))
        sheet.write(0, 3, convert_c("二级手术"))
        sheet.write(0, 4, convert_c("三级手术"))
        sheet.write(0, 5, convert_c("四级手术"))
        #将结果写入excel
        depts = G_mantime_op_dept.keys()
        tmp_index = 1 #从第一行开始写 第零行写了表头了
        for dept in depts:
            sheet.write(tmp_index, 0, convert_c(dept))
            for i in range(len(G_mantime_op_dept[dept])):
                sheet.write(tmp_index, i + 1, (G_mantime_op_dept[dept])[i])
            tmp_index = tmp_index + 1
              
        result_xls.save((G_path_prefix + r"result\手术信息统计" + (datetime.datetime.now()).strftime("%Y-%m-%d_%H-%M-%S") + ".xls").decode('utf-8').encode('cp936'))
        
        return 1
    
    except Exception,e:
        G_logger.error(convert_c(str(e)))
        return 0
        

#主函数
if __name__ == '__main__':
    
    #从命令行输入提取的开始和结束日期
    b_str = ""
    e_str = ""
    b_str = raw_input(convert("请输入提取的开始日期，格式为yyyy/mm/dd\n"))
    e_str = raw_input(convert("请输入提取的结束日期，格式为yyyy/mm/dd\n"))
    
    #判断参数 如果有一个输入参数为空 则提取程序运行上个月的数据
    if len(b_str) == 0 or len(e_str) == 0:
        today = datetime.date.today()
        b_str = datetime.date(today.year, today.month - 1,1).strftime("%Y/%m/%d")
        e_str = datetime.date(today.year, today.month, 1).strftime("%Y/%m/%d")   
    #判断参数 是否符合日期规则
    elif G_date_re.match(b_str) == None or G_date_re.match(e_str) == None:
        print(convert("输入参数不合法,程序退出!!"))
        G_logger.error(convert("输入参数不合法,程序退出!!"))
        sys.exit()
        
    #获取数据库连接
    try:
        conn = db_connector.get_connection()
    except cx_Oracle.DatabaseError:
        G_logger.error(convert("连接数据库失败"))
        sys.exit()
   
    G_logger.info(convert("连接数据库成功"))
        
    #从数据库中获取手术患者基本信息
    result = get_info_fromdb(conn.cursor(), b_str, e_str)
    
    #数据处理与统计
    if result != 0:
        data_process(result)
    else:
        G_logger.info(convert("由于未从数据库中获取到有效数据，程序终止"))
    
    #写excel
    if statistics_write() == 0:
        G_logger.error(convert("写入excel失败"))
    
    #关闭数据库连接
    try:
        db_connector.close_connection(conn)
    except cx_Oracle.DatabaseError:
        G_logger.error(convert("关闭数据库连接失败"))
        
    G_logger.info(convert("数据库连接关闭成功"))
    