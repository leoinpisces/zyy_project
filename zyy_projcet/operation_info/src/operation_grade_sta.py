#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re
import xlwt
import xlrd
import datetime


os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

reload(sys)
sys.setdefaultencoding('utf8')

G_path_prefix = r'E:\project\operation_info\\'

G_chn_digit = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十']

G_load_info = {} #存储编码字典 结构为{编码,[operation_grade对象列表]}

G_error_list = []

G_code_name = {}

class operation_grade():
    def __init__(self):
        self.op_code = ''
        self.op_name = ''
        self.op_grade = ''
        self.dept = ''
        
    def print_member(self):
        print "手术编码:%s--手术名称:%s--手术级别:%s--定级科室:%s" % (self.op_code, self.op_name, self.op_grade, self.dept)
        
#函数-转换为中文操作系统可读的编码
def convert_c(str):
    return str.decode('utf-8').encode('cp936')
        
def list_filename(path):
    filename_list = []
    for filename in os.listdir(path):
        filename_list.append(filename)
        #print filename.decode('cp936')
    return filename_list 

def generate_dict():
    path = ( G_path_prefix + r"data\operation_grade\\" ).decode('utf-8').encode('cp936')
    filename_list = list_filename(path)
    for name in filename_list:
        file_path = path + name
        name = name.decode('cp936').encode('utf-8')
        #外二科的excel不规范 暂时不考虑
        if ('外二'.decode('utf-8').encode('cp936')) in file_path:
            continue
        dept_str = name[:name.find('.')]
        workbook = xlrd.open_workbook(file_path)
        sheet_list = workbook.sheet_names()
        active_sheet = workbook.sheet_by_name(sheet_list[0])
        #逐行扫描
        for row_index in range(0, active_sheet.nrows):
            temp_item = operation_grade()
            temp_item.dept = dept_str
            temp_str = str(active_sheet.cell(row_index, 0).value)
            #手术编码前两位是数字且包含'.'
            if temp_str[:2].isdigit() and '.' in temp_str:
                temp_item.op_code = temp_str
                
                temp_str = str(active_sheet.cell(row_index, 1).value).strip()
                temp_item.op_name = temp_str
                
                temp_str = str(active_sheet.cell(row_index, 4).value).strip()
                if len(temp_str) == 0:
                    G_error_list.append("%s的手术:%s-%s未定级 " %(temp_item.dept, temp_item.op_code, temp_item.op_name))
                    continue
                temp_str = temp_str.replace("手术", '')
                temp_str = temp_str.replace("级", '')
                temp_str = temp_str.strip()
                #处理某些科室把级别写成阿拉伯数字的情况
                if '.' in temp_str:
                    temp_str = temp_str[:temp_str.find('.')]
                if temp_str.isdigit():
                    temp_int = int(temp_str)
                    if temp_int > 4:
                        G_error_list.append("手术%s在%s定级错误,科室定级为%s" % (temp_item.op_code, temp_item.dept, temp_str))
                        continue
                    else:
                        temp_str = G_chn_digit[temp_int]
                temp_item.op_grade = temp_str
                
                if G_load_info.has_key(temp_item.op_code):
                    G_load_info[temp_item.op_code].append(temp_item)
                    #temp_item.print_member()
                else:
                    G_load_info[temp_item.op_code] = [temp_item,] #由单个对象生成一个列表
                    #temp_item.print_member()
                G_code_name[temp_item.op_code] = temp_item.op_name
            elif '编码' in temp_str:
                #首行不考虑
                continue
            else:
                temp_str = str(active_sheet.cell(row_index, 1).value).strip()
                if len(temp_str) == 0:
                    temp_str = str(active_sheet.cell(row_index, active_sheet.ncols - 1).value).strip()
                    G_error_list.append("%s的手术:%s无对应标准编码" % (temp_item.dept, temp_str))     
    
def find_repeat():
    if len(G_load_info) == 0:
        print "未装载有效信息！！"
        return
    #将定级不重复的写入excel
    result_xls = xlwt.Workbook(encoding='cp936')
    sheet_1 = result_xls.add_sheet('sheet 1', cell_overwrite_ok = True)
    sheet_1.write(0, 0, convert_c("手术编码"))
    sheet_1.write(0, 1, convert_c("手术名称"))
    sheet_1.write(0, 2, convert_c("手术级别"))
    sheet_1.write(0, 3, convert_c("开展科室列表"))
    write_line_index = 1
     
    for op_code in G_load_info.keys():
        if len(G_load_info[op_code]) != 1:
            temp_dict = {} #数据结构为{科室,定级}
            grade_set = set()
            
            for item in G_load_info[op_code]:
                #print op_code, item.dept, item.op_grade
                if temp_dict.has_key(item.dept) and temp_dict[item.dept] != item.op_grade:
                    G_error_list.append("%s的手术:%s定级重复" % (item.dept, item.op_code))
                    continue
                else:   
                    temp_dict[item.dept] = item.op_grade
                grade_set.add(item.op_grade)
                    
            if len(grade_set) != 1:
                print "手术%s在%s间的定级可能存在重复" % ( op_code, ",".join(temp_dict.keys()) )
                print "相应级别为%s" % ",".join(grade_set)
                G_error_list.append("手术%s--%s在%s间的定级可能存在重复" % ( op_code, G_code_name[op_code], ",".join(temp_dict.keys()) ))
                err_msg = "其中"
                for dept_name in temp_dict.keys():
                    temp_str = "%s定级为:%s级," % (dept_name, temp_dict[dept_name])
                    err_msg = err_msg + temp_str
                G_error_list.append(err_msg + '\n')
            else:
                sheet_1.write( write_line_index, 0, convert_c(op_code) )
                sheet_1.write( write_line_index, 1, convert_c(G_code_name[op_code]) )
                sheet_1.write( write_line_index, 2, convert_c(grade_set.pop()) )
                col_index = 3
                for dept in temp_dict.keys():
                    sheet_1.write( write_line_index, col_index, convert_c(dept) )
                    col_index = col_index + 1
                write_line_index = write_line_index + 1
                
    result_xls.save((G_path_prefix + r"result\手术定级列表.xls").decode('utf-8').encode('cp936'))
                
if __name__ == '__main__':
    generate_dict()
#     for op_code in G_load_info.keys():
#         print op_code
#         for item in G_load_info[op_code]:
#             item.print_member()
        
    find_repeat()
    result_file = open(( G_path_prefix + r"result\手术定级问题校验.txt" ).decode('utf-8').encode('cp936'), "a+")
    result_file.write('\n'.join(G_error_list))
    result_file.close()
