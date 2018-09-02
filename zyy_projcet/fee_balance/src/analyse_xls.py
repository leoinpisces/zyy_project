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

G_path_prefix = r'E:\project\fee_balance\\'

G_t6_fee_list = ['T635','T636','T637','T638','T639','T640','T641','T642','T643','T644','T645','T646']


#科室收入
class dept_income:
    def __init__(self):
        self.dept_name = ""
        self.dept_code = ""
        self.income = {}
        

#函数-python内部用的是unicode 以utf-8解码 转换为可读的汉字
def convert(str):
    return str.decode('utf-8', 'ignore')

#从表6中获取科室的相关收入数据，返回dept_income的对象列表
def load_info():
    info_dict = {}
    #打开表格  遍历所有行和列 填写患者信息
    workbook = xlrd.open_workbook( (G_path_prefix + r"data\dept_cost.xlsx").decode('utf-8', 'ignore').encode('cp936') )
#     print workbook.sheet_names() 获取所有工作表的名字
    active_sheet = workbook.sheet_by_name('Sheet1')
#     row = active_sheet.row_values(0) 取到第一行的内容
    for row_index in range(4, active_sheet.nrows):
        temp_item = dept_income()
        temp_item.dept_code = active_sheet.cell(row_index, 1).value
        #住院科室编码以2开头 只获取住院的数据
        if temp_item.dept_code[0:1] != "2":
            break
        temp_item.dept_name = active_sheet.cell(row_index, 2).value
        #获取科室收入信息
        for item in G_t6_fee_list:
            temp_item.income[item] = active_sheet.cell(row_index, int(item[-2:])).value
        if not info_dict.has_key(temp_item.dept_code):
            info_dict[temp_item.dept_code] = temp_item
    return info_dict

if __name__ == '__main__':
    load_info()